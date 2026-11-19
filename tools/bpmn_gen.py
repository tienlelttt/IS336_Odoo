"""Sinh file BPMN 2.0 (có DI, mở được bằng Camunda Modeler desktop) và ảnh PNG trắng đen từ cùng một đặc tả.

Dùng: python tools/bpmn_gen.py   → ghi bpmn/<tên>.bpmn và bpmn/<tên>.png
Mỗi sơ đồ là một collaboration: pool công ty (các lane phòng ban) và pool riêng cho từng bên ngoài
(spec["external"]: khách hàng, nhà cung cấp, ngân hàng). Luồng giữa hai pool là message flow (nét đứt).
"""
import sys
from pathlib import Path
from xml.sax.saxutils import escape

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).parent))
from bpmn_specs import PROCESSES  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "bpmn"
COMPANY = "Công ty TNHH Bánh Bảo Hân"
COL_W, LANE_H, EXT_H, GAP = 170, 150, 130, 60
POOL_W, LANE_W = 30, 30
X_C = POOL_W + LANE_W + 20  # mép trái vùng vẽ phần tử
SIZES = {"start": (36, 36), "msgstart": (36, 36), "timer": (36, 36), "end": (36, 36), "gw": (50, 50),
         "task": (130, 80), "user": (130, 80), "service": (130, 80), "send": (130, 80), "receive": (130, 80),
         "call": (130, 80)}
TAG = {"start": "startEvent", "msgstart": "startEvent", "timer": "startEvent", "end": "endEvent",
       "gw": "exclusiveGateway", "task": "task", "user": "userTask", "service": "serviceTask", "send": "sendTask",
       "receive": "receiveTask", "call": "callActivity"}
EVENTS = ("start", "msgstart", "timer", "end")


def pools(spec):
    """Danh sách pool từ trên xuống: (id, tên, các lane, y, cao). Bên ngoài ở trên, công ty ở dưới."""
    ext = spec.get("external", [])
    out, y = [], 0
    for i, name in enumerate(ext):
        out.append((f"Ext{i}", name, [name], y, EXT_H))
        y += EXT_H + GAP
    lanes = [ln for ln in spec["lanes"] if ln not in ext]
    out.append(("Main", COMPANY, lanes, y, len(lanes) * LANE_H))
    return out


def layout(spec):
    ps = pools(spec)
    ncol = max(n[3] for n in spec["nodes"]) + 1
    width = X_C + ncol * COL_W + 20
    lane_y, pool_of = {}, {}
    for pid, _name, lanes, y, h in ps:
        lh = h // len(lanes)
        for i, ln in enumerate(lanes):
            lane_y[ln] = (y + i * lh, lh)
            pool_of[ln] = pid
    pos, node_pool = {}, {}
    for nid, typ, lane, col, _label in spec["nodes"]:
        w, h = SIZES[typ]
        ly, lh = lane_y[lane]
        cx, cy = X_C + col * COL_W + COL_W // 2, ly + lh // 2
        pos[nid] = (cx - w // 2, cy - h // 2, w, h)
        node_pool[nid] = pool_of[lane]
    return width, ps, pos, node_pool


def hits(pts, boxes):
    """Đường gấp khúc (chỉ đoạn ngang/dọc) có cắt hộp nào không (hộp nới 6px)."""
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        lx, hx, ly, hy = min(x1, x2), max(x1, x2), min(y1, y2), max(y1, y2)
        for bx, by, bw, bh in boxes:
            if lx < bx + bw + 6 and hx > bx - 6 and ly < by + bh + 6 and hy > by - 6:
                return True
    return False


def waypoints(a, b, boxes=(), from_gw=False):
    """Đường vuông góc từ a tới b; thử lần lượt các phương án, lấy phương án đầu tiên không cắt hộp khác.
    Ra khỏi cổng: nhánh lên/xuống đi từ đỉnh trên/dưới của cổng, nhánh ngang đi từ đỉnh phải, để các nhánh không chung đoạn."""
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    cands = []
    ty = by + bh // 2
    if from_gw and bx > ax and abs(ty - (ay + ah // 2)) > 2:
        gx = ax + aw // 2
        cands.append([(gx, ay if ty < ay else ay + ah), (gx, ty), (bx, ty)])
    if bx > ax:  # đi tới
        s, t = (ax + aw, ay + ah // 2), (bx, by + bh // 2)
        if s[1] == t[1]:
            cands.append([s, t])
        else:
            for mx in ((s[0] + t[0]) // 2, s[0] + 20, t[0] - 20):
                cands.append([s, (mx, s[1]), (mx, t[1]), t])
    for top in (min(ay, by) - 22, max(ay + ah, by + bh) + 22):  # vòng phía trên, rồi phía dưới
        sy, ty = (ay, by) if top < ay else (ay + ah, by + bh)
        cands.append([(ax + aw // 2, sy), (ax + aw // 2, top), (bx + bw // 2, top), (bx + bw // 2, ty)])
    for pts in cands:
        if not hits(pts, boxes):
            return pts
    return cands[0]


def msg_waypoints(a, b, band_y, ds=0, dt=0):
    """Message flow: đi dọc ra khỏi phần tử, ngang trong khoảng trống giữa hai pool, rồi dọc vào đích.
    ds, dt: lệch điểm chạm khỏi giữa cạnh khi một phần tử có nhiều message flow."""
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    sx, tx = ax + aw // 2 + ds, bx + bw // 2 + dt
    s = (sx, ay + ah) if by > ay else (sx, ay)
    t = (tx, by) if by > ay else (tx, by + bh)
    if abs(sx - tx) < 2:
        return [s, (sx, t[1])]
    return [s, (sx, band_y), (tx, band_y), t]


def split_flows(key, spec, node_pool):
    seq, msg = [], []
    for i, (src, dst, label) in enumerate(spec["flows"]):
        assert src in node_pool and dst in node_pool, (key, src, dst)
        (seq if node_pool[src] == node_pool[dst] else msg).append((f"Flow_{key}_{i}", src, dst, label))
    return seq, msg


def band_for(ps, pos, src, dst, k):
    """Độ cao đoạn ngang của message flow: trong khoảng trống ngay trên pool thấp hơn, lệch nhau theo thứ tự."""
    lower_top = max(y for _p, _n, _l, y, _h in ps if y <= max(pos[src][1], pos[dst][1]))
    return lower_top - GAP // 2 + (k % 5 - 2) * 8


def to_bpmn(key, spec):
    width, ps, pos, node_pool = layout(spec)
    types = {n[0]: n[1] for n in spec["nodes"]}
    seq, msg = split_flows(key, spec, node_pool)
    proc = {pid: f"Process_{key}_{pid}" for pid, *_ in ps}
    x = ['<?xml version="1.0" encoding="UTF-8"?>',
         '<bpmn:definitions xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL" '
         'xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI" xmlns:dc="http://www.omg.org/spec/DD/20100524/DC" '
         'xmlns:di="http://www.omg.org/spec/DD/20100524/DI" xmlns:modeler="http://camunda.org/schema/modeler/1.0" '
         f'id="Definitions_{key}" targetNamespace="http://bpmn.io/schema/bpmn" exporter="Camunda Modeler" '
         'exporterVersion="5.0.0" modeler:executionPlatform="Camunda Platform" modeler:executionPlatformVersion="7.20.0">',
         f'  <bpmn:collaboration id="Collaboration_{key}">']
    for pid, name, *_ in ps:
        x.append(f'    <bpmn:participant id="Participant_{key}_{pid}" name="{escape(name)}" processRef="{proc[pid]}" />')
    for fid, src, dst, label in msg:
        name = f' name="{escape(label)}"' if label else ""
        x.append(f'    <bpmn:messageFlow id="{fid}"{name} sourceRef="{src}" targetRef="{dst}" />')
    x.append('  </bpmn:collaboration>')
    for pid, _name, lanes, _y, _h in ps:
        pname = f' name="{escape(spec["title"])}"' if pid == "Main" else ""
        x.append(f'  <bpmn:process id="{proc[pid]}"{pname} isExecutable="false">')
        if pid == "Main":
            x.append(f'    <bpmn:laneSet id="LaneSet_{key}">')
            for i, lane in enumerate(lanes):
                x.append(f'      <bpmn:lane id="Lane_{key}_{i}" name="{escape(lane)}">')
                x += [f'        <bpmn:flowNodeRef>{n[0]}</bpmn:flowNodeRef>' for n in spec["nodes"] if n[2] == lane]
                x.append('      </bpmn:lane>')
            x.append('    </bpmn:laneSet>')
        for nid, typ, _lane, _col, label in spec["nodes"]:
            if node_pool[nid] != pid:
                continue
            tag = TAG[typ]
            x.append(f'    <bpmn:{tag} id="{nid}" name="{escape(label)}">')
            x += [f'      <bpmn:incoming>{f[0]}</bpmn:incoming>' for f in seq if f[2] == nid]
            x += [f'      <bpmn:outgoing>{f[0]}</bpmn:outgoing>' for f in seq if f[1] == nid]
            if typ == "timer":
                x.append(f'      <bpmn:timerEventDefinition id="Timer_{nid}" />')
            if typ == "msgstart":
                x.append(f'      <bpmn:messageEventDefinition id="Msg_{nid}" />')
            x.append(f'    </bpmn:{tag}>')
        for fid, src, dst, label in seq:
            if node_pool[src] == pid:
                name = f' name="{escape(label)}"' if label else ""
                x.append(f'    <bpmn:sequenceFlow id="{fid}"{name} sourceRef="{src}" targetRef="{dst}" />')
        x.append('  </bpmn:process>')
    x += [f'  <bpmndi:BPMNDiagram id="Diagram_{key}">',
          f'    <bpmndi:BPMNPlane id="Plane_{key}" bpmnElement="Collaboration_{key}">']
    for pid, _name, lanes, y, h in ps:
        x += [f'      <bpmndi:BPMNShape id="Participant_{key}_{pid}_di" bpmnElement="Participant_{key}_{pid}" isHorizontal="true">',
              f'        <dc:Bounds x="0" y="{y}" width="{width}" height="{h}" />', '      </bpmndi:BPMNShape>']
        if pid == "Main":
            for i, _lane in enumerate(lanes):
                x += [f'      <bpmndi:BPMNShape id="Lane_{key}_{i}_di" bpmnElement="Lane_{key}_{i}" isHorizontal="true">',
                      f'        <dc:Bounds x="{POOL_W}" y="{y + i * LANE_H}" width="{width - POOL_W}" height="{LANE_H}" />',
                      '      </bpmndi:BPMNShape>']
    for nid, typ, *_ in spec["nodes"]:
        bx, by, bw, bh = pos[nid]
        marker = ' isMarkerVisible="true"' if typ == "gw" else ""
        x += [f'      <bpmndi:BPMNShape id="{nid}_di" bpmnElement="{nid}"{marker}>',
              f'        <dc:Bounds x="{bx}" y="{by}" width="{bw}" height="{bh}" />', '      </bpmndi:BPMNShape>']
    edges = [(f, waypoints(pos[f[1]], pos[f[2]], [p for n, p in pos.items() if n not in f[1:3]], types[f[1]] == "gw"))
             for f in seq]
    touch = {}  # phần tử -> các message flow chạm vào, để chia điểm chạm
    for f in msg:
        for n in f[1:3]:
            touch.setdefault(n, []).append(f[0])
    off = {(fid, n): (ids.index(fid) - (len(ids) - 1) / 2) * 36 for n, ids in touch.items() for fid in ids}
    edges += [(f, msg_waypoints(pos[f[1]], pos[f[2]], band_for(ps, pos, f[1], f[2], k),
                                int(off[(f[0], f[1])]), int(off[(f[0], f[2])]))) for k, f in enumerate(msg)]
    for (fid, *_), pts in edges:
        x.append(f'      <bpmndi:BPMNEdge id="{fid}_di" bpmnElement="{fid}">')
        x += [f'        <di:waypoint x="{px}" y="{py}" />' for px, py in pts]
        x.append('      </bpmndi:BPMNEdge>')
    x += ['    </bpmndi:BPMNPlane>', '  </bpmndi:BPMNDiagram>', '</bpmn:definitions>']
    assert all(types[f[1]] != "end" for f in seq), key  # sự kiện kết thúc không có luồng ra
    return "\n".join(x), (width, ps, pos, edges, {f[0] for f in msg})


def font(size, bold=False):
    return ImageFont.truetype("C:/Windows/Fonts/" + ("segoeuib.ttf" if bold else "segoeui.ttf"), size)


def wrap(draw, text, f, maxw):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=f) <= maxw:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    return lines + [cur]


def dashed(d, pts, width, dash, gap):
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        length = abs(x2 - x1) + abs(y2 - y1)
        ux, uy = ((x2 > x1) - (x2 < x1), (y2 > y1) - (y2 < y1))
        p = 0
        while p < length:
            q = min(p + dash, length)
            d.line((x1 + ux * p, y1 + uy * p, x1 + ux * q, y1 + uy * q), fill="black", width=width)
            p = q + gap


def vertical_text(im, text, f, box_w, box_h, x, y):
    """Chữ xoay 90° trong dải tiêu đề pool / lane."""
    tmp = Image.new("RGBA", (box_h, box_w), (0, 0, 0, 0))
    td = ImageDraw.Draw(tmp)
    ls = wrap(td, text, f, box_h - 10)
    for k, line in enumerate(ls):
        td.text((box_h // 2, box_w // 2 + (k - (len(ls) - 1) / 2) * f.size * 1.15), line, font=f, fill="black", anchor="mm")
    rot = tmp.rotate(90, expand=True)
    im.paste(rot, (x, y), rot)


def task_icon(d, typ, x, y, S):
    """Biểu tượng loại task ở góc trên trái như Camunda: người, bánh răng, phong bì đặc (gửi) / rỗng (nhận)."""
    if typ == "user":
        d.ellipse((x + 4 * S, y, x + 10 * S, y + 6 * S), outline="black", width=S)
        d.chord((x + 1 * S, y + 6 * S, x + 13 * S, y + 18 * S), 180, 360, outline="black", width=S)
    elif typ == "service":
        import math
        cx, cy, r = x + 7 * S, y + 7 * S, 6 * S
        for k in range(8):
            a = k * math.pi / 4
            d.line((cx + math.cos(a) * r * 0.6, cy + math.sin(a) * r * 0.6, cx + math.cos(a) * r, cy + math.sin(a) * r),
                   fill="black", width=2 * S)
        d.ellipse((cx - r * 0.65, cy - r * 0.65, cx + r * 0.65, cy + r * 0.65), fill="white", outline="black", width=S)
        d.ellipse((cx - 2 * S, cy - 2 * S, cx + 2 * S, cy + 2 * S), outline="black", width=S)
    elif typ in ("send", "receive"):
        fill = "black" if typ == "send" else "white"
        d.rectangle((x, y + 2 * S, x + 16 * S, y + 13 * S), fill=fill, outline="black", width=S)
        d.line((x, y + 2 * S, x + 8 * S, y + 8 * S, x + 16 * S, y + 2 * S), fill="white" if typ == "send" else "black",
               width=S)


def to_png(key, spec, geo, path):
    width, ps, pos, edges, msg_ids = geo
    S = 2  # vẽ gấp đôi cho nét chữ rõ
    height = ps[-1][3] + ps[-1][4]
    oy = 40
    im = Image.new("RGB", (width * S, (height + oy + 10) * S), "white")
    d = ImageDraw.Draw(im)
    f, fb, fs = font(11 * S), font(12 * S, True), font(10 * S)
    d.text((10 * S, 8 * S), spec["title"], font=font(16 * S, True), fill="black")
    Y = lambda v: (v + oy) * S  # noqa: E731
    for pid, name, lanes, y, h in ps:
        d.rectangle((0, Y(y), width * S - 1, Y(y + h)), outline="black", width=2)
        d.line((POOL_W * S, Y(y), POOL_W * S, Y(y + h)), fill="black", width=2)
        vertical_text(im, name, fb, POOL_W * S, h * S, 0, Y(y))
        if pid == "Main":
            for i, lane in enumerate(lanes):
                ly = y + i * LANE_H
                if i:
                    d.line((POOL_W * S, Y(ly), width * S, Y(ly)), fill="black", width=1)
                d.line(((POOL_W + LANE_W) * S, Y(ly), (POOL_W + LANE_W) * S, Y(ly + LANE_H)), fill="black", width=1)
                vertical_text(im, lane, fs, LANE_W * S, LANE_H * S, POOL_W * S, Y(ly))
    for (fid, _src, _dst, label), wp in edges:
        pts = [(px * S, Y(py)) for px, py in wp]
        is_msg = fid in msg_ids
        if is_msg:
            dashed(d, pts, 2, 9 * S, 5 * S)
            x0, y0 = pts[0]
            d.ellipse((x0 - 4 * S, y0 - 4 * S, x0 + 4 * S, y0 + 4 * S), fill="white", outline="black", width=2)
        else:
            d.line(pts, fill="black", width=2)
        (x1, y1), (x2, y2) = pts[-2], pts[-1]
        ux, uy = (x2 > x1) - (x2 < x1), (y2 > y1) - (y2 < y1)
        a = 9 * S
        tri = [(x2, y2), (x2 - ux * a - uy * a // 2, y2 - uy * a - ux * a // 2),
               (x2 - ux * a + uy * a // 2, y2 - uy * a + ux * a // 2)]
        d.polygon(tri, fill="white" if is_msg else "black", outline="black")
        if label:
            if is_msg:  # nhãn cạnh đoạn dọc đầu tiên
                lx, ly = pts[0][0] + 6 * S, (pts[0][1] + pts[1][1]) // 2
            elif len(pts) == 2:
                lx, ly = pts[0][0] + 6 * S, pts[0][1] - 16 * S
            elif len(pts) == 3:  # nhánh ra từ đỉnh trên/dưới của cổng: nhãn ở chỗ rẽ ngang về đích
                lx, ly = pts[1][0] + 6 * S, pts[1][1] - 16 * S
            else:
                lx, ly = pts[1][0] + 4 * S, (pts[1][1] + pts[2][1]) // 2
            d.text((lx, ly), label, font=fs, fill="black")
    for nid, typ, _lane, _col, label in spec["nodes"]:
        bx, by, bw, bh = pos[nid]
        bx, bw, bh, by = bx * S, bw * S, bh * S, Y(by)
        if typ in EVENTS:
            d.ellipse((bx, by, bx + bw, by + bh), fill="white", outline="black", width=(6 if typ == "end" else 2))
            if typ == "timer":
                d.ellipse((bx + 6 * S, by + 6 * S, bx + bw - 6 * S, by + bh - 6 * S), outline="black", width=S)
            if typ == "msgstart":  # phong bì
                ex, ey = bx + 9 * S, by + 12 * S
                d.rectangle((ex, ey, ex + 18 * S, ey + 12 * S), outline="black", width=S)
                d.line((ex, ey, ex + 9 * S, ey + 7 * S, ex + 18 * S, ey), fill="black", width=S)
            for k, line in enumerate(wrap(d, label, fs, 120 * S)):
                d.text((bx + bw // 2, by + bh + 4 * S + k * 13 * S), line, font=fs, fill="black", anchor="ma")
        elif typ == "gw":
            cx, cy = bx + bw // 2, by + bh // 2
            d.polygon([(cx, by), (bx + bw, cy), (cx, by + bh), (bx, cy)], fill="white", outline="black", width=2)
            d.text((cx, cy), "X", font=fb, fill="black", anchor="mm")
            # Nhãn đặt chỗ không có đường đi qua: trên, nếu có đường ở đỉnh trên thì dưới, nếu cả hai thì bên trái
            ends = {p for (_f, wp) in edges for p in (wp[0], wp[-1])}
            gx, gy0, gy1 = pos[nid][0] + pos[nid][2] // 2, pos[nid][1], pos[nid][1] + pos[nid][3]
            up, down = (gx, gy0) in ends, (gx, gy1) in ends
            ls = wrap(d, label, fs, 150 * S)
            for k, line in enumerate(ls):
                if not up:
                    d.text((cx, by - 6 * S - (len(ls) - k) * 13 * S), line, font=fs, fill="black", anchor="ma")
                elif not down:
                    d.text((cx, by + bh + 4 * S + k * 13 * S), line, font=fs, fill="black", anchor="ma")
                else:
                    d.text((bx - 4 * S, by - 4 * S - (len(ls) - k) * 13 * S), line, font=fs, fill="black", anchor="ra")
        else:
            d.rounded_rectangle((bx, by, bx + bw, by + bh), radius=10 * S, fill="white", outline="black",
                                width=5 if typ == "call" else 2)  # call activity: viền đậm theo BPMN
            task_icon(d, typ, bx + 6 * S, by + 5 * S, S)
            ls = wrap(d, label, f, bw - 12 * S)
            for k, line in enumerate(ls):
                d.text((bx + bw // 2, by + bh // 2 + (k - (len(ls) - 1) / 2) * 14 * S), line, font=f,
                       fill="black", anchor="mm")
    im.save(path, optimize=True)


def main():
    OUT.mkdir(exist_ok=True)
    for key, spec in PROCESSES.items():
        xml, geo = to_bpmn(key, spec)
        (OUT / f"{key}.bpmn").write_text(xml, encoding="utf-8")
        to_png(key, spec, geo, OUT / f"{key}.png")
        print("Đã ghi", key, len(spec["nodes"]), "phần tử,", len(spec["flows"]), "luồng")


if __name__ == "__main__":
    main()
