"""API cá nhân (Đoàn Thị Thùy Trang): XML-RPC – hệ thống ngoài tạo yêu cầu báo giá (RFQ) gửi nhà cung cấp.

Chạy: ODOO_USER=admin ODOO_API_KEY=<key hoặc mật khẩu> python scripts/api_ca_nhan/xmlrpc_tao_don_mua.py
Bước: /xmlrpc/2/common authenticate → uid; /xmlrpc/2/object execute_kw(model, method, args, kwargs).
"""
import os
import xmlrpc.client

URL = os.environ.get("ODOO_URL", "http://localhost:8069")
DB = os.environ.get("ODOO_DB", "baohan")
USER = os.environ.get("ODOO_USER", "admin")
KEY = os.environ["ODOO_API_KEY"]

common = xmlrpc.client.ServerProxy(f"{URL}/xmlrpc/2/common")
print("Phiên bản:", common.version()["server_version"])
uid = common.authenticate(DB, USER, KEY, {})
models = xmlrpc.client.ServerProxy(f"{URL}/xmlrpc/2/object")


def x(model, method, *args, **kw):
    return models.execute_kw(DB, uid, KEY, model, method, list(args), kw)


vendor = x("res.partner", "search", [["ref", "=", "NCC05"]], limit=1)[0]
products = {p["default_code"]: p["id"] for p in x("product.product", "search_read", [["default_code", "in", ["RM12", "RM13"]]],
                                                 fields=["default_code"])}
po_id = x("purchase.order", "create", {
    "partner_id": vendor, "origin": "Tạo qua XML-RPC",
    "order_line": [[0, 0, {"product_id": products["RM12"], "product_qty": 15}],
                   [0, 0, {"product_id": products["RM13"], "product_qty": 10}]]})
po = x("purchase.order", "read", [po_id], fields=["name", "state", "amount_total"])[0]
print(f"Đã tạo {po['name']} trạng thái {po['state']} tổng {po['amount_total']:,.0f} VND")
