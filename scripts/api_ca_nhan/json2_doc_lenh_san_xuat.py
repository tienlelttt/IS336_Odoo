"""API cá nhân (thành viên B): JSON-2 API của Odoo 19 – đọc lệnh sản xuất và lô thành phẩm cho báo cáo xưởng.

Lấy API key: Odoo > avatar > Tùy chọn của tôi > Bảo mật tài khoản > Khóa API mới (chọn hạn dùng).
Chạy: ODOO_API_KEY=<key> python scripts/api_ca_nhan/json2_doc_lenh_san_xuat.py
JSON-2: POST /json/2/<model>/<method>, header Authorization: bearer <API key>, body là tham số dạng tên.
"""
import json
import os

import requests

BASE = os.environ.get("ODOO_URL", "http://localhost:8069")
H = {"Authorization": f"bearer {os.environ['ODOO_API_KEY']}", "Content-Type": "application/json",
     "X-Odoo-Database": os.environ.get("ODOO_DB", "baohan")}


def call(model, method, **kw):
    r = requests.post(f"{BASE}/json/2/{model}/{method}", headers=H, data=json.dumps(kw), timeout=15)
    r.raise_for_status()
    return r.json()


mos = call("mrp.production", "search_read", domain=[["state", "=", "done"]],
           fields=["name", "product_id", "product_qty", "qty_produced", "date_finished"], order="id")
print("Lệnh sản xuất đã xong:")
for m in mos:
    note = "  (làm thiếu)" if m["qty_produced"] < m["product_qty"] else ""
    print(f"  {m['name']}  {m['product_id'][1]:<40} kế hoạch {m['product_qty']:>5.0f}  thực tế {m['qty_produced']:>5.0f}{note}")
lots = call("stock.lot", "search_read", domain=[["product_id.default_code", "=like", "FG%"], ["bh_stage", "!=", "normal"]],
            fields=["name", "product_id", "expiration_date", "bh_stage", "bh_remaining_pct"])
print("Lô thành phẩm đang ở mức cận hạn:")
for l in lots:
    print(f"  {l['name']:<14} {l['bh_stage']:<9} còn {l['bh_remaining_pct']:>5}%  hạn {l['expiration_date']}")
