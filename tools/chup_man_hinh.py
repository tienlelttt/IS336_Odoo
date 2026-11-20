"""Chụp ảnh màn hình Odoo local cho báo cáo (Playwright + Edge cài sẵn, chạy ngầm).
Dùng: PYTHONIOENCODING=utf-8 python tools/chup_man_hinh.py  → baocao/hinh/*.png
Tài khoản thử nghiệm local admin/admin (xem data/README.md). Chạy lại sẽ ghi đè ảnh cũ.
"""
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "http://localhost:8069"
OUT = Path(__file__).resolve().parents[1] / "baocao" / "hinh"
OUT.mkdir(parents=True, exist_ok=True)

# (tệp ảnh, đường dẫn hoặc ("model", domain, action) để mở bản ghi đầu tiên, chờ thêm ms)
SHOTS = [
    ("01_cong_ty", "/odoo/action-base.action_res_company_form/1"),
    ("02_nguoi_dung", "/odoo/action-base.action_res_users"),
    ("03_kho_cau_hinh", "/odoo/action-stock.action_warehouse_form/1"),
    ("04_vi_tri_kho", "/odoo/action-stock.action_location_form"),
    ("05_bom_fg02", ("mrp.bom", [["product_tmpl_id.default_code", "=", "FG02"]], "mrp.mrp_bom_form_action")),
    ("06_khu_vuc_san_xuat", "/odoo/action-mrp.mrp_workcenter_action"),
    ("07_hop_dong_gia", ("purchase.requisition", [["vendor_id.ref", "=", "NCC01"]], "purchase_requisition.action_purchase_requisition")),
    ("08_khach_hang", "/odoo/action-base.action_partner_form"),
    ("09_bang_gia", "/odoo/action-product.product_pricelist_action2"),
    ("10_san_pham", "/odoo/action-sale.product_template_action"),
    ("11_don_ban", "/odoo/action-sale.action_orders"),
    ("12_don_bi_chan_S00020", ("sale.order", [["name", "=", "S00020"]], "sale.action_orders")),
    ("13_don_duyet_S00003", ("sale.order", [["name", "=", "S00003"]], "sale.action_orders")),
    ("14_dot_soan_theo_tuyen", "/odoo/action-stock_picking_batch.stock_picking_batch_action"),
    ("15_dot_soan_chi_tiet", ("stock.picking.batch", [["name", "=", "BATCH/OUT/00005"]], "stock_picking_batch.stock_picking_batch_action")),
    ("16_hoa_don_ban", "/odoo/action-account.action_move_out_invoice_type"),
    ("17_hoa_don_theo_so_giao", ("account.move", [["name", "=", "INV/2026/00012"]], "account.action_move_out_invoice_type")),
    ("18_thanh_toan", "/odoo/action-account.action_account_payments"),
    ("19_giay_bao_co", ("account.move", [["name", "=", "RINV/2026/00001"]], "account.action_move_out_refund_type")),
    ("20_don_mua", "/odoo/action-purchase.purchase_form_action"),
    ("21_don_mua_cho_duyet", ("purchase.order", [["name", "=", "P00004"]], "purchase.purchase_form_action")),
    ("22_phieu_nhap_trung", ("stock.picking", [["name", "=", "BH/IN/00003"]], "stock.action_picking_tree_all")),
    ("23_phieu_qc_danh_sach", "/odoo/action-quality_control_oca.action_qc_inspection"),
    ("24_phieu_qc_trung_khong_dat", ("qc.inspection", [["name", "=", "QC-000009"]], "quality_control_oca.action_qc_inspection")),
    ("25_hoa_don_ncc", "/odoo/action-account.action_move_in_invoice_type"),
    ("26_lenh_san_xuat", "/odoo/action-mrp.mrp_production_action"),
    ("27_lenh_san_xuat_thieu", ("mrp.production", [["name", "=", "WH/MO/00007"]], "mrp.mrp_production_action")),
    ("28_lenh_san_xuat_oem", ("mrp.production", [["name", "=", "WH/MO/00011"]], "mrp.mrp_production_action")),
    ("29_phe_pham", "/odoo/action-stock.action_stock_scrap"),
    ("30_lo_thanh_pham", ("stock.lot", [["name", "=", "FG02-261116"]], "stock.action_production_lot_form")),
    ("31_ton_kho_vi_tri", "/odoo/action-stock.action_view_quants"),
    ("32_lich_su_dieu_chuyen", "/odoo/action-stock.stock_move_line_action"),
    ("33_viec_can_han", "/odoo/action-bh_near_expiry.bh_expiry_log_action"),
    ("34_quy_tac_can_han", "/odoo/action-bh_near_expiry.bh_expiry_rule_action"),
    ("35_giao_dich_ngan_hang", "/odoo/action-bh_api.bh_bank_txn_action"),
    ("36_api_doi_tac", ("bh.api.client", [], "bh_api.bh_api_client_action")),
    ("37_quy_tac_tu_dong", "/odoo/action-base_automation.base_automation_act"),
    ("38_quy_tac_BH2b", ("base.automation", [["name", "like", "BH2b"]], "base_automation.base_automation_act")),
    ("39_phan_tich_ban_hang", "/odoo/action-sale.action_order_report_all"),
    ("40_phan_tich_hoa_don", "/odoo/action-account.action_account_invoice_report_all"),
    ("41_tai_khu_vuc_san_xuat", "/odoo/action-mrp.action_mrp_workcenter_load_report_graph"),
    ("42_web_trang_chu", "/"),
    ("43_web_cua_hang", "/shop"),
    ("44_web_lien_he", "/contactus"),
]


def rpc_first_id(page, model, domain):
    return page.evaluate("""async ([model, domain]) => {
        const r = await fetch('/web/dataset/call_kw', {method: 'POST', headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({jsonrpc: '2.0', method: 'call', params: {model, method: 'search', args: [domain],
            kwargs: {limit: 1}}})});
        const j = await r.json(); return (j.result || [])[0];
    }""", [model, domain])


def main():
    only = set(sys.argv[1:])
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="msedge", headless=True)
        ctx = browser.new_context(viewport={"width": 1440, "height": 900}, locale="vi-VN")
        page = ctx.new_page()
        page.goto(BASE + "/web/login")
        page.fill("input[name=login]", "admin")
        page.fill("input[name=password]", "admin")
        page.press("input[name=password]", "Enter")
        page.wait_for_url("**/odoo**", timeout=60000)
        # Màn hình Bổ sung hàng cần chạy hàm tạo đề xuất như khi bấm menu
        page.evaluate("""async () => fetch('/web/dataset/call_kw', {method: 'POST', headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({jsonrpc: '2.0', method: 'call', params: {model: 'stock.warehouse.orderpoint',
            method: 'action_open_orderpoints', args: [], kwargs: {}}})})""")
        shots = SHOTS + [("45_bo_sung_hang", "/odoo/action-stock.action_orderpoint_replenish")]
        for name, target in shots:
            if only and name not in only:
                continue
            if isinstance(target, tuple):
                model, domain, action = target
                rid = rpc_first_id(page, model, domain)
                if not rid:
                    print("  ! không có bản ghi", name)
                    continue
                url = f"/odoo/action-{action}/{rid}"
            else:
                url = target
            page.goto(BASE + url)
            try:
                if url.startswith("/odoo"):
                    # Giao diện Odoo giữ kết nối thông báo mở nên không chờ "networkidle"; chờ view hiện ra
                    page.wait_for_selector(".o_view_controller, .o_form_view, .o_list_view, .o_pivot, .o_graph_view",
                                           timeout=90000)
                    page.wait_for_function("!document.querySelector('.o_loading_indicator, .o-loading')", timeout=30000)
                else:
                    page.wait_for_load_state("networkidle", timeout=30000)
            except Exception as e:  # vẫn chụp để thấy trạng thái
                print("  ! chờ quá lâu", name, str(e)[:60])
            page.wait_for_timeout(2500)
            page.screenshot(path=str(OUT / f"{name}.png"), full_page=not url.startswith("/odoo"))
            print("chụp", name)
        # Website trên điện thoại
        m = browser.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True)
        mp = m.new_page()
        mp.goto(BASE + "/")
        mp.wait_for_load_state("networkidle")
        mp.screenshot(path=str(OUT / "46_web_dien_thoai.png"))
        print("chụp 46_web_dien_thoai")
        browser.close()


if __name__ == "__main__":
    main()
