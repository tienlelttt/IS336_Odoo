"""Gọi thử Module API bh_api và webhook ngân hàng từ hệ thống bên ngoài (máy của khách / cổng ngân hàng).

Chạy:
  BH_API_TOKEN=<token> python scripts/api_demo_calls.py [invoice_name]
Token lấy ở Odoo: Thiết lập > API & Tích hợp > API đối tác > Sinh token mới (chỉ hiện một lần).
"""
import json
import os
import sys

import requests

BASE = os.environ.get("BH_BASE_URL", "http://localhost:8069")
TOKEN = os.environ["BH_API_TOKEN"]
BANK_SECRET = os.environ.get("BH_BANK_SECRET", "bh-local-webhook-secret")
H = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}


def show(title, resp):
    print(f"\n=== {title} → HTTP {resp.status_code}")
    print(json.dumps(resp.json(), ensure_ascii=False, indent=2)[:1200])
    return resp


# 1. Không có token → 401
show("GET /products không token", requests.get(f"{BASE}/api/bh/v1/products", timeout=10))

# 2. Danh mục, giá theo bảng giá của khách, tồn kho
show("GET /products", requests.get(f"{BASE}/api/bh/v1/products", headers=H, timeout=10))

# 3. Tạo đơn hàng từ app đặt hàng của chuỗi trà sữa
order = show("POST /orders", requests.post(f"{BASE}/api/bh/v1/orders", headers=H, timeout=10, data=json.dumps({
    "client_ref": "APP-LAXANH-0001",
    "note": "Giao trước 7h sáng",
    "lines": [{"default_code": "FG06", "qty": 4}, {"default_code": "FG08", "qty": 20}],
})))

# 4. Xem lại đơn vừa tạo
if order.status_code == 201:
    show("GET /orders/<số đơn>", requests.get(f"{BASE}/api/bh/v1/orders/{order.json()['name']}", headers=H, timeout=10))

# 5. Dữ liệu sai → 422
show("POST /orders sai mã hàng", requests.post(f"{BASE}/api/bh/v1/orders", headers=H, timeout=10,
                                              data=json.dumps({"lines": [{"default_code": "XYZ", "qty": 1}]})))

# 6. Công nợ của khách
show("GET /debt", requests.get(f"{BASE}/api/bh/v1/debt", headers=H, timeout=10))

# 7. Webhook ngân hàng (định dạng kiểu SePay): khách chuyển khoản, nội dung có số hóa đơn
if len(sys.argv) > 1:
    inv, amount = sys.argv[1], float(sys.argv[2])
    payload = {"id": 880001, "gateway": "Vietcombank", "transactionDate": "2026-11-18 09:15:00",
               "accountNumber": "0000000000", "transferType": "in", "transferAmount": amount,
               "content": f"SAO MAI TT {inv.replace('/', '')}", "referenceCode": "FT26322880001"}
    hb = {"Authorization": f"Apikey {BANK_SECRET}", "Content-Type": "application/json"}
    show("POST /webhook/bank sai secret", requests.post(f"{BASE}/api/bh/v1/webhook/bank", timeout=10,
                                                        headers={**hb, "Authorization": "Apikey sai"},
                                                        data=json.dumps(payload)))
    show("POST /webhook/bank", requests.post(f"{BASE}/api/bh/v1/webhook/bank", headers=hb, timeout=10,
                                             data=json.dumps(payload)))
    show("POST /webhook/bank gửi lại (trùng)", requests.post(f"{BASE}/api/bh/v1/webhook/bank", headers=hb,
                                                             timeout=10, data=json.dumps(payload)))
