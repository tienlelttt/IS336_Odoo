import re

from odoo import api, fields, models


class BhBankTxn(models.Model):
    """Giao dịch nhận từ webhook ngân hàng (định dạng kiểu SePay). Lưu lại để không ghi nhận trùng."""
    _name = "bh.bank.txn"
    _description = "Giao dịch ngân hàng nhận qua webhook"
    _order = "id desc"

    txn_ref = fields.Char("Mã giao dịch", required=True, index=True)
    amount = fields.Monetary("Số tiền")
    currency_id = fields.Many2one("res.currency", default=lambda self: self.env.company.currency_id)
    content = fields.Char("Nội dung chuyển khoản")
    move_id = fields.Many2one("account.move", "Hóa đơn khớp")
    payment_id = fields.Many2one("account.payment", "Thanh toán đã tạo")
    state = fields.Selection([("matched", "Đã ghi nhận"), ("unmatched", "Không khớp hóa đơn"), ("duplicate", "Trùng")],
                             required=True)

    @api.model
    def _process(self, payload):
        """Trả về bản ghi giao dịch. Chỉ xử lý tiền vào; tìm số hóa đơn trong nội dung chuyển khoản."""
        ref = str(payload.get("id") or payload.get("referenceCode") or "")
        amount = float(payload.get("transferAmount") or 0)
        content = payload.get("content") or ""
        if self.search([("txn_ref", "=", ref)], limit=1):
            return self.create({"txn_ref": ref, "amount": amount, "content": content, "state": "duplicate"})
        invoice = self._find_invoice(content)
        txn = self.create({"txn_ref": ref, "amount": amount, "content": content,
                           "move_id": invoice.id, "state": "matched" if invoice else "unmatched"})
        if invoice and amount > 0:
            bank = self.env["account.journal"].search(
                [("type", "=", "bank"), ("company_id", "=", invoice.company_id.id)], limit=1)
            wizard = self.env["account.payment.register"].with_context(
                active_model="account.move", active_ids=invoice.ids).create({
                    "amount": min(amount, invoice.amount_residual),
                    "journal_id": bank.id,
                    "communication": f"CK {ref} - {invoice.name}",
                })
            payments = wizard._create_payments()
            txn.payment_id = payments[:1]
        return txn

    @api.model
    def _find_invoice(self, content):
        # Ngân hàng thường bỏ dấu '/', nên so khớp cả dạng INV/2026/00012 lẫn INV202600012.
        squashed = re.sub(r"[^A-Z0-9]", "", content.upper())
        invoices = self.env["account.move"].search([
            ("move_type", "=", "out_invoice"), ("state", "=", "posted"),
            ("payment_state", "in", ("not_paid", "partial"))])
        for inv in invoices:
            if re.sub(r"[^A-Z0-9]", "", inv.name.upper()) in squashed:
                return inv
        return self.env["account.move"]
