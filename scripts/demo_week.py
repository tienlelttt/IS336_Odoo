# Kịch bản "tuần đầu go-live" của Bảo Hân (bản 2). Chạy trong Odoo shell SAU seed + automation, nối sau seed_data.py:
#   cat scripts/seed_data.py scripts/demo_week.py | docker compose run --rm -T odoo -- shell -d baohan --no-http --addons-path=...
#
# Vì sao không giả lập lùi nhiều tuần: Odoo kiểm "ngày rút khỏi kệ" của lô theo giờ thật, nên lô bánh mì 5 ngày tạo
# cho tuần trước sẽ không giao được. Kịch bản bám đúng một dự án ERP thật:
#   Thứ Bảy 14/11: chuyển dữ liệu đầu kỳ (kiểm kê tồn, công nợ tháng 10), nhận đơn cho thứ Hai.
#   Thứ Hai 16/11, thứ Ba 17/11: vận hành trọn ngày.
#   Thứ Tư 18/11 (hôm nay): buổi sáng xong; chiều đang nhận đơn cho thứ Năm, chưa lập kế hoạch sản xuất, chưa lập hóa đơn.
# Mỗi phần đánh dấu bằng tham số 'bh_week.<phần>' nên chạy lại chỉ làm phần chưa xong.
import hashlib
from datetime import date, datetime, timedelta

from odoo import fields

ICP = env["ir.config_parameter"].sudo()
wh = env["stock.warehouse"].search([], limit=1)
STOCK = wh.lot_stock_id
CASH = env["account.journal"].search([("type", "=", "cash")], limit=1)
BANK = env["account.journal"].search([("type", "=", "bank")], limit=1)
U = {u.login.split("@")[0]: u for u in env["res.users"].search([("login", "like", "@baohan.local")])}
APPROVED = env["crm.tag"].search([("name", "=", "Đã duyệt công nợ")], limit=1)
ACC_OPEN = env["account.account"].search([("code", "=like", "4211%")], limit=1)  # TK đối ứng số dư đầu kỳ


def P(code):
    return env["product.product"].search([("default_code", "=", code)], limit=1)


def C(ref):
    return env["res.partner"].search([("ref", "=", ref)], limit=1)


def L(name):
    return env["stock.location"].search([("name", "=", name)], limit=1)


def at(d, hh, mm=0):
    """Giờ địa phương (UTC+7) → datetime UTC lưu trong Odoo."""
    return datetime(d.year, d.month, d.day, hh, mm) - timedelta(hours=7)


def section(key):
    def deco(fn):
        if ICP.get_param(f"bh_week.{key}"):
            print(f"[bỏ qua] {key}")
            return fn
        print(f"[chạy] {key}")
        fn()
        ICP.set_param(f"bh_week.{key}", fields.Datetime.to_string(fields.Datetime.now()))
        env.cr.commit()
        return fn
    return deco


def vary(base, key):
    """Biến động ±10% cố định theo khóa (để chạy lại vẫn ra cùng số)."""
    h = int(hashlib.md5(key.encode()).hexdigest(), 16) % 21 - 10
    return max(1, round(base * (1 + h / 100)))


def lot_for(product, made_at, name):
    t = product.product_tmpl_id
    exp = made_at + timedelta(days=t.expiration_time)
    return env["stock.lot"].create({
        "name": name, "product_id": product.id, "expiration_date": exp,
        "use_date": exp - timedelta(days=t.use_time), "removal_date": exp - timedelta(days=t.removal_time),
        "alert_date": exp - timedelta(days=t.alert_time)})


def backdate(pickings, dt):
    pickings.write({"date_done": dt, "scheduled_date": dt})
    pickings.move_ids.write({"date": dt})
    pickings.move_ids.move_line_ids.write({"date": dt})


def wizards(res, no_backorder=True):
    """Xử lý hộp thoại khi xác nhận: thiếu hàng (không tạo đơn chờ với bánh tươi), giao lô qua ngày cảnh báo, làm thiếu MO."""
    for _i in range(4):
        if not isinstance(res, dict) or not res.get("res_model"):
            return
        model = res["res_model"]
        wiz = env[model].with_context(res.get("context", {})).create({})
        if model == "stock.backorder.confirmation":
            res = wiz.process_cancel_backorder() if no_backorder else wiz.process()
        elif model == "mrp.production.backorder":
            res = wiz.action_close_mo() if no_backorder else wiz.action_backorder()
        else:
            res = wiz.process() if hasattr(wiz, "process") else wiz.action_confirm()


def validate(picking, done_qty=None, lots=None, no_backorder=True):
    """done_qty: {mã SP: số thực}; lots: {mã SP: (tên lô, hạn dùng)} cho hàng nhập."""
    picking.action_assign()
    for move in picking.move_ids:
        code = move.product_id.default_code
        qty = (done_qty or {}).get(code, move.product_uom_qty)
        if lots and code in lots:
            move.move_line_ids.unlink()
            if qty:
                env["stock.move.line"].create({
                    "move_id": move.id, "picking_id": picking.id, "product_id": move.product_id.id,
                    "product_uom_id": move.product_uom.id, "location_id": move.location_id.id,
                    "location_dest_id": move.location_dest_id.id, "lot_name": lots[code][0],
                    "expiration_date": lots[code][1], "quantity": qty})
        elif qty != move.quantity and move.product_id.tracking == "none":
            move.quantity = qty
        elif qty < move.quantity:  # giao thiếu hàng theo lô: bớt dòng cuối
            extra = move.quantity - qty
            for ml in move.move_line_ids.sorted("id", reverse=True):
                cut = min(extra, ml.quantity)
                ml.quantity -= cut
                extra -= cut
                if not extra:
                    break
        move.picked = True
    wizards(picking.button_validate(), no_backorder)
    return picking


def fill_qc(insp, ok=True, temp=95.0):
    for line in insp.inspection_lines:
        if line.question_type == "quantitative":
            if not line.uom_id:
                line.uom_id = line.test_uom_id or env.ref("uom.product_uom_unit")
            line.quantitative_value = temp if ok or "Nhiệt" not in line.name else 88.0
        else:
            vals = line.test_line.ql_values
            good = vals.filtered("ok")[:1]
            line.qualitative_value = good if ok or "Bao bì" not in line.name else (vals - good)[:1]
    insp.action_confirm()
    if insp.state == "waiting":
        insp.action_approve()
    insp.activity_ids.action_feedback(feedback="Đã kiểm, kết quả: " + insp.state)


def invoice(orders, d):
    moves = orders._create_invoices()
    moves.invoice_date = d
    moves.action_post()
    return moves


def pay(moves, journal, d, amount=None):
    vals = {"journal_id": journal.id, "payment_date": d}
    if amount:
        vals["amount"] = amount
    wiz = env["account.payment.register"].with_context(active_model="account.move", active_ids=moves.ids).create(vals)
    return wiz._create_payments()


# ---------------------------------------------------------------------------------------------------------------
def take_orders(deliver_day, confirm=True, skip=()):
    """16:00 ngày hôm trước: kinh doanh nhập đơn cố định cho ngày giao."""
    order_day = deliver_day - timedelta(days=2 if deliver_day.weekday() == 0 else 1)
    created = env["sale.order"]
    for ref_, plan in STANDING_ORDERS.items():
        lines = plan.get(None, []) + plan.get(deliver_day.weekday(), [])
        if not lines or ref_ in skip:
            continue
        so = env["sale.order"].create({
            "partner_id": C(ref_).id, "user_id": C(ref_).user_id.id,
            "date_order": at(order_day, 15, 30), "commitment_date": at(deliver_day, 6),
            "client_order_ref": f"Đơn cố định {deliver_day:%d/%m}",
            "order_line": [(0, 0, {"product_id": P(c).id, "product_uom_qty": vary(q, f"{ref_}{c}{deliver_day}")})
                           for c, q in lines]})
        created |= so
    if confirm:
        for so in created:
            try:
                with env.cr.savepoint():
                    so.action_confirm()
            except Exception as e:  # BH2b chặn khách nợ quá hạn
                print("   CHẶN:", so.name, so.partner_id.ref, str(e)[:90])
        created.filtered(lambda s: s.state == "sale").write({"date_order": at(order_day, 15, 30)})
    return created


def plan_production(plan_day, prod_day, short=None, fail_qc=None, scrap_after=None):
    """16:00 ngày lập kế hoạch: Bổ sung hàng → lệnh sản xuất; 16:30 thủ kho cấp NVL; ca đêm trước ngày prod_day;
    05:00 ngày prod_day ghi sản lượng."""
    before = env["mrp.production"].search([]).ids
    # Như khi quản đốc mở màn hình Bổ sung hàng: Odoo tự đề xuất dòng cho mọi sản phẩm có tồn dự báo âm
    env["stock.warehouse.orderpoint"].with_context(search_default_filter_to_reorder=True)._get_orderpoint_action()
    ops = env["stock.warehouse.orderpoint"].search([("product_id.default_code", "=like", "FG%")])
    ops._compute_qty_to_order() if hasattr(ops, "_compute_qty_to_order") else None
    ops.filtered(lambda o: o.qty_to_order > 0).action_replenish()
    mos = env["mrp.production"].search([("id", "not in", before)])
    mos.write({"date_start": at(prod_day - timedelta(days=1), 22)})
    for mo in mos.filtered(lambda m: m.state == "draft"):
        mo.action_confirm()
    print("   lệnh SX:", [(m.name, m.product_id.default_code, m.product_qty) for m in mos])
    # 16:30 cấp NVL cho cả ca ra Khu sản xuất
    for pick in mos.picking_ids.filtered(lambda p: p.state not in ("done", "cancel")):
        validate(pick)
        backdate(pick, at(plan_day, 16, 30))
    # 05:00 QC lấy mẫu, tổ trưởng ghi sản lượng
    made_at = at(prod_day, 5)
    for mo in mos:
        code = mo.product_id.default_code
        insp = env["qc.inspection"].search([("internal_notes", "ilike", mo.name)], limit=1)
        if insp:
            fill_qc(insp, ok=code != (fail_qc or ""))
        mo.action_assign()
        lot = lot_for(mo.product_id, made_at, f"{code}-{prod_day:%y%m%d}")
        mo.lot_producing_ids = lot
        mo.qty_producing = mo.product_qty - (short or {}).get(code, 0)
        for m in mo.move_raw_ids | mo.move_byproduct_ids:
            if m.quantity < m.product_uom_qty and m.product_id.tracking == "none":
                m.quantity = m.product_uom_qty
            m.picked = True
        res = mo.with_context(skip_consumption=True).button_mark_done()
        wizards(res, no_backorder=mo.product_id.categ_id.name in ("Bánh mì tươi", "Bánh lạnh"))
        mo.write({"date_finished": made_at})
        mo.move_finished_ids.write({"date": made_at})
        mo.move_raw_ids.write({"date": made_at})
        if scrap_after and code in scrap_after:  # bánh hỏng khi đóng gói, ghi sau khi lệnh xong
            quant = env["stock.quant"].search([("lot_id", "=", lot.id), ("location_id.usage", "=", "internal"),
                                               ("quantity", ">", 0)], limit=1)
            env["stock.scrap"].create({"product_id": mo.product_id.id, "lot_id": lot.id,
                                       "scrap_qty": scrap_after[code][0], "production_id": mo.id,
                                       "product_uom_id": mo.product_uom_id.id, "location_id": quant.location_id.id,
                                       "origin": scrap_after[code][1]}).action_validate()
    return mos


def deliver(d, actual=None):
    """05:00 soạn theo tuyến (đợt), tài xế giao; 10:30 tài xế về, thủ kho xác nhận số thực giao."""
    picks = env["stock.picking"].search([("picking_type_code", "=", "outgoing"), ("state", "not in", ("done", "cancel")),
                                         ("sale_id.commitment_date", ">=", at(d, 0)),
                                         ("sale_id.commitment_date", "<", at(d + timedelta(days=1), 0))])
    for route in ROUTES:
        group = picks.filtered(lambda p: route in p.partner_id.category_id.mapped("name"))
        if not group:
            continue
        batch = env["stock.picking.batch"].create({"description": f"{route} - {d:%d/%m}", "picking_ids": [(6, 0, group.ids)],
                                                   "user_id": U["thukho"].id, "scheduled_date": at(d, 5)})
        batch.action_confirm()
        for p in group:
            spec = (actual or {}).get(p.partner_id.ref)
            if spec and not any(spec.values()):
                # Khách không nhận: hàng chưa rời kho về sổ sách → hủy phiếu giao và đơn
                p.action_cancel()
                p.sale_id._action_cancel()
                p.sale_id.message_post(body="Khách đóng cửa, không nhận hàng; tài xế mang về kho.")
                continue
            p.action_assign()
            if not any(m.quantity for m in p.move_ids):
                # Hết bánh tươi khi soạn tới điểm cuối tuyến: không giao bù hôm sau, kinh doanh báo khách
                p.action_cancel()
                p.sale_id._action_cancel()
                p.sale_id.message_post(body="Hết hàng khi soạn theo tuyến; đã báo khách, không giao bù.")
                continue
            validate(p, spec)
            backdate(p, at(d, 10, 30))
        print("   giao", batch.name, route[:7], [(p.partner_id.ref, p.state) for p in group])
    return picks


def receive(d, reject=None):
    """07:00 xe NCC đến: QC kiểm tại cửa, thủ kho nhận số đạt (không tạo đơn chờ), ghi lô và hạn dùng."""
    picks = env["stock.picking"].search([("picking_type_code", "=", "incoming"), ("state", "=", "assigned"),
                                         ("scheduled_date", "<", at(d + timedelta(days=1), 0))])
    for p in picks:
        for insp in env["qc.inspection"].search([("internal_notes", "ilike", p.name), ("state", "=", "ready")]):
            bad = reject and insp.product_id.default_code in reject
            fill_qc(insp, ok=not bad, temp=3.5)
        lots = {m.product_id.default_code: (f"NCC-{m.product_id.default_code}-{d:%y%m%d}",
                                            at(d, 7) + timedelta(days=m.product_id.expiration_time))
                for m in p.move_ids if m.product_id.tracking == "lot"}
        qty = {c: q for c, (q, _why) in (reject or {}).items()}
        validate(p, {c: m.product_uom_qty - qty[c] for m in p.move_ids for c in [m.product_id.default_code] if c in qty},
                 lots)
        if reject:
            p.message_post(body="; ".join(f"{c}: trả lại {q} – {why}" for c, (q, why) in reject.items()))
        backdate(p, at(d, 7, 30))
        print("   nhận", p.name, p.partner_id.ref, p.state)


def purchase(day, deliver_on):
    """16:30: Bổ sung hàng NVL → đơn mua theo giá hợp đồng; trên 20 triệu chờ giám đốc duyệt."""
    before = env["purchase.order"].search([]).ids
    ops = env["stock.warehouse.orderpoint"].search([("product_id.default_code", "=like", "RM%")])
    ops.filtered(lambda o: o.qty_to_order > 0).action_replenish()
    pos = env["purchase.order"].search([("id", "not in", before)])
    for po in pos:
        po.write({"date_order": at(day, 16, 30), "date_planned": at(deliver_on, 7), "user_id": U["muahang"].id})
        po.button_confirm()
        # Odoo tính lại ngày giao theo giờ thật + thời gian giao của NCC; đặt lại theo lịch đã hẹn với NCC
        po.order_line.write({"date_planned": at(deliver_on, 7)})
        po.picking_ids.write({"scheduled_date": at(deliver_on, 7)})
        print("   mua", po.name, po.partner_id.ref, f"{po.amount_total:,.0f}", po.state)
    return pos


def vendor_bills(d):
    """Kế toán: hóa đơn NCC theo số đã nhận (đối chiếu đơn mua – phiếu nhập – hóa đơn); NCC trả ngay (trứng) chi tiền mặt."""
    immediate = env.ref("account.account_payment_term_immediate")
    for po in env["purchase.order"].search([("invoice_status", "=", "to invoice")]):
        po.action_create_invoice()
        bill = po.invoice_ids.filtered(lambda m: m.state == "draft")
        bill.write({"invoice_date": d, "ref": f"HĐ {po.partner_id.ref}/{d:%d%m}"})
        bill.action_post()
        if po.partner_id.property_supplier_payment_term_id == immediate:
            pay(bill, CASH, d)
        print("   hóa đơn NCC", bill.name, po.name, po.partner_id.ref, f"{bill.amount_total:,.0f}", bill.payment_state)


def end_of_day(d):
    """17:00 kế toán: hóa đơn hàng loạt theo số đã giao; ghi tiền mặt tài xế nộp; KH02 chuyển khoản ngay."""
    orders = env["sale.order"].search([("invoice_status", "=", "to invoice")])
    moves = invoice(orders, d) if orders else env["account.move"]
    for mv in moves:
        if "Trả tiền mặt cho tài xế" in mv.partner_id.category_id.mapped("name"):
            pay(mv, CASH, d)
        elif mv.partner_id.ref == "KH02":
            pay(mv, BANK, d)
    print("   hóa đơn", [(m.name, m.partner_id.ref, f"{m.amount_total:,.0f}", m.payment_state) for m in moves])


# ---------------------------------------------------------------------------------------------------------------
SAT, SUN, MON, TUE, WED, THU = (date(2026, 11, d) for d in (14, 15, 16, 17, 18, 19))


@section("00_dau_ky")
def _():
    # Kiểm kê chốt tồn lúc go-live (thứ Bảy 15:00)
    where = {"NVL khô": "Kho khô", "NVL mát": "Kho mát", "Bao bì": "Kho bao bì"}
    opening = {"RM01": 480, "RM02": 200, "RM03": 180, "RM04": 30, "RM05": 12, "RM06": 6, "RM07": 45, "RM08": 900,
               "RM09": 60, "RM10": 20, "RM11": 20, "RM12": 18, "RM13": 20, "RM14": 50, "RM15": 15, "RM16": 10,
               "RM17": 50, "PK01": 2500, "PK02": 700, "PK03": 400, "PK04": 500, "PK05": 250, "PK06": 1200}
    for code, qty in opening.items():
        p = P(code)
        vals = {"product_id": p.id, "location_id": L(where[p.categ_id.name]).id, "inventory_quantity": qty}
        if p.tracking == "lot":
            vals["lot_id"] = lot_for(p, at(SAT, 7) - timedelta(days=p.expiration_time // 3), f"DK-{code}").id
        env["stock.quant"].with_context(inventory_mode=True).create(vals).action_apply_inventory()
    # Thành phẩm tồn lúc kiểm kê (có lô cũ để thấy việc cận hạn)
    fg = [("FG02", 30, SAT, "TP nhiệt độ thường"), ("FG01", 20, SAT, "TP nhiệt độ thường"),
          ("FG07", 6, date(2026, 11, 15), "TP lạnh"), ("FG08", 60, date(2026, 7, 15), "TP nhiệt độ thường"),
          ("FG08", 120, date(2026, 11, 2), "TP nhiệt độ thường"), ("FG06", 25, date(2026, 11, 10), "TP nhiệt độ thường"),
          ("FG09", 150, date(2026, 10, 20), "TP đông"), ("FG10", 140, date(2026, 10, 22), "TP đông"),
          ("FG11", 90, date(2026, 11, 5), "TP đông"), ("FG12", 60, date(2026, 10, 28), "TP đông")]
    for code, qty, made, where_ in fg:
        p = P(code)
        lot = lot_for(p, at(made, 5), f"{code}-{made:%y%m%d}")
        env["stock.quant"].with_context(inventory_mode=True).create({
            "product_id": p.id, "location_id": L(where_).id, "lot_id": lot.id, "inventory_quantity": qty}).action_apply_inventory()
    moves = env["stock.move"].search([("is_inventory", "=", True)])
    moves.write({"date": at(SAT, 15)})
    moves.move_line_ids.write({"date": at(SAT, 15)})
    # Công nợ chuyển từ sổ cũ: hóa đơn tháng 10 chưa thu, hóa đơn NCC chưa trả (đối ứng TK 4211)
    for ref_, d, amount in (("KH03", date(2026, 10, 5), 18500000), ("KH04", date(2026, 10, 23), 30200000),
                            ("KH06", date(2026, 10, 26), 11400000)):
        inv = env["account.move"].create({
            "move_type": "out_invoice", "partner_id": C(ref_).id, "invoice_date": d, "ref": "Số dư đầu kỳ (sổ cũ)",
            "invoice_line_ids": [(0, 0, {"name": f"Công nợ chuyển từ sổ cũ - hàng giao tháng 10/2026",
                                         "quantity": 1, "price_unit": amount, "account_id": ACC_OPEN.id, "tax_ids": []})]})
        inv.action_post()
    for ref_, d, amount in (("NCC01", date(2026, 10, 25), 24600000), ("NCC03", date(2026, 11, 2), 9800000)):
        bill = env["account.move"].create({
            "move_type": "in_invoice", "partner_id": C(ref_).id, "invoice_date": d, "ref": "Số dư đầu kỳ (sổ cũ)",
            "invoice_line_ids": [(0, 0, {"name": "Công nợ NCC chuyển từ sổ cũ", "quantity": 1, "price_unit": amount,
                                         "account_id": ACC_OPEN.id, "tax_ids": []})]})
        bill.action_post()


@section("01_thu7_chot_don_thu2")
def _():
    # 16:00 thứ Bảy: đơn cho thứ Hai. KH03 đang có hóa đơn tháng 10 quá hạn → BH2b chặn
    take_orders(MON)
    so = env["sale.order"].search([("partner_id", "=", C("KH03").id), ("state", "=", "draft")], limit=1)
    if so:
        # Giám đốc gọi KH03, khách hứa chuyển 50% sáng thứ Hai → gắn nhãn duyệt, kinh doanh xác nhận lại
        so.tag_ids = [(4, APPROVED.id)]
        so.activity_ids.action_feedback(feedback="KH03 hứa chuyển 50% sáng thứ Hai; đồng ý giao.")
        so.action_confirm()
        so.date_order = at(SAT, 16, 10)
        print("   GĐ duyệt công nợ, xác nhận", so.name)


@section("02_thu7_ke_hoach_ca_dem_CN")
def _():
    # Thứ Bảy 16:00 lập kế hoạch cho ca đêm Chủ nhật 22:00 → 05:00 thứ Hai
    plan_production(SAT, MON)
    purchase(SAT, MON)


@section("03_thu2_van_hanh")
def _():
    deliver(MON)
    receive(MON, reject={"RM08": (60, "Trứng vỡ khi vận chuyển")})
    # 09:00 KH03 chuyển 50% hóa đơn tháng 10 (kế toán nhập từ sao kê ngân hàng)
    inv = env["account.move"].search([("partner_id", "=", C("KH03").id), ("ref", "=", "Số dư đầu kỳ (sổ cũ)")], limit=1)
    pay(inv, BANK, MON, amount=inv.amount_total / 2)
    end_of_day(MON)
    vendor_bills(MON)
    take_orders(TUE)
    # Ca đêm: mẻ bánh mì sandwich trắng thiếu 8 ổ (bột không nở) → đóng lệnh, không làm bù
    plan_production(MON, TUE, short={"FG02": 8}, scrap_after={"FG01": (5, "Rách bao bì khi đóng gói")})
    purchase(MON, TUE)


@section("04_thu3_van_hanh")
def _():
    # KH07 đóng cửa, không nhận hàng; KH04 nhận thiếu bánh mì sandwich vì mẻ thiếu
    deliver(TUE, actual={"KH07": {"FG01": 0, "FG04": 0}})
    receive(TUE)
    end_of_day(TUE)
    vendor_bills(TUE)
    # 17:00 thủ kho đếm nhanh thành phẩm: bánh tiệc trà thiếu 2 khay
    q = env["stock.quant"].search([("product_id", "=", P("FG06").id), ("location_id.usage", "=", "internal"),
                                   ("quantity", ">", 0)], limit=1)
    q.with_context(inventory_mode=True).write({"inventory_quantity": q.quantity - 2})
    q.with_context(inventory_mode=True).action_apply_inventory()
    env["stock.move"].search([("is_inventory", "=", True), ("product_id", "=", P("FG06").id)],
                             order="id desc", limit=1).write({"date": at(TUE, 17)})
    take_orders(WED)
    plan_production(TUE, WED)
    # Đơn bột tuần (giao thứ Năm) vượt 20 triệu → chờ giám đốc duyệt (để nguyên trạng thái chờ)
    flour = env["purchase.order"].with_user(U["muahang"]).create({
        "partner_id": C("NCC01").id, "date_order": at(TUE, 16, 40), "date_planned": at(THU, 7),
        "order_line": [(0, 0, {"product_id": P("RM01").id, "product_qty": 1000}),
                       (0, 0, {"product_id": P("RM02").id, "product_qty": 250})]})
    flour.with_user(U["muahang"]).button_confirm()  # NV mua hàng xác nhận → trên 20 triệu: chờ giám đốc duyệt
    flour.picking_ids.write({"scheduled_date": at(THU, 7)})
    print("   đơn bột tuần", flour.name, f"{flour.amount_total:,.0f}", flour.state)
    purchase(TUE, WED)


@section("05_thu4_buoi_sang")
def _():
    deliver(WED)
    receive(WED)
    vendor_bills(WED)
    # 10:30 KH01 trả 6 ổ bánh mì sandwich không bán hết (theo thỏa thuận) → Khu cách ly, giấy báo có
    out = env["stock.picking"].search([("partner_id", "=", C("KH01").id), ("picking_type_code", "=", "outgoing"),
                                       ("state", "=", "done")], order="id", limit=1)
    wiz = env["stock.return.picking"].with_context(active_id=out.id, active_ids=out.ids, active_model="stock.picking").create({})
    for line in wiz.product_return_moves:
        line.quantity = 6 if line.product_id.default_code == "FG02" else 0
    ret = wiz.action_create_returns()
    ret_pick = env["stock.picking"].browse(ret["res_id"])
    ret_pick.location_dest_id = L("Khu cách ly")
    ret_pick.move_ids.write({"location_dest_id": L("Khu cách ly").id})
    validate(ret_pick)
    backdate(ret_pick, at(WED, 10, 40))
    so = out.sale_id
    price = so.order_line.filtered(lambda l: l.product_id.default_code == "FG02").price_unit
    refund = env["account.move"].create({
        "move_type": "out_refund", "partner_id": C("KH01").id, "invoice_date": WED,
        "ref": f"Trả hàng {ret_pick.name}",
        "invoice_line_ids": [(0, 0, {"product_id": P("FG02").id, "quantity": 6, "price_unit": price})]})
    refund.action_post()
    print("   trả hàng", ret_pick.name, "giấy báo có", refund.name)


@section("06_thu4_buoi_chieu_dang_dien_ra")
def _():
    # Đang nhận đơn cho thứ Năm: phần lớn đã xác nhận, đơn trường học còn là báo giá chờ khách chốt
    take_orders(THU, confirm=True, skip=("KH05",))
    so = env["sale.order"].create({
        "partner_id": C("KH05").id, "client_order_ref": "Bữa phụ học sinh tuần 48 (chờ trường chốt số)",
        "commitment_date": at(THU, 6), "order_line": [(0, 0, {"product_id": P("FG01").id, "product_uom_qty": 90})]})
    # Đơn OEM bông lan 300 hộp giao thứ Sáu: route MTO tự sinh lệnh sản xuất riêng
    oem = env["sale.order"].create({
        "partner_id": C("KH06").id, "client_order_ref": "PO OEM-SAOMAI-1125", "commitment_date": at(date(2026, 11, 20), 9),
        "order_line": [(0, 0, {"product_id": P("FG05").id, "product_uom_qty": 300})]})
    oem.action_confirm()
    print("   báo giá", so.name, "| OEM", oem.name, oem.mrp_production_ids.mapped("name"))


def quarantine_lots(stages=("recall", "expired")):
    """Thủ kho chuyển các lô cần thu hồi / hết hạn đang ở kho bán được vào Khu cách ly (QT4)."""
    logs = env["bh.expiry.log"].search([("partner_id", "=", False), ("stage", "in", stages), ("state", "=", "todo")])
    quants = env["stock.quant"].search([("lot_id", "in", logs.lot_id.ids), ("quantity", ">", 0),
                                        ("location_id", "child_of", STOCK.id)])
    if not quants:
        return
    pick = env["stock.picking"].create({
        "picking_type_id": wh.int_type_id.id, "location_id": STOCK.id, "location_dest_id": L("Khu cách ly").id,
        "origin": "Cách ly hàng cận hạn / hết hạn",
        "move_ids": [(0, 0, {"product_id": q.product_id.id, "product_uom_qty": q.quantity,
                             "product_uom": q.product_id.uom_id.id, "location_id": q.location_id.id,
                             "location_dest_id": L("Khu cách ly").id}) for q in quants]})
    pick.action_confirm()
    for move, q in zip(pick.move_ids, quants):
        move.move_line_ids.unlink()
        env["stock.move.line"].create({"move_id": move.id, "picking_id": pick.id, "product_id": q.product_id.id,
                                       "product_uom_id": q.product_id.uom_id.id, "location_id": q.location_id.id,
                                       "location_dest_id": L("Khu cách ly").id, "lot_id": q.lot_id.id,
                                       "quantity": q.quantity})
        move.picked = True
    wizards(pick.button_validate())
    print("   cách ly", pick.name, [(q.lot_id.name, q.quantity) for q in quants])


@section("07_kiem_tra_can_han")
def _():
    env["stock.lot"]._bh_cron_check_expiry()
    quarantine_lots()
    print("   việc cận hạn:", [(l.lot_id.name, l.stage, l.partner_id.ref or "kho", l.qty) for l in env["bh.expiry.log"].search([])])


@section("08_api_token")
def _():
    client = env["bh.api.client"].create({"name": "App đặt hàng - Chuỗi trà sữa Lá Xanh", "partner_id": C("KH02").id,
                                          "user_id": env.ref("base.user_admin").id, "scope_stock": True,
                                          "scope_order": True, "scope_debt": True})
    wiz = env["bh.api.token.wizard"].browse(client.action_generate_token()["res_id"])
    ICP.set_param("bh_api.bank_webhook_secret", "bh-local-webhook-secret")
    ICP.set_param("bh_demo.api_token_kh02", wiz.token)


print("HOÀN TẤT TUẦN GO-LIVE")
