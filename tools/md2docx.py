"""Dựng báo cáo .docx từ các file markdown trên mẫu tools/mau_bao_cao.docx (bìa, lề, style của báo cáo mẫu IS201;
tạo lại mẫu bằng tools/tao_mau_bao_cao.py).

Hỗ trợ: # / ## / ### tiêu đề (vào Heading 1–3 → mục lục tự động), đoạn văn, danh sách '-' và '1.', bảng '|...|',
**đậm**, ![chú thích](ảnh.png), khối ``` code ```, dòng '^^' căn giữa (trang bìa),
[[TOC]] mục lục, [[DM_HINH]] danh mục hình (Word cập nhật khi mở file), [[PAGEBREAK]] ngắt trang,
[[SECTION]] hết phần đầu (không số trang) – chương sau bắt đầu trang 1.
Dùng: python tools/md2docx.py out.docx in1.md [in2.md ...]
"""
import os
import re
import sys
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

TEMPLATE = Path(__file__).with_name("mau_bao_cao.docx")
FRONT_SECT = []  # đoạn mang section phần đầu, lấy từ mẫu


def add_runs(par, text, size=None):
    for i, part in enumerate(re.split(r"\*\*(.+?)\*\*", text)):
        if part:
            run = par.add_run(part)
            run.bold = bool(i % 2) or None
            run.font.name = "Times New Roman"
            if size:
                run.font.size = Pt(size)


def set_borders(table):
    borders = OxmlElement("w:tblBorders")
    for side in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement(f"w:{side}")
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), "4")
        el.set(qn("w:color"), "808080")
        borders.append(el)
    table._tbl.tblPr.append(borders)


def shade(cell, hex_fill):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_fill)
    tc_pr.append(shd)


def add_table(doc, rows):
    cells = [[c.strip() for c in re.split(r"(?<!\\)\|", r.strip().strip("|"))] for r in rows]
    cells = [r for r in cells if not all(re.fullmatch(r":?-+:?", c) for c in r if c)]
    ncol = max(len(r) for r in cells)
    table = doc.add_table(rows=len(cells), cols=ncol)
    set_borders(table)
    for i, r in enumerate(cells):
        for j in range(ncol):
            cell = table.cell(i, j)
            par = cell.paragraphs[0]
            add_runs(par, r[j] if j < len(r) else "", size=11)
            if i == 0:
                shade(cell, "F3E9DD")
                for run in par.runs:
                    run.bold = True
    doc.add_paragraph()


def add_field(paragraph, instr, hint_text="Nhấn chuột phải vào đây → Update Field nếu mục lục chưa hiện."):
    """Chèn trường Word (ví dụ mục lục) – Word tính lại khi mở file."""
    run = paragraph.add_run()
    for tag, attrs in (("w:fldChar", {"w:fldCharType": "begin"}),):
        el = OxmlElement(tag)
        for k, v in attrs.items():
            el.set(qn(k), v)
        run._r.append(el)
    instr_el = OxmlElement("w:instrText")
    instr_el.set(qn("xml:space"), "preserve")
    instr_el.text = instr
    run._r.append(instr_el)
    sep = OxmlElement("w:fldChar")
    sep.set(qn("w:fldCharType"), "separate")
    run._r.append(sep)
    hint = paragraph.add_run(hint_text)
    hint.italic = True
    end_run = paragraph.add_run()
    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")
    end_run._r.append(end)


def convert(md_text, doc, base_dir):
    lines = md_text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        if not line:
            i += 1
            continue
        if line.startswith("```"):
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                p = doc.add_paragraph()
                run = p.add_run(lines[i])
                run.font.name = "Consolas"
                run.font.size = Pt(10)
                p.paragraph_format.space_after = Pt(0)
                i += 1
            i += 1
            doc.add_paragraph()
            continue
        if line.startswith("|"):
            block = []
            while i < len(lines) and lines[i].startswith("|"):
                block.append(lines[i])
                i += 1
            add_table(doc, block)
            continue
        if line == "[[PAGEBREAK]]":
            doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
        elif line == "[[TOC]]":
            add_field(doc.add_paragraph(), 'TOC \\o "1-3" \\h \\z \\u')
        elif line == "[[DM_HINH]]":
            add_field(doc.add_paragraph(), 'TOC \\h \\z \\t "Caption,1"',
                      "Nhấn chuột phải vào đây → Update Field nếu danh mục hình chưa hiện.")
        elif line == "[[SECTION]]":
            doc.element.body[-1].addprevious(FRONT_SECT.pop())
        elif line.startswith("^^"):
            p = doc.add_paragraph()
            add_runs(p, line[2:], size=14)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        elif m := re.match(r"(#{1,4}) (.+)", line):
            level = len(m.group(1))
            p = doc.add_paragraph(style=f"Heading {min(level, 3)}")
            add_runs(p, m.group(2))
            if level == 1:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        elif img := re.match(r"!\[(.*)\]\((.+)\)", line):
            path = (base_dir / img.group(2)).resolve()
            if path.exists():
                doc.add_picture(str(path), width=Cm(16))
                doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                doc.add_paragraph(f"[THIẾU HÌNH: {img.group(2)}]")
            cap = doc.add_paragraph(style="Caption")
            add_runs(cap, img.group(1), size=11)
            for run in cap.runs:
                run.italic = True
            cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        elif re.match(r"(- |\d+\. )", line):
            p = doc.add_paragraph(style="List Paragraph")
            add_runs(p, re.sub(r"^- ", "• ", line))
        else:
            p = doc.add_paragraph(style="Normal")
            add_runs(p, line)
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        i += 1


def main(out, *inputs):
    doc = Document(str(TEMPLATE))
    body = doc.element.body
    # Mẫu: bìa (giữ) + đoạn mang section phần đầu (chèn lại ở [[SECTION]]) + section thân bài (cuối body)
    sect_ps = [el for el in body if el.tag == qn("w:p") and el.find(".//" + qn("w:sectPr")) is not None]
    FRONT_SECT.append(sect_ps[1])
    body.remove(sect_ps[1])
    for k, f in enumerate(inputs):
        text = Path(f).read_text(encoding="utf-8")
        # Mỗi chương (file bắt đầu bằng "# ") sang trang mới
        after_section = body[-2].find(".//" + qn("w:sectPr")) is not None  # ngắt section đã sang trang
        if k and text.lstrip().startswith("# ") and not after_section:
            doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
        convert(text, doc, Path(f).parent)
    for p in doc.paragraphs:
        for run in p.runs:
            if run.font.name != "Consolas":
                run.font.name = "Times New Roman"
                run._element.get_or_add_rPr().get_or_add_rFonts().set(qn("w:eastAsia"), "Times New Roman")
    # Yêu cầu Word cập nhật trường (mục lục) khi mở file
    if not os.environ.get("NO_UPDATE_FIELDS"):  # khi tự động hóa bằng Word COM thì bỏ để không hiện hộp thoại
        settings = doc.settings.element
        upd = OxmlElement("w:updateFields")
        upd.set(qn("w:val"), "true")
        settings.append(upd)
    doc.save(out)
    print("Đã ghi", out)


if __name__ == "__main__":
    main(*sys.argv[1:])
