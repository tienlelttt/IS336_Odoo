"""Sinh file BPMN 2.0 (có DI, mở được bằng Camunda Modeler desktop) và ảnh PNG xem trước từ cùng một đặc tả.

Dùng: python tools/bpmn_gen.py   → ghi bpmn/<tên>.bpmn và bpmn/<tên>.png
Ảnh PNG chỉ để xem nhanh; ảnh nộp bài nên xuất từ Camunda Modeler (File > Export as image) theo yêu cầu môn học.
"""
import sys
from pathlib import Path
from xml.sax.saxutils import escape

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).parent))
from bpmn_specs import PROCESSES  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "bpmn"
COL_W, LANE_H, LANE_LABEL_W, X0 = 170, 150, 40, 60
SIZES = {"start": (36, 36), "timer": (36, 36), "end": (36, 36), "gw": (50, 50),
         "task": (130, 80), "user": (130, 80), "service": (130, 80), "send": (130, 80), "receive": (130, 80), "call": (130, 80)}
TAG = {"start": "startEvent", "timer": "startEvent", "end": "endEvent", "gw": "exclusiveGateway",
       "task": "task", "user": "userTask", "service": "serviceTask", "send": "sendTask", "receive": "receiveTask",
       "call": "callActivity"}


def layout(spec):
    lanes = spec["lanes"]
    ncol = max(n[3] for n in spec["nodes"]) + 1
    width = LANE_LABEL_W + X0 + ncol * COL_W + 40
    pos = {}
    for nid, typ, lane, col, _label in spec["nodes"]:
        w, h = SIZES[typ]
        cx = LANE_LABEL_W + X0 + col * COL_W + COL_W // 2
        cy = lanes.index(lane) * LANE_H + LANE_H // 2
        pos[nid] = (cx - w // 2, cy - h // 2, w, h)
    return width, len(lanes) * LANE_H, pos


def waypoints(a, b):
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    if bx > ax:  # đi tới
        s, t = (ax + aw, ay + ah // 2), (bx, by + bh // 2)
        if s[1] == t[1]:
            return [s, t]
        mx = (s[0] + t[0]) // 2
        return [s, (mx, s[1]), (mx, t[1]), t]
    # quay lui: đi vòng phía trên hai nút
    top = min(ay, by) - 22
    return [(ax + aw // 2, ay), (ax + aw // 2, top), (bx + bw // 2, top), (bx + bw // 2, by)]


def to_bpmn(key, spec):
    width, height, pos = layout(spec)
    pid, cid = f"Process_{key}", f"Participant_{key}"
    types = {n[0]: n[1] for n in spec["nodes"]}
    x = ['<?xml version="1.0" encoding="UTF-8"?>',
         '<bpmn:definitions xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL" '
         'xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI" xmlns:dc="http://www.omg.org/spec/DD/20100524/DC" '
         'xmlns:di="http://www.omg.org/spec/DD/20100524/DI" xmlns:modeler="http://camunda.org/schema/modeler/1.0" '
         f'id="Definitions_{key}" targetNamespace="http://bpmn.io/schema/bpmn" exporter="Camunda Modeler" '
         'exporterVersion="5.0.0" modeler:executionPlatform="Camunda Platform" modeler:executionPlatformVersion="7.20.0">',
         f'  <bpmn:collaboration id="Collaboration_{key}">',
         f'    <bpmn:participant id="{cid}" name="{escape(spec["title"])}" processRef="{pid}" />',
         '  </bpmn:collaboration>',
         f'  <bpmn:process id="{pid}" isExecutable="false">',
         f'    <bpmn:laneSet id="LaneSet_{key}">']
    for i, lane in enumerate(spec["lanes"]):
        x.append(f'      <bpmn:lane id="Lane_{key}_{i}" name="{escape(lane)}">')
        x += [f'        <bpmn:flowNodeRef>{n[0]}</bpmn:flowNodeRef>' for n in spec["nodes"] if n[2] == lane]
        x.append('      </bpmn:lane>')
    x.append('    </bpmn:laneSet>')
    flows = [(f"Flow_{key}_{i}", *f) for i, f in enumerate(spec["flows"])]
    for nid, typ, _lane, _col, label in spec["nodes"]:
        tag = TAG[typ]
        inc = [f'      <bpmn:incoming>{f[0]}</bpmn:incoming>' for f in flows if f[2] == nid]
        out = [f'      <bpmn:outgoing>{f[0]}</bpmn:outgoing>' for f in flows if f[1] == nid]
        x.append(f'    <bpmn:{tag} id="{nid}" name="{escape(label)}">')
        x += inc + out
        if typ == "timer":
            x.append(f'      <bpmn:timerEventDefinition id="Timer_{nid}" />')
        x.append(f'    </bpmn:{tag}>')
    for fid, src, dst, label in flows:
        assert src in types and dst in types, (key, src, dst)
        name = f' name="{escape(label)}"' if label else ""
        x.append(f'    <bpmn:sequenceFlow id="{fid}"{name} sourceRef="{src}" targetRef="{dst}" />')
    x += ['  </bpmn:process>', f'  <bpmndi:BPMNDiagram id="Diagram_{key}">',
          f'    <bpmndi:BPMNPlane id="Plane_{key}" bpmnElement="Collaboration_{key}">',
          f'      <bpmndi:BPMNShape id="{cid}_di" bpmnElement="{cid}" isHorizontal="true">',
          f'        <dc:Bounds x="0" y="0" width="{width}" height="{height}" />',
          '      </bpmndi:BPMNShape>']
    for i, _lane in enumerate(spec["lanes"]):
        x += [f'      <bpmndi:BPMNShape id="Lane_{key}_{i}_di" bpmnElement="Lane_{key}_{i}" isHorizontal="true">',
              f'        <dc:Bounds x="{LANE_LABEL_W}" y="{i * LANE_H}" width="{width - LANE_LABEL_W}" height="{LANE_H}" />',
              '      </bpmndi:BPMNShape>']
    for nid, typ, *_ in spec["nodes"]:
        bx, by, bw, bh = pos[nid]
        marker = ' isMarkerVisible="true"' if typ == "gw" else ""
        x += [f'      <bpmndi:BPMNShape id="{nid}_di" bpmnElement="{nid}"{marker}>',
              f'        <dc:Bounds x="{bx}" y="{by}" width="{bw}" height="{bh}" />',
              '      </bpmndi:BPMNShape>']
    for fid, src, dst, _label in flows:
        x.append(f'      <bpmndi:BPMNEdge id="{fid}_di" bpmnElement="{fid}">')
        x += [f'        <di:waypoint x="{px}" y="{py}" />' for px, py in waypoints(pos[src], pos[dst])]
        x.append('      </bpmndi:BPMNEdge>')
    x += ['    </bpmndi:BPMNPlane>', '  </bpmndi:BPMNDiagram>', '</bpmn:definitions>']
    return "\n".join(x), (width, height, pos, flows)


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


def to_png(key, spec, geo, path):
    width, height, pos, flows = geo
    S = 2  # vẽ gấp đôi cho nét chữ rõ
    im = Image.new("RGB", (width * S, (height + 40) * S), "white")
    d = ImageDraw.Draw(im)
    f, fb, fs = font(11 * S), font(12 * S, True), font(10 * S)
    oy = 40 * S
    d.text((10 * S, 8 * S), spec["title"], font=font(16 * S, True), fill="#2E1F18")
    d.rectangle((0, oy, width * S - 1, oy + height * S - 1), outline="#2E1F18", width=2)
    for i, lane in enumerate(spec["lanes"]):
        y = oy + i * LANE_H * S
        d.rectangle((0, y, LANE_LABEL_W * S, y + LANE_H * S), fill="#F3E9DD", outline="#2E1F18", width=1)
        d.line((LANE_LABEL_W * S, y, width * S, y), fill="#2E1F18", width=1)
        tmp = Image.new("RGBA", (LANE_H * S, LANE_LABEL_W * S), (0, 0, 0, 0))
        td = ImageDraw.Draw(tmp)
        ls = wrap(td, lane, fb, LANE_H * S - 10)
        for k, line in enumerate(ls):
            td.text((LANE_H * S // 2, LANE_LABEL_W * S // 2 + (k - (len(ls) - 1) / 2) * 15 * S), line,
                    font=fb, fill="#2E1F18", anchor="mm")
        im.paste(tmp.rotate(90, expand=True), (0, y), tmp.rotate(90, expand=True))
    for fid, src, dst, label in flows:
        pts = [(px * S, oy + py * S) for px, py in waypoints(pos[src], pos[dst])]
        d.line(pts, fill="#444444", width=2)
        (x1, y1), (x2, y2) = pts[-2], pts[-1]
        ux, uy = (x2 > x1) - (x2 < x1), (y2 > y1) - (y2 < y1)
        a = 9 * S
        d.polygon([(x2, y2), (x2 - ux * a - uy * a // 2, y2 - uy * a - ux * a // 2),
                   (x2 - ux * a + uy * a // 2, y2 - uy * a + ux * a // 2)], fill="#444444")
        if label:
            lx, ly = pts[0][0] + 6 * S, pts[0][1] - 16 * S if len(pts) == 2 else (pts[1][1] + pts[2][1]) // 2
            if len(pts) > 2:
                lx = pts[1][0] + 4 * S
            d.text((lx, ly), label, font=fs, fill="#A84B16")
    for nid, typ, _lane, _col, label in spec["nodes"]:
        bx, by, bw, bh = [v * S for v in pos[nid]]
        by += oy
        if typ in ("start", "timer", "end"):
            d.ellipse((bx, by, bx + bw, by + bh), fill="white", outline="#2E1F18", width=(5 if typ == "end" else 2) * S // 2)
            if typ == "timer":
                d.ellipse((bx + 6 * S, by + 6 * S, bx + bw - 6 * S, by + bh - 6 * S), outline="#2E1F18", width=S)
            ls = wrap(d, label, fs, 120 * S)
            for k, line in enumerate(ls):
                d.text((bx + bw // 2, by + bh + 4 * S + k * 13 * S), line, font=fs, fill="#2E1F18", anchor="ma")
        elif typ == "gw":
            cx, cy = bx + bw // 2, by + bh // 2
            d.polygon([(cx, by), (bx + bw, cy), (cx, by + bh), (bx, cy)], fill="#FFF8E7", outline="#2E1F18")
            d.text((cx, cy), "X", font=fb, fill="#2E1F18", anchor="mm")
            ls = wrap(d, label, fs, 150 * S)
            for k, line in enumerate(ls):
                d.text((cx, by - 6 * S - (len(ls) - k) * 13 * S), line, font=fs, fill="#2E1F18", anchor="ma")
        else:
            fill = {"service": "#E8F0E8", "send": "#FDEFE3", "receive": "#FDEFE3"}.get(typ, "#FFFFFF")
            d.rounded_rectangle((bx, by, bx + bw, by + bh), radius=10 * S, fill=fill, outline="#2E1F18",
                                width=5 if typ == "call" else 2)  # call activity: viền đậm theo BPMN
            tag = {"user": "Người", "service": "Hệ thống", "send": "Gửi", "receive": "Nhận", "call": "Quy trình con"}.get(typ)
            if tag:
                d.text((bx + 5 * S, by + 3 * S), tag, font=font(8 * S), fill="#6B5A50")
            ls = wrap(d, label, f, bw - 12 * S)
            for k, line in enumerate(ls):
                d.text((bx + bw // 2, by + bh // 2 + (k - (len(ls) - 1) / 2) * 14 * S), line, font=f,
                       fill="#2E1F18", anchor="mm")
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
