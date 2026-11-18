import json

from odoo.tests import HttpCase, tagged


@tagged("post_install", "-at_install")
class TestBhApi(HttpCase):

    def setUp(self):
        super().setUp()
        self.partner = self.env["res.partner"].create({"name": "Quán Cà Phê Test"})
        self.product = self.env["product.product"].create({
            "name": "Bánh mì sandwich test", "default_code": "BM-TEST", "is_storable": True,
            "sale_ok": True, "list_price": 25000})
        self.client = self.env["bh.api.client"].create({
            "name": "App đặt hàng", "partner_id": self.partner.id, "user_id": self.env.ref("base.user_admin").id,
            "scope_stock": True, "scope_order": True, "scope_debt": False, "rate_limit": 100})
        wiz = self.env["bh.api.token.wizard"].browse(self.client.action_generate_token()["res_id"])
        self.headers = {"Authorization": f"Bearer {wiz.token}", "Content-Type": "application/json"}

    def _get(self, path, headers=None):
        return self.url_open("/api/bh/v1" + path, headers=headers if headers is not None else self.headers)

    def test_auth_required(self):
        self.assertEqual(self._get("/products", headers={}).status_code, 401)
        self.assertEqual(self._get("/products", headers={"Authorization": "Bearer sai"}).status_code, 401)
        self.assertFalse(self.client.log_ids, "Token sai không được ghi nhật ký vào client")

    def test_token_hashed_not_plain(self):
        self.assertEqual(len(self.client.sudo().token_hash), 64)
        self.assertNotIn(self.client.sudo().token_hash, self.headers["Authorization"])

    def test_products_and_log(self):
        resp = self._get("/products")
        self.assertEqual(resp.status_code, 200)
        codes = [p["default_code"] for p in resp.json()["products"]]
        self.assertIn("BM-TEST", codes)
        self.assertEqual(self.client.log_ids[:1].status, 200)

    def test_scope_forbidden(self):
        self.assertEqual(self._get("/debt").status_code, 403)

    def test_create_and_read_order(self):
        body = json.dumps({"client_ref": "PO-01", "lines": [{"default_code": "BM-TEST", "qty": 40}]})
        resp = self.url_open("/api/bh/v1/orders", data=body, headers=self.headers)
        self.assertEqual(resp.status_code, 201, resp.text)
        name = resp.json()["name"]
        order = self.env["sale.order"].search([("name", "=", name)])
        self.assertEqual(order.partner_id, self.partner)
        self.assertEqual(order.order_line.product_uom_qty, 40)
        self.assertEqual(self._get(f"/orders/{name}").json()["name"], name)

    def test_invalid_order_rejected(self):
        body = json.dumps({"lines": [{"default_code": "KHONG-CO", "qty": 1}]})
        self.assertEqual(self.url_open("/api/bh/v1/orders", data=body, headers=self.headers).status_code, 422)

    def test_other_partner_order_hidden(self):
        other = self.env["sale.order"].create({
            "partner_id": self.env["res.partner"].create({"name": "Khách khác"}).id,
            "order_line": [(0, 0, {"product_id": self.product.id, "product_uom_qty": 1})]})
        self.assertEqual(self._get(f"/orders/{other.name}").status_code, 404)

    def test_rate_limit(self):
        self.client.rate_limit = 2
        self._get("/products")
        self._get("/products")
        self.assertEqual(self._get("/products").status_code, 429)

    def test_expired_token(self):
        self.client.expire_date = "2000-01-01"
        self.assertEqual(self._get("/products").status_code, 401)
