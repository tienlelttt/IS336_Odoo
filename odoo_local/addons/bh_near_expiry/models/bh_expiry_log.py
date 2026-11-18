from odoo import api, fields, models
from odoo.exceptions import UserError

from .bh_expiry_rule import STAGES

RESOLUTIONS = [
    ("sold_markdown", "Đã bán giảm giá"),
    ("recalled", "Đã thu hồi từ điểm bán"),
    ("returned_vendor", "Trả nhà cung cấp"),
    ("scrapped", "Đã hủy"),
    ("donated", "Tặng / từ thiện"),
    ("other", "Khác"),
]


class NpExpiryLog(models.Model):
    _name = "bh.expiry.log"
    _description = "Việc xử lý hàng cận hạn"
    _inherit = ["mail.thread"]
    _order = "create_date desc"

    lot_id = fields.Many2one("stock.lot", "Lô", required=True, ondelete="cascade", index=True)
    product_id = fields.Many2one(related="lot_id.product_id", store=True, string="Sản phẩm")
    categ_id = fields.Many2one(related="lot_id.product_id.categ_id", store=True, string="Nhóm SP")
    expiration_date = fields.Datetime(related="lot_id.expiration_date", string="Hạn sử dụng")
    partner_id = fields.Many2one("res.partner", "Điểm bán (khách)",
                                 help="Trống: hàng đang ở kho công ty. Có giá trị: hàng đang ở khách cần thu hồi.")
    stage = fields.Selection(STAGES, "Mức", required=True)
    rule_id = fields.Many2one("bh.expiry.rule", "Quy tắc")
    remaining_pct = fields.Float("% hạn còn lại lúc phát hiện", digits=(5, 1))
    qty = fields.Float("Số lượng")
    unit_cost = fields.Float("Giá vốn đơn vị")
    value = fields.Float("Giá trị", compute="_compute_value", store=True)
    suggested_price = fields.Float("Giá bán đề xuất")
    user_id = fields.Many2one("res.users", "Người xử lý", tracking=True)
    state = fields.Selection([("todo", "Cần xử lý"), ("done", "Đã xử lý")], default="todo", tracking=True)
    resolution = fields.Selection(RESOLUTIONS, "Cách xử lý", tracking=True)
    loss_value = fields.Float("Tổn thất", tracking=True,
                              help="Giá trị mất đi: toàn bộ giá vốn nếu hủy, phần chênh nếu bán giảm giá.")
    scrap_id = fields.Many2one("stock.scrap", "Phiếu hủy", readonly=True)

    @api.depends("qty", "unit_cost")
    def _compute_value(self):
        for log in self:
            log.value = log.qty * log.unit_cost

    def action_scrap(self):
        """Tạo và xác nhận phiếu hủy cho phần hàng đang ở kho công ty."""
        for log in self:
            if log.partner_id:
                raise UserError("Hàng đang ở điểm bán: cần thu hồi về kho trước khi hủy.")
            qty = min(log.qty, log.lot_id.product_qty)
            if qty <= 0:
                raise UserError(f"Lô {log.lot_id.name} không còn tồn trong kho.")
            quant = self.env["stock.quant"].search([
                ("lot_id", "=", log.lot_id.id), ("location_id.usage", "=", "internal"), ("quantity", ">", 0)], limit=1)
            scrap = self.env["stock.scrap"].create({
                "product_id": log.product_id.id,
                "lot_id": log.lot_id.id,
                "scrap_qty": qty,
                "product_uom_id": log.product_id.uom_id.id,
                "location_id": quant.location_id.id,
                "origin": f"Cận hạn {log.lot_id.name}",
            })
            scrap.action_validate()
            log.write({"scrap_id": scrap.id, "state": "done", "resolution": "scrapped",
                       "loss_value": qty * log.unit_cost})
        return True

    def action_mark_done(self):
        for log in self:
            if not log.resolution:
                raise UserError("Chọn 'Cách xử lý' trước khi đánh dấu hoàn tất.")
        self.write({"state": "done"})
        return True
