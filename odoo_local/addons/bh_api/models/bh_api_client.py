import hashlib
import hmac
import secrets
from datetime import timedelta

from odoo import api, fields, models


def _hash(token):
    return hashlib.sha256(token.encode()).hexdigest()


class BhApiClient(models.Model):
    _name = "bh.api.client"
    _description = "Đối tác dùng API"

    name = fields.Char("Tên ứng dụng / đối tác", required=True)
    partner_id = fields.Many2one("res.partner", "Khách hàng", required=True,
                                 help="Dữ liệu trả về (giá, đơn, công nợ) luôn giới hạn theo khách hàng này.")
    user_id = fields.Many2one("res.users", "Chạy dưới quyền người dùng", required=True,
                              default=lambda self: self.env.user,
                              help="API dùng đúng quyền của người dùng này, nên phân quyền Odoo vẫn có hiệu lực.")
    active = fields.Boolean(default=True)
    token_hash = fields.Char(readonly=True, copy=False, groups="base.group_system")
    token_prefix = fields.Char("Đầu token", readonly=True, copy=False, help="8 ký tự đầu, để nhận biết token.")
    expire_date = fields.Date("Hết hạn", default=lambda self: fields.Date.today() + timedelta(days=180))
    scope_stock = fields.Boolean("Xem sản phẩm, giá, tồn", default=True)
    scope_order = fields.Boolean("Tạo và xem đơn hàng")
    scope_debt = fields.Boolean("Xem công nợ")
    rate_limit = fields.Integer("Số lần gọi tối đa / phút", default=60)
    log_ids = fields.One2many("bh.api.log", "client_id", "Nhật ký")
    call_count = fields.Integer("Số lần gọi", compute="_compute_call_count")

    def _compute_call_count(self):
        data = dict(self.env["bh.api.log"]._read_group([("client_id", "in", self.ids)], ["client_id"], ["__count"]))
        for c in self:
            c.call_count = data.get(c, 0)

    def action_generate_token(self):
        """Sinh token mới, chỉ lưu bản băm; token gốc hiện đúng một lần."""
        self.ensure_one()
        token = "bh_" + secrets.token_urlsafe(32)
        self.sudo().write({"token_hash": _hash(token), "token_prefix": token[:8]})
        wizard = self.env["bh.api.token.wizard"].create({"client_id": self.id, "token": token})
        return {
            "type": "ir.actions.act_window",
            "res_model": "bh.api.token.wizard",
            "res_id": wizard.id,
            "view_mode": "form",
            "target": "new",
        }

    def action_revoke(self):
        self.sudo().write({"token_hash": False, "token_prefix": False})

    @api.model
    def _authenticate(self, token):
        if not token:
            return self.browse()
        digest = _hash(token)
        client = self.sudo().search([("token_hash", "=", digest)], limit=1)
        if not client or not hmac.compare_digest(client.token_hash, digest):
            return self.browse()
        if client.expire_date and client.expire_date < fields.Date.today():
            return self.browse()
        return client

    def _over_rate_limit(self):
        self.ensure_one()
        since = fields.Datetime.now() - timedelta(minutes=1)
        recent = self.env["bh.api.log"].sudo().search_count([("client_id", "=", self.id), ("create_date", ">=", since)])
        return recent >= self.rate_limit


class BhApiLog(models.Model):
    _name = "bh.api.log"
    _description = "Nhật ký gọi API"
    _order = "id desc"

    client_id = fields.Many2one("bh.api.client", ondelete="cascade", index=True)
    endpoint = fields.Char()
    method = fields.Char()
    status = fields.Integer()
    ip = fields.Char("IP")
    duration_ms = fields.Integer("Thời gian xử lý (ms)")
