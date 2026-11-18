from odoo.addons.account.tests.common import AccountTestInvoicingCommon
from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestBankWebhook(AccountTestInvoicingCommon):

    def _invoice(self, amount):
        inv = self.init_invoice("out_invoice", amounts=[amount], post=True)
        return inv

    def test_match_and_pay(self):
        inv = self._invoice(1000.0)
        payload = {"id": 9001, "transferAmount": inv.amount_total, "transferType": "in",
                   "content": f"THANH TOAN {inv.name.replace('/', '')} QUAN CA PHE"}
        txn = self.env["bh.bank.txn"]._process(payload)
        self.assertEqual(txn.state, "matched")
        self.assertEqual(txn.move_id, inv)
        self.assertIn(inv.payment_state, ("paid", "in_payment"))

    def test_duplicate_ignored(self):
        inv = self._invoice(500.0)
        payload = {"id": 9002, "transferAmount": 100.0, "content": inv.name}
        self.env["bh.bank.txn"]._process(payload)
        second = self.env["bh.bank.txn"]._process(payload)
        self.assertEqual(second.state, "duplicate")
        self.assertEqual(len(inv._get_reconciled_payments()), 1)

    def test_unmatched(self):
        txn = self.env["bh.bank.txn"]._process({"id": 9003, "transferAmount": 50.0, "content": "CHUYEN TIEN"})
        self.assertEqual(txn.state, "unmatched")
        self.assertFalse(txn.payment_id)
