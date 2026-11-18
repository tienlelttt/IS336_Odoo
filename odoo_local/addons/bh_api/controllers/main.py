"""API nghiệp vụ cho đối tác của Bảo Hân.

Xác thực: header  Authorization: Bearer <token>  (token sinh trong Cài đặt > API đối tác).
Mọi phản hồi là JSON. Mã lỗi: 401 sai/thiếu token, 403 không đủ phạm vi, 404, 422 dữ liệu sai, 429 quá tần suất.
"""
import hmac
import json
import time
from functools import wraps

from odoo import fields, http
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.http import request

PREFIX = "/api/bh/v1"


def _json(data, status=200):
    return request.make_json_response(data, status=status)


def api_route(path, scope, methods):
    """Bọc route: xác thực token, kiểm tra phạm vi, giới hạn tần suất, ghi nhật ký."""
    def decorator(func):
        @http.route(PREFIX + path, type="http", auth="public", methods=methods, csrf=False, save_session=False)
        @wraps(func)
        def wrapper(self, **kw):
            start = time.time()
            header = request.httprequest.headers.get("Authorization", "")
            token = header[7:].strip() if header.startswith("Bearer ") else ""
            client = request.env["bh.api.client"]._authenticate(token)
            if not client:
                return _json({"error": "invalid_token"}, 401)
            if not client[scope]:
                resp = _json({"error": "forbidden_scope", "scope": scope}, 403)
            elif client._over_rate_limit():
                resp = _json({"error": "rate_limited"}, 429)
            else:
                try:
                    resp = func(self, client, client.with_user(client.user_id).env, **kw)
                except (UserError, ValidationError) as e:
                    resp = _json({"error": "invalid_request", "message": str(e)}, 422)
                except AccessError:
                    resp = _json({"error": "forbidden"}, 403)
            request.env["bh.api.log"].sudo().create({
                "client_id": client.id,
                "endpoint": request.httprequest.path,
                "method": request.httprequest.method,
                "status": resp.status_code,
                "ip": request.httprequest.remote_addr,
                "duration_ms": int((time.time() - start) * 1000),
            })
            return resp
        return wrapper
    return decorator


def _body():
    try:
        return json.loads(request.httprequest.get_data() or b"{}")
    except ValueError:
        raise UserError("Body phải là JSON hợp lệ.")


class BhApiController(http.Controller):

    @api_route("/products", "scope_stock", ["GET"])
    def products(self, client, env, **kw):
        partner = client.partner_id
        pricelist = partner.property_product_pricelist
        products = env["product.product"].search([("sale_ok", "=", True), ("is_storable", "=", True)])
        return _json({"currency": env.company.currency_id.name, "products": [{
            "default_code": p.default_code,
            "name": p.name,
            "uom": p.uom_id.name,
            "qty_available": p.qty_available,
            "price": pricelist._get_product_price(p, 1.0) if pricelist else p.lst_price,
        } for p in products]})

    @api_route("/orders", "scope_order", ["POST"])
    def create_order(self, client, env, **kw):
        data = _body()
        lines = data.get("lines") or []
        if not lines:
            raise UserError("Đơn hàng cần ít nhất một dòng.")
        Product = env["product.product"]
        order_lines = []
        for line in lines:
            product = Product.search([("default_code", "=", line.get("default_code")), ("sale_ok", "=", True)], limit=1)
            qty = float(line.get("qty") or 0)
            if not product or qty <= 0:
                raise UserError(f"Dòng không hợp lệ: {line}")
            order_lines.append((0, 0, {"product_id": product.id, "product_uom_qty": qty}))
        order = env["sale.order"].create({
            "partner_id": client.partner_id.id,
            "client_order_ref": data.get("client_ref"),
            "note": data.get("note"),
            "order_line": order_lines,
        })
        return _json(self._order_dict(order), 201)

    @api_route("/orders/<string:name>", "scope_order", ["GET"])
    def get_order(self, client, env, name, **kw):
        order = env["sale.order"].search(
            [("name", "=", name), ("partner_id", "child_of", client.partner_id.commercial_partner_id.id)], limit=1)
        if not order:
            return _json({"error": "not_found"}, 404)
        return _json(self._order_dict(order))

    @api_route("/debt", "scope_debt", ["GET"])
    def debt(self, client, env, **kw):
        invoices = env["account.move"].search([
            ("move_type", "=", "out_invoice"), ("state", "=", "posted"),
            ("partner_id", "child_of", client.partner_id.commercial_partner_id.id),
            ("payment_state", "in", ("not_paid", "partial"))], order="invoice_date_due")
        today = fields.Date.today()
        return _json({
            "total_due": sum(invoices.mapped("amount_residual")),
            "overdue": sum(i.amount_residual for i in invoices if i.invoice_date_due and i.invoice_date_due < today),
            "invoices": [{"name": i.name, "date": str(i.invoice_date), "due": str(i.invoice_date_due),
                          "total": i.amount_total, "residual": i.amount_residual} for i in invoices],
        })

    @staticmethod
    def _order_dict(order):
        return {"name": order.name, "state": order.state, "amount_total": order.amount_total,
                "lines": [{"default_code": l.product_id.default_code, "qty": l.product_uom_qty,
                           "price_unit": l.price_unit} for l in order.order_line]}

    @http.route(PREFIX + "/webhook/bank", type="http", auth="public", methods=["POST"], csrf=False, save_session=False)
    def bank_webhook(self, **kw):
        """Nhận biến động số dư (kiểu SePay). Xác thực bằng header Authorization: Apikey <secret>."""
        secret = request.env["ir.config_parameter"].sudo().get_param("bh_api.bank_webhook_secret")
        given = request.httprequest.headers.get("Authorization", "").removeprefix("Apikey ").strip()
        if not secret or not hmac.compare_digest(secret, given):
            return _json({"success": False, "error": "unauthorized"}, 401)
        try:
            payload = _body()
        except UserError:
            return _json({"success": False, "error": "invalid_json"}, 422)
        if payload.get("transferType", "in") != "in":
            return _json({"success": True, "ignored": "outgoing"})
        txn = request.env["bh.bank.txn"].sudo()._process(payload)
        return _json({"success": True, "state": txn.state, "invoice": txn.move_id.name or None})
