"""Xuất master data ra file Excel/CSV đúng định dạng import của Odoo 19 (cột = tên kỹ thuật của trường).
Chạy: python scripts/export_import_files.py  → ghi vào thư mục data/
"""
import csv
import sys
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

sys.path.insert(0, str(Path(__file__).parent))
from seed_data import CUSTOMERS, FINISHED, RAW, ROUTES, VENDOR_LEAD_DAYS, VENDORS  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "data"
OUT.mkdir(exist_ok=True)
UOM = {"kg": "kg", "L": "L", "Đơn vị": "Đơn vị"}
vendor_name = dict(VENDORS)

sheets = {
    "san_pham_thanh_pham": (
        ["default_code", "name", "categ_id", "is_storable", "list_price", "tracking", "use_expiration_date",
         "expiration_time", "sale_ok", "purchase_ok"],
        [[c, n, f"Thành phẩm / {cat}", True, price, "lot", True, days, True, False]
         for c, n, cat, price, days, _web in FINISHED]),
    "nguyen_vat_lieu": (
        ["default_code", "name", "categ_id", "is_storable", "uom_id", "standard_price", "tracking",
         "use_expiration_date", "expiration_time", "sale_ok", "purchase_ok",
         "seller_ids/partner_id", "seller_ids/price", "seller_ids/delay"],
        [[c, n, (f"Nguyên vật liệu / {cat}" if cat.startswith("NVL") else cat), True, UOM[u], cost,
          "lot" if days else "none", bool(days), days, False, True, vendor_name[v], cost, VENDOR_LEAD_DAYS[v]]
         for c, n, cat, u, cost, days, v, _mn, _mx in RAW]),
    "khach_hang": (
        ["ref", "name", "is_company", "city", "property_product_pricelist", "property_payment_term_id",
         "use_partner_credit_limit", "credit_limit", "category_id"],
        [[c, n, True, "TP. Hồ Chí Minh", pl, "30 ngày" if t == "30" else "Thanh toán ngay", bool(lim), lim,
          ROUTES[r] + (",Trả tiền mặt cho tài xế" if cod else "")]
         for c, n, pl, t, lim, r, cod in CUSTOMERS]),
    "nha_cung_cap": (
        ["ref", "name", "is_company", "supplier_rank"],
        [[c, n, True, 1] for c, n in VENDORS]),
}

wb = Workbook()
wb.remove(wb.active)
head_font = Font(bold=True, color="FFFFFF")
head_fill = PatternFill("solid", fgColor="A84B16")
for name, (cols, rows) in sheets.items():
    ws = wb.create_sheet(name[:31])
    ws.append(cols)
    for cell in ws[1]:
        cell.font, cell.fill = head_font, head_fill
    for r in rows:
        ws.append(r)
    for col in ws.columns:
        ws.column_dimensions[col[0].column_letter].width = max(12, min(45, max(len(str(c.value)) for c in col) + 2))
    with open(OUT / f"{name}.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(cols)
        w.writerows(rows)
wb.save(OUT / "master_data_bao_han.xlsx")
print("Đã ghi:", ", ".join(sorted(p.name for p in OUT.iterdir())))
