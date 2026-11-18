"""Tạo tools/mau_bao_cao.docx từ báo cáo mẫu IS201 (định dạng chuẩn nhóm dùng): giữ bìa, khung, logo, style,
lề và chân trang số trang; thay chữ trên bìa; bỏ toàn bộ nội dung cũ và ảnh không dùng.

Dùng: python tools/tao_mau_bao_cao.py "../IS201.Q21_24521769_24521776_24521817_24522039.docx"
Kết quả: bìa (section 0) + đoạn rỗng mang section trang đầu (không số trang) + section thân bài (số trang từ 1).
"""
import sys
from copy import deepcopy
from pathlib import Path

from docx import Document
from docx.oxml.ns import qn

OUT = Path(__file__).with_name("mau_bao_cao.docx")
COVER = {  # chỉ số đoạn trên bìa mẫu -> chữ mới (None = giữ)
    6: "HOẠCH ĐỊNH NGUỒN LỰC DOANH NGHIỆP",
    9: "TRIỂN KHAI HỆ THỐNG ERP ODOO 19",
    10: "CHO CÔNG TY TNHH BÁNH BẢO HÂN",
    12: "Nhóm 06 – Sinh viên thực hiện:",
}
NAMES = {13: ("Lê Thị Thanh Tiền", "24521769"), 14: ("Đoàn Thị Thùy Trang", "24521817"),
         15: ("Phạm Tuấn Hải", "24520442")}


def set_text(p, text):
    ts = list(p.iter(qn("w:t")))
    ts[0].text = text
    for t in ts[1:]:
        t.text = ""


def main(src):
    d = Document(src)
    body = d.element.body
    els = list(body)
    secs = [i for i, el in enumerate(els) if el.tag == qn("w:p") and el.find(".//" + qn("w:sectPr")) is not None]
    cover_end = secs[0]
    front_sect = deepcopy(d.sections[2]._sectPr)   # trang đầu: lề thân bài, không số trang
    body_sect = deepcopy(d.sections[6]._sectPr)    # chương 1 trở đi: số trang giữa chân trang, bắt đầu 1

    for i, text in COVER.items():
        set_text(els[i], text)
    for i, (name, mssv) in NAMES.items():
        ts = list(els[i].iter(qn("w:t")))
        ts[0].text, ts[-1].text = name, mssv
        for t in ts[1:-1]:
            t.text = ""
    # Dòng thứ 4 của danh sách tên -> giảng viên hướng dẫn (không gạch đầu dòng), giữ số dòng của bìa
    gv = els[16]
    gv.find(qn("w:pPr")).remove(gv.find(qn("w:pPr")).find(qn("w:numPr")))
    set_text(gv, "Giảng viên hướng dẫn: ThS. Văn Đức Sơn Hà")
    for tab in gv.findall(".//" + qn("w:r") + "/" + qn("w:tab")):
        tab.getparent().remove(tab)
    body.remove(gv)
    els[12].addprevious(gv)

    for el in els[cover_end + 1:]:
        body.remove(el)
    p = deepcopy(els[cover_end])
    for child in list(p):
        p.remove(child)
    ppr = p.makeelement(qn("w:pPr"), {})
    ppr.append(front_sect)
    p.append(ppr)
    body.append(p)
    body.append(body_sect)

    # Tiêu đề: bỏ đánh số tự động của mẫu (markdown đã ghi số "1.1."), bỏ thụt lề treo đi kèm
    for sid in ("Heading 1", "Heading 2", "Heading 3", "Heading 4"):
        ppr = d.styles[sid].element.find(qn("w:pPr"))
        for tag in ("w:numPr", "w:ind"):
            el = ppr.find(qn(tag)) if ppr is not None else None
            if el is not None:
                ppr.remove(el)

    # Bỏ ảnh của báo cáo cũ (giữ ảnh bìa)
    used = set(body.xpath(".//@r:embed | .//@r:id"))
    part = d.part
    for rid, rel in list(part.rels.items()):
        if rel.reltype.endswith("/image") and rid not in used:
            part.drop_rel(rid)
    d.save(OUT)
    print("Đã ghi", OUT, OUT.stat().st_size // 1024, "KB")


if __name__ == "__main__":
    main(sys.argv[1])
