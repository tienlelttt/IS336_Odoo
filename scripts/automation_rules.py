# Automation Rules (base_automation) cho Bảo Hân – bản 2 theo vận hành thực tế. Chạy trong Odoo shell; chạy lại sẽ cập nhật.
# Trên giao diện: Thiết lập > Kỹ thuật > Tự động hóa > Quy tắc tự động hóa (bật chế độ nhà phát triển).
# Code trong server action chạy trong sandbox: không gán thuộc tính trực tiếp (dùng write), không gọi hàm bắt đầu bằng "_".


def model(name):
    return env["ir.model"]._get(name)


def field(model_name, fname):
    return env["ir.model.fields"]._get(model_name, fname)


def selection(model_name, fname, value):
    return env["ir.model.fields.selection"].search([("field_id", "=", field(model_name, fname).id),
                                                    ("value", "=", value)], limit=1)


def rule(name, vals, actions):
    auto = env["base.automation"].with_context(active_test=False).search([("name", "=", name)], limit=1)
    vals = {"name": name, "active": True, **vals}
    if auto:
        auto.action_server_ids.unlink()
        auto.write(vals)
    else:
        auto = env["base.automation"].create(vals)
    for a in actions:
        env["ir.actions.server"].create({"model_id": vals["model_id"], "base_automation_id": auto.id,
                                         "usage": "base_automation", **a})
    print("  ", name, "| trigger:", auto.trigger, "| active:", auto.active)
    return auto


todo = env.ref("mail.mail_activity_data_todo")
user = {u.login.split("@")[0]: u for u in env["res.users"].search([("login", "like", "@baohan.local")])}

# Bỏ quy tắc cũ của bản 1 nếu còn
env["base.automation"].with_context(active_test=False).search([("name", "=", "BH2 - Báo giá trên 10 triệu: giám đốc duyệt")]).unlink()

# Đoạn kiểm tra rủi ro công nợ dùng chung cho BH2a, BH2b
RISK = '''
def risk(order):
    p = order.partner_id.commercial_partner_id
    overdue = env["account.move"].search_count([
        ("partner_id", "child_of", p.id), ("move_type", "=", "out_invoice"), ("state", "=", "posted"),
        ("payment_state", "in", ("not_paid", "partial")), ("invoice_date_due", "<", datetime.date.today())])
    over = p.use_partner_credit_limit and (p.credit + order.amount_total > p.credit_limit)
    reasons = []
    if overdue:
        reasons.append("có " + str(overdue) + " hóa đơn quá hạn")
    if over:
        reasons.append("vượt hạn mức nợ " + "{:,.0f}".format(p.credit_limit))
    return reasons

approved = env["crm.tag"].search([("name", "=", "Đã duyệt công nợ")], limit=1)
'''

# BH1. Xe NCC đến (phiếu nhập Sẵn sàng) → tạo phiếu QC cho từng NVL, giao việc QC; kiểm xong thủ kho mới xác nhận
QC_IN = '''
qc_user = env["res.users"].search([("login", "=", "qc@baohan.local")], limit=1)
tests = {"NVL mát": "Kiểm nguyên liệu mát đầu vào", "NVL khô": "Kiểm nguyên liệu khô đầu vào"}
for picking in records:
    for move in picking.move_ids:
        test_name = tests.get(move.product_id.categ_id.name)
        if not test_name:
            continue
        # Trạng thái có thể được ghi nhiều lần: đã có phiếu cho phiếu nhập + sản phẩm này thì bỏ qua
        if env["qc.inspection"].search_count([("internal_notes", "ilike", picking.name),
                                              ("product_id", "=", move.product_id.id)]):
            continue
        test = env["qc.test"].search([("name", "=", test_name)], limit=1)
        insp = env["qc.inspection"].create({
            "test": test.id, "object_id": "product.product,%s" % move.product_id.id, "qty": move.product_uom_qty,
            "internal_notes": "Kiểm tại cửa kho trước khi nhận: " + picking.name + " (" + (picking.origin or "") + ")",
            "inspection_lines": [(0, 0, {"test_line": q.id, "name": q.name, "product_id": move.product_id.id,
                                         "question_type": q.type, "min_value": q.min_value, "max_value": q.max_value,
                                         "possible_ql_values": [(6, 0, q.ql_values.ids)],
                                         "test_uom_id": q.uom_id.id, "uom_id": q.uom_id.id}) for q in test.test_lines],
        })
        insp.action_todo()
        # Phiếu QC được chuẩn bị sẵn khi đơn mua xác nhận; hạn làm là ngày xe NCC dự kiến đến
        insp.activity_schedule("mail.mail_activity_data_todo", summary="Kiểm hàng NCC: " + move.product_id.display_name,
                               user_id=qc_user.id or env.user.id, date_deadline=picking.scheduled_date.date())
'''
rule("BH1 - Đơn mua xác nhận: chuẩn bị phiếu kiểm tra tại cửa kho", {
    "model_id": model("stock.picking").id, "trigger": "on_state_set",
    "trg_selection_field_id": selection("stock.picking", "state", "assigned").id,
    "filter_domain": "[('picking_type_code', '=', 'incoming')]",
}, [{"name": "Tạo phiếu QC và giao việc cho QC", "state": "code", "code": QC_IN}])

# BH2a. Tạo / sửa báo giá cho khách đang có rủi ro công nợ → giao việc giám đốc xem trước (không chặn)
BH2A = RISK + '''
gd = env["res.users"].search([("login", "=", "giamdoc@baohan.local")], limit=1)
for order in records:
    reasons = risk(order)
    if not reasons or approved in order.tag_ids:
        continue
    if order.activity_ids.filtered(lambda a: a.summary and a.summary.startswith("Duyệt công nợ")):
        continue
    order.activity_schedule("mail.mail_activity_data_todo", user_id=gd.id or env.user.id,
                            summary="Duyệt công nợ: " + ", ".join(reasons),
                            note="Xem công nợ khách. Đồng ý giao thì gắn nhãn 'Đã duyệt công nợ' lên đơn.")
'''
rule("BH2a - Khách có rủi ro công nợ: báo giám đốc", {
    "model_id": model("sale.order").id, "trigger": "on_create_or_write",
    "trigger_field_ids": [(6, 0, [field("sale.order", "partner_id").id, field("sale.order", "amount_total").id])],
    "filter_domain": "[('state', 'in', ('draft', 'sent'))]",
}, [{"name": "Giao việc giám đốc duyệt công nợ", "state": "code", "code": BH2A}])

# BH2b. Xác nhận đơn khi khách nợ quá hạn / vượt hạn mức mà chưa có nhãn duyệt → chặn
BH2B = RISK + '''
for order in records:
    reasons = risk(order)
    if reasons and approved not in order.tag_ids:
        raise UserError("Không thể xác nhận đơn " + order.name + ": khách " + order.partner_id.name + " "
                        + ", ".join(reasons) + ". Cần giám đốc gắn nhãn 'Đã duyệt công nợ'.")
'''
rule("BH2b - Chặn xác nhận đơn khi chưa duyệt công nợ", {
    "model_id": model("sale.order").id, "trigger": "on_state_set",
    "trg_selection_field_id": selection("sale.order", "state", "sale").id,
}, [{"name": "Kiểm tra công nợ trước khi xác nhận", "state": "code", "code": BH2B}])

# BH3. Hóa đơn bán quá hạn 1 ngày mà chưa trả đủ → giao việc nhắc nợ cho kế toán
rule("BH3 - Hóa đơn quá hạn: nhắc nợ", {
    "model_id": model("account.move").id, "trigger": "on_time",
    "trg_date_id": field("account.move", "invoice_date_due").id, "trg_date_range": 1,
    "trg_date_range_type": "day", "trg_date_range_mode": "after",
    "filter_domain": "[('move_type', '=', 'out_invoice'), ('state', '=', 'posted'), "
                     "('payment_state', 'in', ('not_paid', 'partial'))]",
}, [{"name": "Giao việc nhắc nợ cho kế toán", "state": "next_activity", "activity_type_id": todo.id,
     "activity_summary": "Gọi nhắc nợ khách hàng (hóa đơn quá hạn)", "activity_user_type": "specific",
     "activity_user_id": user["ketoan"].id, "activity_date_deadline_range": 0}])

# BH4. Việc cận hạn mới → webhook Google Sheets (tắt cho tới khi có URL Apps Script)
url = env["ir.config_parameter"].sudo().get_param("bh_demo.sheets_webhook_url") or ""
rule("BH4 - Việc cận hạn mới: gửi sang Google Sheets", {
    "model_id": model("bh.expiry.log").id, "trigger": "on_create", "active": bool(url),
}, [{"name": "Webhook Google Sheets", "state": "webhook", "webhook_url": url or "https://script.google.com/macros/s/DIEN_ID/exec",
     "webhook_field_ids": [(6, 0, [field("bh.expiry.log", f).id for f in
                                   ("product_id", "lot_id", "stage", "remaining_pct", "qty", "value", "partner_id",
                                    "expiration_date", "user_id")])]}])

# BH5. Lệnh sản xuất được xác nhận → phiếu kiểm mẫu thành phẩm theo lô, giao việc QC (lấy mẫu lúc 05:00)
QC_MO = '''
qc_user = env["res.users"].search([("login", "=", "qc@baohan.local")], limit=1)
test = env["qc.test"].search([("name", "=", "Kiểm mẫu thành phẩm theo lô")], limit=1)
for mo in records:
    if env["qc.inspection"].search_count([("internal_notes", "ilike", mo.name)]):
        continue
    insp = env["qc.inspection"].create({
        "test": test.id, "object_id": "product.product,%s" % mo.product_id.id, "qty": mo.product_qty,
        "internal_notes": "Kiểm mẫu lô của lệnh " + mo.name + " (" + (mo.origin or "kế hoạch") + ")",
        "inspection_lines": [(0, 0, {"test_line": q.id, "name": q.name, "product_id": mo.product_id.id,
                                     "question_type": q.type, "min_value": q.min_value, "max_value": q.max_value,
                                     "possible_ql_values": [(6, 0, q.ql_values.ids)],
                                     "test_uom_id": q.uom_id.id, "uom_id": q.uom_id.id}) for q in test.test_lines],
    })
    insp.action_todo()
    insp.activity_schedule("mail.mail_activity_data_todo", summary="Lấy mẫu kiểm " + mo.name,
                           user_id=qc_user.id or env.user.id)
'''
rule("BH5 - Lệnh sản xuất xác nhận: tạo phiếu kiểm mẫu thành phẩm", {
    "model_id": model("mrp.production").id, "trigger": "on_state_set",
    "trg_selection_field_id": selection("mrp.production", "state", "confirmed").id,
}, [{"name": "Tạo phiếu QC thành phẩm", "state": "code", "code": QC_MO}])

env.cr.commit()
print("XONG automation")
