# Chạy trong Odoo shell, nối sau seed_data.py (bản 2 – thiết kế vận hành thực tế, xem RA_SOAT_QUY_TRINH.md):
#   cat scripts/seed_data.py scripts/seed_odoo.py | docker compose run --rm -T odoo -- shell -d baohan --no-http --addons-path=...
# Chạy lại nhiều lần không tạo trùng (tìm theo tên / mã trước khi tạo).
# use/removal/alert_time trong Odoo 19 là SỐ NGÀY TRƯỚC hạn sử dụng (không phải sau ngày sản xuất).
import base64
from datetime import date

IMG = "/mnt/extra-addons/theme_custom_website/static/src/img/"


def img(name):
    with open(IMG + name, "rb") as f:
        return base64.b64encode(f.read())


def ref(xmlid):
    rec = env.ref(xmlid, raise_if_not_found=False)
    if not rec:
        print("  ! không có", xmlid)
    return rec


def get_or_create(model, domain, vals):
    rec = env[model].with_context(active_test=False).search(domain, limit=1)
    if rec:
        rec.write(vals)
        return rec
    return env[model].create(vals)


company = env.company
vn = env.ref("base.vn")
vnd = env.ref("base.VND")
vnd.active = True

# 1. Công ty, tiền tệ, hệ thống tài khoản Việt Nam
print("1. Công ty và kế toán")
company.write({**COMPANY, "country_id": vn.id, "logo": img("logo_baohan.png")})
if company.chart_template != "vn":
    if env["account.move.line"].search_count([("company_id", "=", company.id)]):
        print("  ! đã có bút toán, không đổi được hệ thống tài khoản")
    else:
        env["account.chart.template"].try_loading("vn", company, install_demo=False)
print("  chart:", company.chart_template, "| tiền tệ:", company.currency_id.name)

# 2. Cài đặt chung
print("2. Cài đặt")
env["res.config.settings"].create({
    "group_stock_multi_locations": True,
    "group_stock_production_lot": True,
    "group_stock_adv_location": True,
    "group_lot_on_delivery_slip": True,
    "group_lot_on_invoice": True,
    "group_mrp_routings": True,
    "group_mrp_byproducts": True,
    "group_product_pricelist": True,
    "group_uom": True,
    "account_use_credit_limit": True,
    "po_order_approval": True,
    "po_double_validation": "two_step",
    "po_double_validation_amount": 20000000,
}).execute()
for lang in ("vi_VN", "en_US"):
    env["res.lang"]._activate_lang(lang)

layout = ref("web.external_layout_boxed")
company.write({
    "external_report_layout_id": layout.id if layout else company.external_report_layout_id.id,
    "primary_color": "#A84B16",
    "secondary_color": "#2E1F18",
    "report_footer": "Công ty TNHH Bánh Bảo Hân · MST 0314345823 · (028) 6274 7929 · Dữ liệu demo đồ án IS336",
})
get_or_create("ir.mail_server", [("name", "=", "Gmail SMTP - Bảo Hân")], {
    "name": "Gmail SMTP - Bảo Hân", "smtp_host": "smtp.gmail.com", "smtp_port": 587,
    "smtp_encryption": "starttls", "smtp_user": "dien-email-cua-nhom@gmail.com", "active": False})

# 3. Người dùng
print("3. Người dùng")
admin = env.ref("base.user_admin")
admin.write({"name": "Quản trị hệ thống", "image_1920": img("avatar_admin.png"), "lang": "vi_VN", "tz": "Asia/Ho_Chi_Minh"})
for login, name, job, groups in USERS:
    gids = [g.id for g in map(ref, groups) if g]
    user = env["res.users"].with_context(active_test=False).search([("login", "=", login)], limit=1)
    vals = {"name": name, "login": login, "email": login, "lang": "vi_VN", "tz": "Asia/Ho_Chi_Minh",
            "group_ids": [(4, g) for g in gids + [env.ref("base.group_user").id]]}
    if user:
        user.write(vals)
    else:
        user = env["res.users"].create({**vals, "password": TEST_PASSWORD})
    user.partner_id.function = job
# Quản đốc (Sản xuất: quản lý, Kho: người dùng) lập kế hoạch ở màn hình Bổ sung hàng: cần tạo/sửa/xóa quy tắc bổ sung
# (Odoo xóa quy tắc tạm 0/0 sau khi đặt lệnh).
# Odoo chỉ cho Kho: quản trị viên; cấp riêng quyền này thay vì cho quản đốc toàn quyền kho (điều chỉnh tồn, cấu hình).
get_or_create("ir.model.access", [("name", "=", "bh_orderpoint_mrp_manager")], {
    "name": "bh_orderpoint_mrp_manager", "model_id": env["ir.model"]._get_id("stock.warehouse.orderpoint"),
    "group_id": env.ref("mrp.group_mrp_manager").id,
    "perm_read": True, "perm_write": True, "perm_create": True, "perm_unlink": True})

# 4. Kho: nhận 1 bước (kiểm tại cửa), giao 1 bước theo tuyến, sản xuất 2 bước (cấp NVL ra Khu sản xuất)
print("4. Kho")
wh = env["stock.warehouse"].search([("company_id", "=", company.id)], limit=1)
wh.write({"name": "Xưởng Hiệp Bình Chánh", "code": "BH", "reception_steps": "one_step",
          "delivery_steps": "ship_only", "manufacture_steps": "pbm"})
if wh.pbm_loc_id:
    wh.pbm_loc_id.name = "Khu sản xuất"
loc = {}
for name in LOCATIONS:
    # Khu cách ly nằm ngoài Tồn kho: hàng trả về, hàng chờ hủy không được tính là hàng bán được
    parent = wh.view_location_id if name == "Khu cách ly" else wh.lot_stock_id
    loc[name] = get_or_create("stock.location", [("name", "=", name), ("location_id", "in", [wh.lot_stock_id.id, wh.view_location_id.id])],
                              {"name": name, "location_id": parent.id, "usage": "internal"})
fefo = env["product.removal"].search([("method", "=", "fefo")], limit=1)
mto = env.ref("stock.route_warehouse0_mto")
mto.active = True

# 5. Đơn vị tính, nhóm sản phẩm
print("5. Nhóm sản phẩm, đơn vị tính")
unit = env.ref("uom.product_uom_unit")
uoms = {"Đơn vị": unit, "kg": env.ref("uom.product_uom_kgm"), "L": env.ref("uom.product_uom_litre")}
thung = get_or_create("uom.uom", [("name", "=", "Thùng 20")], {"name": "Thùng 20", "relative_factor": 20, "relative_uom_id": unit.id})
categ = {}
for name, parent, put_loc, is_fefo in CATEGORIES:
    vals = {"name": name, "parent_id": categ[parent].id if parent else False,
            "removal_strategy_id": fefo.id if is_fefo else False}
    categ[name] = get_or_create("product.category", [("name", "=", name)], vals)
    categ[name].property_cost_method = "average"
    categ[name].property_valuation = "real_time"
    # Thành phẩm, phụ phẩm hạch toán TK 155; NVL, bao bì giữ TK 152 mặc định
    if name in ("Thành phẩm", "Phụ phẩm") or parent == "Thành phẩm":
        acc155 = env["account.account"].search([("code", "=", "155")], limit=1)
        if acc155:
            categ[name].property_stock_valuation_account_id = acc155
    if put_loc:
        get_or_create("stock.putaway.rule", [("category_id", "=", categ[name].id)], {
            "category_id": categ[name].id, "location_in_id": wh.lot_stock_id.id, "location_out_id": loc[put_loc].id})

# 6. Đối tác, bảng giá, tuyến
print("6. Nhà cung cấp, khách hàng, bảng giá, tuyến")
partner = {}
term30 = env.ref("account.account_payment_term_30days")
immediate = env.ref("account.account_payment_term_immediate")
for code, name in VENDORS:
    partner[code] = get_or_create("res.partner", [("ref", "=", code)], {
        "name": name, "ref": code, "is_company": True, "country_id": vn.id, "supplier_rank": 1,
        # NCC trứng nhận tiền mặt khi giao; NCC khác trả sau 30 ngày
        "property_supplier_payment_term_id": (immediate if code == "NCC04" else term30).id})
pricelist = {}
for name, disc in PRICELISTS:
    pl = get_or_create("product.pricelist", [("name", "=", name)], {"name": name, "currency_id": vnd.id})
    pl.item_ids.unlink()
    if disc:
        pl.item_ids = [(0, 0, {"applied_on": "3_global", "compute_price": "percentage", "percent_price": disc})]
    pricelist[name] = pl
route_tag = [get_or_create("res.partner.category", [("name", "=", r)], {"name": r}) for r in ROUTES]
cod_tag = get_or_create("res.partner.category", [("name", "=", "Trả tiền mặt cho tài xế")], {"name": "Trả tiền mặt cho tài xế"})
term30 = env.ref("account.account_payment_term_30days")
immediate = env.ref("account.account_payment_term_immediate")
for code, name, pl, term, limit, route, cod in CUSTOMERS:
    tags = [route_tag[route].id] + ([cod_tag.id] if cod else [])
    partner[code] = get_or_create("res.partner", [("ref", "=", code)], {
        "name": name, "ref": code, "is_company": True, "country_id": vn.id, "customer_rank": 1,
        "city": "TP. Hồ Chí Minh", "property_product_pricelist": pricelist[pl].id,
        "property_payment_term_id": (term30 if term == "30" else immediate).id,
        "use_partner_credit_limit": bool(limit), "credit_limit": limit, "category_id": [(6, 0, tags)],
        # KD1 phụ trách quán, tạp hóa; KD2 phụ trách siêu thị, bếp ăn, trường học, OEM
        "user_id": env["res.users"].search([("login", "=", "kinhdoanh1@baohan.local" if pl == "Giá sỉ quán"
                                             else "kinhdoanh2@baohan.local")], limit=1).id})
get_or_create("crm.tag", [("name", "=", "Đã duyệt công nợ")], {"name": "Đã duyệt công nợ"})

# 7. Sản phẩm
print("7. Sản phẩm")
prod = {}
route_mfg = ref("mrp.route_warehouse0_manufacture")
route_buy = ref("purchase_stock.route_warehouse0_buy")
for code, name, cat, price, days, web in FINISHED:
    routes = [route_mfg.id] + ([mto.id] if FG_PLANNING[code][0] == "oem" else [])
    vals = {"name": name, "default_code": code, "categ_id": categ[cat].id, "type": "consu", "is_storable": True,
            "sale_ok": True, "purchase_ok": False, "list_price": price, "uom_id": unit.id, "uom_ids": [(6, 0, [thung.id])],
            "invoice_policy": "delivery", "tracking": "lot", "use_expiration_date": True, "expiration_time": days,
            "use_time": max(round(days * .1), 1), "removal_time": max(round(days * .1), 1),
            "alert_time": max(round(days * .35), 1), "route_ids": [(6, 0, routes)], "is_published": web}
    if code in FG_IMAGES:
        vals["image_1920"] = img(FG_IMAGES[code])
    prod[code] = get_or_create("product.product", [("default_code", "=", code)], vals)
for code, name, cat, uom, cost, days, vendor, mn, mx in RAW:
    vals = {"name": name, "default_code": code, "categ_id": categ[cat].id, "type": "consu", "is_storable": True,
            "sale_ok": False, "purchase_ok": True, "purchase_method": "receive", "uom_id": uoms[uom].id,
            "standard_price": cost, "tracking": "lot" if days else "none", "use_expiration_date": bool(days),
            "expiration_time": days, "alert_time": max(round(days * .25), 1) if days else 0,
            "removal_time": max(round(days * .1), 1) if days else 0, "use_time": max(round(days * .1), 1) if days else 0,
            "route_ids": [(6, 0, [route_buy.id])]}
    p = prod[code] = get_or_create("product.product", [("default_code", "=", code)], vals)
    p.seller_ids.unlink()
    p.seller_ids = [(0, 0, {"partner_id": partner[vendor].id, "price": cost, "delay": VENDOR_LEAD_DAYS[vendor],
                            "currency_id": vnd.id})]
    # Tạo bằng admin: Odoo tự xóa quy tắc "thủ công" do superuser tạo khi đã đủ hàng (_unlink_processed_orderpoints)
    op_vals = {"product_id": p.id, "warehouse_id": wh.id, "location_id": wh.lot_stock_id.id,
               "product_min_qty": mn, "product_max_qty": mx, "trigger": "manual"}
    OP = env["stock.warehouse.orderpoint"].with_user(env.ref("base.user_admin")).with_context(active_test=False)
    op = OP.search([("product_id", "=", p.id)], limit=1)
    op.write(op_vals) if op else OP.create(op_vals)
code, name, cat, uom, cost = BYPRODUCT
prod[code] = get_or_create("product.product", [("default_code", "=", code)], {
    "name": name, "default_code": code, "categ_id": categ[cat].id, "type": "consu", "is_storable": True,
    "sale_ok": True, "purchase_ok": False, "uom_id": uoms[uom].id, "list_price": cost, "standard_price": cost,
    "invoice_policy": "delivery", "is_published": False})

# 8. Khu vực sản xuất, định mức, kế hoạch
print("8. Work center, BoM, quy tắc bổ sung thành phẩm")
wc = {}
for code, name, cost, _cap in WORKCENTERS:
    wc[code] = get_or_create("mrp.workcenter", [("code", "=", code)], {
        "name": name, "code": code, "costs_hour": cost, "time_efficiency": 100, "company_id": company.id})
for fg, qty, comps, ops, byp in BOMS:
    tmpl = prod[fg].product_tmpl_id
    bom = env["mrp.bom"].search([("product_tmpl_id", "=", tmpl.id)], limit=1)
    vals = {"product_tmpl_id": tmpl.id, "product_qty": qty, "type": "normal", "consumption": "warning",
            "bom_line_ids": [(5, 0, 0)] + [(0, 0, {"product_id": prod[c].id, "product_qty": q}) for c, q in comps],
            "operation_ids": [(5, 0, 0)] + [(0, 0, {"name": n, "workcenter_id": wc[w].id, "time_mode": "manual",
                                                    "time_cycle_manual": m, "sequence": i * 10})
                                            for i, (n, w, m) in enumerate(ops)],
            "byproduct_ids": [(5, 0, 0)] + ([(0, 0, {"product_id": prod["BP01"].id, "product_qty": byp,
                                                      "product_uom_id": uoms["kg"].id})] if byp else [])}
    if bom:
        bom.write(vals)
    else:
        bom = env["mrp.bom"].create(vals)
    tmpl.button_bom_cost()
    kind, mn, mx = FG_PLANNING[fg]
    op = env["stock.warehouse.orderpoint"].search([("product_id", "=", prod[fg].id)], limit=1)
    if kind == "oem":
        op.unlink()
    else:
        get_or_create("stock.warehouse.orderpoint", [("product_id", "=", prod[fg].id)], {
            "product_id": prod[fg].id, "warehouse_id": wh.id, "location_id": wh.lot_stock_id.id,
            "product_min_qty": mn, "product_max_qty": mx, "trigger": "manual"})

# 9. Hợp đồng giá theo quý (thỏa thuận mua hàng)
print("9. Hợp đồng giá với NCC")
q_start = date(date.today().year, ((date.today().month - 1) // 3) * 3 + 1, 1)
q_end = date(q_start.year + (q_start.month == 10), (q_start.month + 2) % 12 + 1, 1)
for vcode, lines in BLANKET_ORDERS:
    req = env["purchase.requisition"].search([("vendor_id", "=", partner[vcode].id),
                                              ("requisition_type", "=", "blanket_order")], limit=1)
    vals = {"vendor_id": partner[vcode].id, "requisition_type": "blanket_order", "date_start": q_start,
            "date_end": q_end, "currency_id": vnd.id,
            "line_ids": [(5, 0, 0)] + [(0, 0, {"product_id": prod[c].id, "product_qty": q, "price_unit": pr})
                                       for c, q, pr in lines]}
    if req:
        if req.state == "draft":
            req.write(vals)
    else:
        req = env["purchase.requisition"].create(vals)
    if req.state == "draft":
        req.action_confirm()
    for c, _q, pr in lines:  # giá hợp đồng cũng là giá NCC mặc định khi bổ sung hàng
        prod[c].seller_ids.filtered(lambda s: s.partner_id == partner[vcode]).price = pr

# 10. Kiểm soát chất lượng (OCA)
print("10. Phiếu kiểm tra chất lượng")
for name, questions in QC_TESTS:
    test = get_or_create("qc.test", [("name", "=", name)], {"name": name})
    test.test_lines.unlink()
    for i, (q, typ, mn, mx, _u) in enumerate(questions):
        vals = {"name": q, "type": typ, "sequence": i, "test": test.id}
        if typ == "quantitative":
            vals.update({"min_value": mn, "max_value": mx, "uom_id": unit.id})
        else:
            vals["ql_values"] = [(0, 0, {"name": "Đạt", "ok": True}), (0, 0, {"name": "Không đạt", "ok": False})]
        env["qc.test.question"].create(vals)
old_test = env["qc.test"].search([("name", "=", "Kiểm thành phẩm sau nướng (HACCP)")])
old_test.active = False

# 11. Quy tắc cận hạn theo nhóm
print("11. Quy tắc cận hạn theo nhóm")
for cat, stage, pct, disc, note in EXPIRY_RULES:
    get_or_create("bh.expiry.rule", [("categ_id", "=", categ[cat].id), ("stage", "=", stage)], {
        "name": f"{cat} - {stage} (còn ≤ {pct}%)", "categ_id": categ[cat].id, "stage": stage,
        "max_remaining_pct": pct, "discount_pct": disc, "note": note,
        "responsible_id": env["res.users"].search([("login", "=", "thukho@baohan.local")], limit=1).id})

# Quy tắc chung của module (categ trống) cũng giao việc cho thủ kho
env["bh.expiry.rule"].search([("categ_id", "=", False)]).write(
    {"responsible_id": env["res.users"].search([("login", "=", "thukho@baohan.local")], limit=1).id})

# 12. Website
print("12. Website")
website = env["website"].search([], limit=1)
website.write({"name": "Bảo Hân Bakery", "logo": img("logo_baohan.png"), "company_id": company.id})

env.cr.commit()
print("XONG. Sản phẩm:", len(prod), "| BoM:", env["mrp.bom"].search_count([]), "| Người dùng:",
      env["res.users"].search_count([("login", "like", "@baohan.local")]), "| Hợp đồng giá:",
      env["purchase.requisition"].search_count([]))
