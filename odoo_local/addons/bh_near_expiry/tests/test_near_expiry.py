from datetime import timedelta

from odoo import fields
from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestNearExpiry(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.stock = cls.env.ref("stock.stock_location_stock")
        cls.product = cls.env["product.product"].create({
            "name": "Bánh bông lan test",
            "is_storable": True,
            "tracking": "lot",
            "use_expiration_date": True,
            "expiration_time": 30,
            "standard_price": 5000,
            "list_price": 8000,
        })

    def _lot(self, days_left, qty=10):
        lot = self.env["stock.lot"].create({
            "name": f"L{days_left}",
            "product_id": self.product.id,
            "expiration_date": fields.Datetime.now() + timedelta(days=days_left, hours=1),
        })
        self.env["stock.quant"]._update_available_quantity(self.product, self.stock, qty, lot_id=lot)
        return lot

    def test_stage_by_remaining_pct(self):
        fresh, watch, markdown, recall = self._lot(25), self._lot(12), self._lot(7), self._lot(3)
        logs = (fresh | watch | markdown | recall)._bh_evaluate()
        self.assertEqual(fresh.bh_stage, "normal")
        self.assertEqual(watch.bh_stage, "watch")        # 40% còn lại
        self.assertEqual(markdown.bh_stage, "markdown")  # ~23%
        self.assertEqual(recall.bh_stage, "recall")      # 10%
        self.assertEqual(len(logs), 3)
        md_log = logs.filtered(lambda l: l.lot_id == markdown)
        self.assertAlmostEqual(md_log.suggested_price, 6400)  # giảm 20%

    def test_no_duplicate_and_only_escalate(self):
        lot = self._lot(7)
        self.assertEqual(len(lot._bh_evaluate()), 1)
        self.assertFalse(lot._bh_evaluate(), "Chạy lại cùng mức thì không tạo việc trùng")

    def test_scrap_records_loss(self):
        lot = self._lot(3, qty=4)
        log = lot._bh_evaluate()
        log.action_scrap()
        self.assertEqual(log.state, "done")
        self.assertEqual(log.loss_value, 4 * 5000)
        self.assertEqual(lot.product_qty, 0)
