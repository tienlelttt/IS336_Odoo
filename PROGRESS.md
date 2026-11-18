# Tiến độ hoàn thiện đồ án ERP – Nhóm 06 (IS336.R12)

Đọc file này trước khi làm tiếp. Hướng dẫn tự kiểm tra: HUONG_DAN_KIEM_TRA.md; cài đặt: HUONG_DAN_CAI_DAT.md; ôn vấn đáp: KIEN_THUC_VAN_DAP.md.

## Quyết định đã chốt (18/11/2026)
- Case: Công ty TNHH Bánh Bảo Hân (cơ sở thật, MST 0314345823, TP Thủ Đức). Thông tin công khai có trích nguồn; số liệu nội bộ ghi "(giả định)". KHÔNG viết biên bản phỏng vấn giả. Bộ câu hỏi: baocao/phuluc_A_phong_van.md.
- Nhóm 3 người: 24521769 (Lê Thị Thanh Tiền), 24521817 (Đoàn Thị Thùy Trang), 24520442 (Phạm Tuấn Hải).
- Nền tảng: CHỈ Odoo 19 Community local bằng Docker (người dùng quyết định, không dùng edu online). Quality/Planning/Barcode/Studio không có trong Community.
- Không đưa website lên Internet dưới tên Bảo Hân khi chưa được doanh nghiệp đồng ý.

- Phạm vi chốt lại (18/11, bản 2 "sát thực tế"): 5 phân hệ Bán, Mua, Sản xuất, Kho, Kế toán; thiết kế theo nhịp một ngày vận hành, Odoo sản xuất dành cho QUẢN ĐỐC (thợ không dùng Odoo). Chi tiết, bảng "bỏ/sửa vì sao", chấm điểm độ khó và phân công A/B/C: RA_SOAT_QUY_TRINH.md. BPMN QT1–QT5 đã vẽ lại theo bản 2.
- ĐÃ áp dụng bản 2 lên Odoo (18/11): DB baohan dựng lại từ đầu bằng scripts/rebuild_all.sh (bản 1 sao lưu ở backups/). Dữ liệu = tuần đầu go-live 14–18/11 (scripts/README.md). Hướng dẫn kiểm tra: HUONG_DAN_KIEM_TRA.md (bản 2).
- Kỹ thuật: Odoo kiểm ngày rút khỏi kệ theo giờ thật → không giả lập lùi nhiều tuần; quy tắc bổ sung 0/0 bị Odoo xóa sau khi đặt → dùng _get_orderpoint_action như màn hình Bổ sung hàng; xác nhận PO làm Odoo tính lại ngày giao → đặt lại scheduled_date; admin tự duyệt PO → tạo bằng user muahang; OCA qc.inspection.line phải điền question_type, min/max, possible_ql_values.
- Đã kiểm trong Odoo 19 Community: không có Shop Floor (mrp_workorder) và Production Analysis (mrp.report); có Gộp lệnh, đóng lệnh không backorder, 3 mức tiêu hao; tồn dự báo trừ đơn bán; có sẵn stock_picking_batch, purchase_requisition, l10n_vn_edi_viettel (chưa cài).

## Môi trường
- odoo_local/docker-compose.yml: Postgres 16 + odoo:19.0, cổng 8069, mount ./addons và ./oca.
- DB chính: `baohan` (đã cài sale_management, purchase, stock, mrp, account, l10n_vn, crm, website_sale, base_automation, product_expiry, bh_near_expiry, bh_api, theme_custom_website; tiếng Việt). Theme đã áp lên website.
- Chỉ còn DB `baohan` (DB thử bh_test, np_test đã xóa 19/11). Server chạy với `--db-filter=^baohan$` để API/webhook không bị hỏi chọn DB.
- Odoo 19: định giá kho 'Perpetual (at invoicing)' ghi bút toán kho lúc lập hóa đơn. use/removal/alert_time là số ngày TRƯỚC hạn dùng.
- Lệnh chạy từ Git Bash phải có `MSYS_NO_PATHCONV=1`. Cài/test module: `docker compose run --rm -T odoo -- -d <db> -i <module> --test-tags /<module> --stop-after-init` (cách truyền mật khẩu DB trên dòng lệnh bị bộ phân loại quyền chặn).
- Đổi SCSS mà trang vẫn báo lỗi cũ: `docker compose restart odoo` rồi xóa ir_attachment có url '/web/assets/%'. libsass của Odoo không tính được clamp() trộn rem+vw → bọc unquote("clamp(...)").
- OCA 19.0 clone ở odoo_local/oca. Người dùng đã cho phép; đã cài vào `baohan`: quality_control_oca, account_financial_report, partner_statement (+ date_range, report_xlsx, report_xlsx_helper). Bỏ mrp_multi_level vì cần stock_warehouse_calendar (repo OCA khác). Khi chạy `docker compose run ... -u/-i` trên `baohan` PHẢI kèm --addons-path có /mnt/oca/..., nếu không Odoo báo thiếu module.

## Trạng thái
| Hạng mục | Trạng thái | Vị trí |
|---|---|---|
| Chương 1 + Phụ lục A | Xong (đã sửa phạm vi kỹ thuật sang local) | baocao/chuong1.md (nằm trong Report - Nhóm 06.docx) |
| Module cận hạn | Xong, 3 test đạt | odoo_local/addons/bh_near_expiry |
| Module API + webhook ngân hàng | Xong, 12 test đạt | odoo_local/addons/bh_api |
| Theme website | Xong, làm lại bản ấm hơn với 7 ảnh bánh giấy phép Pexels/Unsplash (nguồn: static/src/img/CREDITS.md); đã kiểm desktop 1280px và mobile 375px | odoo_local/addons/theme_custom_website |
| Master data + cấu hình cơ bản | Xong: scripts/seed_data.py + seed_odoo.py (chạy lại không trùng), file import ở data/ (dry-run đạt), tài khoản thử ở data/README.md | data/, scripts/ |
| Kịch bản demo | Bản 2: scripts/demo_week.py (tuần go-live). bản 1 đã xóa | scripts/ |
| Automation Rules | Bản 2: BH1 (QC tại cửa), BH2a/BH2b (chặn đơn khi nợ quá hạn), BH3, BH4 (tắt), BH5 (QC thành phẩm); đã chạy thật trong tuần go-live | scripts/automation_rules.py |
| Tích hợp hệ thống ngoài | Ngân hàng (webhook) và app đặt hàng (API) chạy thật; Google Sheets: Apps Script + hướng dẫn, phía Odoo đã kiểm với máy nhận tạm; Telegram: code, chờ token | integrations/ |
| BPMN 5 quy trình | Xong (QT3 vẽ lại theo mẻ hằng ngày, thêm QT5 kế toán công nợ): bpmn/QT1–QT4 .bpmn + .png xem trước (tools/bpmn_gen.py, tools/bpmn_specs.py); bpmn-js nạp 0 cảnh báo. Ảnh nộp bài nên xuất lại từ Camunda Modeler desktop | bpmn/ |
| Báo cáo đầy đủ | Xong bản 1: baocao/00_mo_dau … chuong9, tham khảo, phụ lục → Report - Nhóm 06.docx (tools/md2docx.py, mục lục tự động). Ảnh: tools/chup_man_hinh.py → baocao/hinh | baocao/, Report - Nhóm 06.docx |
| Hướng dẫn cài đặt, làm lại, quay video | Xong: HUONG_DAN_CAI_DAT.md | |
| Tài liệu ôn vấn đáp | Xong: KIEN_THUC_VAN_DAP.md | |
| API cá nhân 3 bạn | Xong, chạy thật: bh_api (api_demo_calls.py), JSON-2 và XML-RPC (scripts/api_ca_nhan/). API key thử: tham số bh_demo.api_key_admin | scripts/ |
| Ảnh chụp màn hình | 46 ảnh tự động (Playwright + Edge), admin/admin local | baocao/hinh |

Công cụ: tools/md2docx.py dựng docx từ markdown theo style file Chương 1 gốc.

Lưu ý kỹ thuật thêm:
- Server action của Automation chạy trong sandbox: không gán thuộc tính (`rec.x = ...`), dùng `rec.write({...})`; không gọi hàm bắt đầu bằng `_`.
- OCA quality_control 19.0: `unlink`/`action_cancel` chỉ chạy từng bản ghi; product_id của phiếu QC tính từ `object_id` ('product.product,<id>').
- Trạng thái 'done' của phiếu kho được ghi 2 lần nên quy tắc on_state_set có thể chạy 2 lần: code BH1 đã chống trùng.

- 18/11 tối: kiểm tra lại toàn hệ thống (33 màn hình), sửa Khu cách ly ra ngoài Tồn kho + bước cách ly lô; gán nhân viên kinh doanh, mua hàng; TK tồn kho thành phẩm 155 (trước đó giá vốn ghi Có 152). Đã dựng lại DB bằng rebuild_all.sh sau các sửa này.
- 19/11: dọn thư mục – đã chuyển vào Thùng rác: file khóa Word, __pycache__, bpmn/kiem_tra_bpmn.html, Chuong1_BaoHan.docx, scripts/demo_transactions.py, KIEM_TRA_YEU_CAU.md, ../DANH_GIA_DE_TAI_va_DE_XUAT.md, backups/baohan_ban1 (dump bản 1). Đã drop DB bh_test, np_test.

- 19/11: repo git tại DoAn_HoanChinh (remote tienlelttt/IS336_Odoo, OCA là submodule, đã push nhánh main 19/11). Đã điền tên Đoàn Thị Thùy Trang (24521817), Phạm Tuấn Hải (24520442) vào bìa, chương 9, README; dựng lại docx. Còn thiếu: gán quy trình/vai trò và % đóng góp ở chương 9. Phụ lục B đã viết thành phỏng vấn mô phỏng 32 câu (ghi rõ là mô phỏng, không phải lời doanh nghiệp), số liệu khớp Chương 1 và seed_data; sửa ví dụ BoM Chương 1 thành 23 kg bột/100 ổ cho khớp DB.

- 19/11 (phiên sau): đã điền phân công chương 9 theo lựa chọn của nhóm: A – Đoàn Thị Thùy Trang (QT1, phải thu, bh_api, website), B – Lê Thị Thanh Tiền (QT3, cận hạn, JSON-2), C – Phạm Tuấn Hải (QT2, kho/kiểm kê, phải trả, Automation, XML-RPC); đóng góp Tiền 34%, Trang 33%, Hải 33%. Ghi tên vào bảng API 7.4.2, README, RA_SOAT mục 6.2 (Website chuyển sang A). Đã dựng lại docx. Việc tiếp: mở Word cập nhật mục lục, soát trang, xuất PDF.
- 19/11: đổi định dạng báo cáo theo mẫu IS201 người dùng chỉ định (Drive, file 57 MB ở DoAn_Nhom6/, ngoài repo): tools/tao_mau_bao_cao.py tạo tools/mau_bao_cao.docx (bìa có khung, logo; lề 3,5/2/3/3,5 cm; số trang từ chương 1). Bỏ baocao/00_bia.md (bìa nằm trong mẫu, có thêm dòng GV hướng dẫn). Phần đầu theo mẫu: Lời cảm ơn → Nhận xét GV → Bảng phân công, đánh giá → Mục lục → Danh mục hình (52 hình, style Caption) → Tóm tắt. Không có danh mục bảng vì bảng chưa có chú thích. Người dùng yêu cầu chỉ làm Word, KHÔNG xuất PDF. Chưa soát hiển thị trong Word.
- 19/11: sửa định dạng theo phản hồi: danh sách thụt treo 0,9 cm giãn 1,5 (bỏ List Paragraph của mẫu); bảng vừa khổ 15,5 cm, cột theo độ dài chữ, lặp dòng tiêu đề, chữ trong ô giãn 1,15; ảnh rộng 15,5 cm. Chú thích 'Hình x.y:' và 'Bảng x.y:' đánh số bằng trường SEQ ( 1 đầu mỗi chương); 58 bảng có chú thích (dòng 'Bảng: ...' trong md; bảng phân công ở trang đầu không đánh số như mẫu); Danh mục hình, Danh mục bảng là TOC \c. Logo mờ nền trang là của header mẫu, giữ nguyên.
