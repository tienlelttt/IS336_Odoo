from odoo import api, fields, models
from odoo.exceptions import ValidationError

STAGES = [
    ("normal", "Bình thường"),
    ("watch", "Theo dõi"),
    ("markdown", "Giảm giá đẩy hàng"),
    ("recall", "Thu hồi / cách ly"),
    ("expired", "Hết hạn - chờ hủy"),
]
# Thứ tự mức độ nghiêm trọng, dùng để chỉ leo thang, không lùi mức.
STAGE_RANK = {key: i for i, (key, _label) in enumerate(STAGES)}


class NpExpiryRule(models.Model):
    _name = "bh.expiry.rule"
    _description = "Quy tắc cận hạn theo % hạn dùng còn lại"
    _order = "categ_id, max_remaining_pct"

    name = fields.Char("Tên quy tắc", required=True)
    active = fields.Boolean(default=True)
    categ_id = fields.Many2one(
        "product.category", "Nhóm sản phẩm",
        help="Để trống: áp dụng cho mọi nhóm chưa có quy tắc riêng.")
    stage = fields.Selection(STAGES[1:], "Mức", required=True)
    max_remaining_pct = fields.Float(
        "Áp dụng khi % hạn còn lại ≤", required=True,
        help="Ví dụ 30 nghĩa là lô còn 30% thời hạn sử dụng trở xuống.")
    discount_pct = fields.Float("Đề xuất giảm giá (%)")
    responsible_id = fields.Many2one("res.users", "Người xử lý", default=lambda self: self.env.user)
    note = fields.Text("Hướng dẫn xử lý")

    @api.constrains("max_remaining_pct", "discount_pct")
    def _check_pct(self):
        for rule in self:
            if not 0 <= rule.max_remaining_pct <= 100 or not 0 <= rule.discount_pct <= 100:
                raise ValidationError("Phần trăm phải nằm trong khoảng 0–100.")

    @api.model
    def _rules_for_category(self, categ):
        """Quy tắc của nhóm gần nhất (đi ngược lên cây nhóm), nếu không có thì quy tắc chung."""
        while categ:
            rules = self.search([("categ_id", "=", categ.id)])
            if rules:
                return rules
            categ = categ.parent_id
        return self.search([("categ_id", "=", False)])

    @api.model
    def _match(self, categ, remaining_pct):
        """Trả về quy tắc nghiêm trọng nhất mà lô thỏa (ngưỡng nhỏ nhất vẫn ≥ % còn lại)."""
        rules = self._rules_for_category(categ).filtered(lambda r: remaining_pct <= r.max_remaining_pct)
        return rules.sorted(lambda r: (r.max_remaining_pct, -STAGE_RANK[r.stage]))[:1]
