import logging
from collections import defaultdict

import requests

from odoo import api, fields, models

from .bh_expiry_rule import STAGES, STAGE_RANK

_logger = logging.getLogger(__name__)


class StockLot(models.Model):
    _inherit = "stock.lot"

    bh_stage = fields.Selection(STAGES, "Mức cận hạn", default="normal", tracking=True, index=True)
    bh_stage_date = fields.Date("Ngày vào mức")
    bh_remaining_pct = fields.Float("% hạn dùng còn lại", digits=(5, 1))
    bh_days_left = fields.Integer("Số ngày còn lại")
    bh_stock_value = fields.Float("Giá trị tồn (giá vốn)", compute="_compute_bh_stock_value")
    bh_customer_qty = fields.Float("SL đang ở điểm bán", compute="_compute_bh_customer_qty",
                                   help="Đã giao cho khách mà chưa trả lại.")

    def _compute_bh_stock_value(self):
        for lot in self:
            lot.bh_stock_value = lot.product_qty * lot.product_id.standard_price

    def _bh_qty_by_customer(self):
        """{partner: số lượng của lô đang nằm ở khách} = đã giao - đã trả về."""
        self.ensure_one()
        result = defaultdict(float)
        lines = self.env["stock.move.line"].sudo().search([("lot_id", "=", self.id), ("state", "=", "done")])
        for ml in lines:
            partner = ml.picking_id.partner_id.commercial_partner_id
            if ml.location_dest_id.usage == "customer":
                result[partner] += ml.quantity
            elif ml.location_id.usage == "customer":
                result[partner] -= ml.quantity
        return {p: q for p, q in result.items() if q > 0}

    def _compute_bh_customer_qty(self):
        for lot in self:
            lot.bh_customer_qty = sum(lot._bh_qty_by_customer().values()) if lot.id else 0.0

    def _bh_remaining(self, now=None):
        """(% còn lại, số ngày còn lại). Tổng thời hạn lấy theo cấu hình sản phẩm, nếu không có thì từ ngày tạo lô."""
        self.ensure_one()
        now = now or fields.Datetime.now()
        left = self.expiration_date - now
        total_days = self.product_id.product_tmpl_id.expiration_time
        if not total_days:
            total_days = max((self.expiration_date - self.create_date).days, 1)
        pct = max(left.total_seconds() / 86400 / total_days * 100, 0.0)
        return round(min(pct, 100.0), 1), left.days

    def _bh_evaluate(self, now=None):
        """Tính lại mức cho từng lô; chỉ leo thang. Trả về các log mới tạo."""
        Rule = self.env["bh.expiry.rule"]
        Log = self.env["bh.expiry.log"]
        new_logs = Log
        today = fields.Date.context_today(self)
        for lot in self.filtered("expiration_date"):
            qty_internal = lot.product_qty
            by_customer = lot._bh_qty_by_customer()
            if qty_internal <= 0 and not by_customer:
                continue
            pct, days = lot._bh_remaining(now)
            rule = Rule._match(lot.product_id.categ_id, pct)
            stage = "expired" if pct <= 0 else (rule.stage if rule else "normal")
            lot.write({"bh_remaining_pct": pct, "bh_days_left": days})
            if STAGE_RANK[stage] <= STAGE_RANK[lot.bh_stage or "normal"]:
                continue
            lot.write({"bh_stage": stage, "bh_stage_date": today})
            responsible = rule.responsible_id or self.env.user
            price = lot.product_id.lst_price
            vals = []
            if qty_internal > 0:
                vals.append({"partner_id": False, "qty": qty_internal})
            if stage in ("recall", "expired"):
                vals += [{"partner_id": p.id, "qty": q} for p, q in by_customer.items()]
            for v in vals:
                v.update({
                    "lot_id": lot.id,
                    "stage": stage,
                    "rule_id": rule.id,
                    "remaining_pct": pct,
                    "unit_cost": lot.product_id.standard_price,
                    "suggested_price": price * (1 - (rule.discount_pct or 0) / 100) if stage == "markdown" else 0.0,
                    "user_id": responsible.id,
                })
            logs = Log.create(vals)
            new_logs |= logs
            stage_label = dict(STAGES)[stage]
            lot.activity_schedule(
                "mail.mail_activity_data_todo",
                date_deadline=today,
                summary=f"Lô {lot.name} chuyển mức: {stage_label}",
                note=rule.note or "Kiểm tra lô và xử lý theo quy định cận hạn.",
                user_id=responsible.id,
            )
        return new_logs

    @api.model
    def _bh_cron_check_expiry(self):
        lots = self.search([("expiration_date", "!=", False), ("bh_stage", "!=", "expired")])
        new_logs = lots._bh_evaluate()
        if new_logs:
            self._bh_notify_telegram(new_logs)
        _logger.info("bh_near_expiry: kiểm tra %s lô, tạo %s việc cần xử lý", len(lots), len(new_logs))
        return True

    @api.model
    def _bh_notify_telegram(self, logs):
        """Gửi tóm tắt sang Telegram nếu đã cấu hình tham số hệ thống (tích hợp hệ thống ngoài #1)."""
        icp = self.env["ir.config_parameter"].sudo()
        token = icp.get_param("bh_near_expiry.telegram_bot_token")
        chat_id = icp.get_param("bh_near_expiry.telegram_chat_id")
        if not token or not chat_id:
            return False
        stage_label = dict(STAGES)
        lines = ["CẢNH BÁO CẬN HẠN - Bảo Hân"]
        for log in logs[:30]:
            where = log.partner_id.name or "Kho công ty"
            lines.append(f"- {log.product_id.display_name} | lô {log.lot_id.name} | "
                         f"{stage_label[log.stage]} | còn {log.remaining_pct}% | SL {log.qty:g} | {where}")
        try:
            requests.post(f"https://api.telegram.org/bot{token}/sendMessage",
                          json={"chat_id": chat_id, "text": "\n".join(lines)}, timeout=10)
        except requests.RequestException as e:  # không để lỗi mạng làm hỏng cron
            _logger.warning("bh_near_expiry: gửi Telegram thất bại: %s", e)
            return False
        return True

    def action_bh_evaluate_now(self):
        self._bh_evaluate()
        return True
