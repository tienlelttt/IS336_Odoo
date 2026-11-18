# Hướng dẫn tự kiểm tra hệ thống trước khi viết báo cáo (bản 2 – tuần go-live)

Dữ liệu trong Odoo mô phỏng **tuần đầu đưa Odoo vào vận hành** của Bảo Hân: chuyển số dư thứ Bảy 14/11, vận hành thứ Hai 16, thứ Ba 17, và thứ Tư 18/11 đang diễn ra (chi tiết từng chứng từ: `scripts/README.md`). Thiết kế quy trình: `RA_SOAT_QUY_TRINH.md`. BPMN: `bpmn/QT1`–`QT5`.
Đánh dấu ☐ → ☑ khi thấy đúng; chỗ nào chưa ưng ghi vào bảng cuối file.

## 0. Khởi động

1. Mở Docker Desktop, chờ xanh. Git Bash tại `DoAn_HoanChinh/odoo_local`: `docker compose up -d`.
2. http://localhost:8069 → `admin` / `admin` (chỉ máy local).
3. Muốn xem đúng góc nhìn từng vai trò: đăng nhập tài khoản trong `data/README.md` (mật khẩu `BaoHan#2026`), ví dụ `quandoc@baohan.local` cho sản xuất.
4. Dữ liệu hỏng: `bash ../scripts/rebuild_all.sh` dựng lại từ đầu (khoảng 5 phút).

## 1. Cấu hình (TC mục 2–7)

| ☐ | Kiểm tra | Link | Phải thấy |
|---|---|---|---|
| ☐ | Công ty, logo, VND | http://localhost:8069/odoo/action-base.action_res_company_form | Công ty TNHH Bánh Bảo Hân, MST 0314345823, VND |
| ☐ | Người dùng | http://localhost:8069/odoo/action-base.action_res_users | 8 người dùng @baohan.local |
| ☐ | Kho | http://localhost:8069/odoo/action-stock.action_warehouse_form | Nhận hàng 1 bước, giao 1 bước, sản xuất 2 bước (cấp NVL rồi sản xuất) |
| ☐ | Vị trí | http://localhost:8069/odoo/action-stock.action_location_form | Trong BH/Tồn kho: Kho khô, Kho mát, Kho bao bì, TP thường / lạnh / đông. Ngoài Tồn kho: BH/Khu sản xuất, BH/Khu cách ly (hàng trả về, hết hạn không tính là hàng bán được) |
| ☐ | Định mức | http://localhost:8069/odoo/action-mrp.mrp_bom_form_action | 12 BoM; mở FG02: 100 ổ dùng 23 kg bột; tối đa 4 công đoạn; tiêu hao "cho phép kèm cảnh báo"; phụ phẩm vụn bánh |
| ☐ | Hợp đồng giá NCC | http://localhost:8069/odoo/action-purchase_requisition.action_purchase_requisition | 3 hợp đồng quý (NCC01, NCC03, NCC04) |
| ☐ | Khách theo tuyến | http://localhost:8069/odoo/action-base.action_partner_form | 8 khách mẫu, nhãn Tuyến 1/2/3, nhãn "Trả tiền mặt cho tài xế" |
| ☐ | Duyệt đơn mua | Mua hàng > Cấu hình > Cài đặt | Duyệt đơn mua 2 cấp, ngưỡng 20.000.000 |
| ☐ | Hóa đơn điện tử | Kế toán > Cấu hình > Cài đặt, tìm "Viettel" | Ô tài khoản Viettel S-Invoice (để trống: chưa có tài khoản thật) |
| ☐ | Mẫu chứng từ, mail | In một hóa đơn; Thiết lập > Kỹ thuật > Máy chủ gửi thư | Khung Boxed màu caramel; Gmail SMTP đang tắt (nhóm tự điền) |

## 2. QT1 – Nhận đơn, giao hàng, thu tiền (bpmn/QT1_ban_hang.png)

| ☐ | Bước | Link | Phải thấy |
|---|---|---|---|
| ☐ | Đơn theo ngày giao | http://localhost:8069/odoo/action-sale.action_orders → nhóm theo "Ngày giao hàng" | Đơn cố định mỗi ngày của từng khách |
| ☐ | Chặn công nợ | Mở S00020 (KH03) → bấm Xác nhận | Báo lỗi "khách có hóa đơn quá hạn…"; có việc "Duyệt công nợ" cho giám đốc |
| ☐ | Giám đốc duyệt | Mở S00003 | Có nhãn "Đã duyệt công nợ", lịch sử ghi lý do duyệt |
| ☐ | Đợt soạn theo tuyến | http://localhost:8069/odoo/action-stock_picking_batch.stock_picking_batch_action | 9 đợt BATCH/OUT (3 tuyến × 3 ngày) |
| ☐ | Ngoại lệ giao | Đơn S00011 (KH07), S00012 (KH08) | Đã hủy, lịch sử ghi "khách đóng cửa" / "hết hàng" |
| ☐ | Hóa đơn theo số giao | http://localhost:8069/odoo/action-account.action_move_out_invoice_type | INV/2026/00012 của KH04 thứ Ba: số bánh mì sandwich thấp hơn đơn |
| ☐ | Tiền mặt / chuyển khoản | http://localhost:8069/odoo/action-account.action_account_payments | Khoản tiền mặt của KH01, KH07, KH08; chuyển khoản KH02, KH03, KH04 |
| ☐ | Trả hàng | http://localhost:8069/odoo/action-account.action_move_out_refund_type | RINV/2026/00001 của KH01 (6 ổ) |
| ☐ | Đơn chưa lập hóa đơn | http://localhost:8069/odoo/action-sale.action_orders_to_invoice | Đơn giao sáng thứ Tư (kế toán chưa làm cuối ngày) |

## 3. QT2 – Mua nguyên liệu (bpmn/QT2_mua_hang.png)

| ☐ | Bước | Link | Phải thấy |
|---|---|---|---|
| ☐ | Đơn mua | http://localhost:8069/odoo/action-purchase.purchase_form_action | P00001 trứng (đã nhận thiếu 60 quả); P00002 bột tuần 24,6 triệu "Chờ duyệt" |
| ☐ | Duyệt | Đăng nhập giamdoc → mở P00002 → Phê duyệt | Chuyển thành đơn mua, sinh phiếu nhập cho thứ Năm |
| ☐ | Phiếu QC tại cửa | http://localhost:8069/odoo/action-quality_control_oca.action_qc_inspection | QC-000006 trứng "Không đạt" |
| ☐ | Nhận hàng | Mở P00001 > Phiếu nhập | BH/IN/00001: nhận 60 quả ít hơn đặt, có lô, hạn dùng, ghi chú lý do |
| ☐ | Hóa đơn NCC | http://localhost:8069/odoo/action-account.action_move_in_invoice_type | Công nợ đầu kỳ NCC01, NCC03 |

## 4. QT3 – Sản xuất cho quản đốc (bpmn/QT3_san_xuat.png)

Đăng nhập `quandoc@baohan.local` để thấy đúng màn hình của quản đốc.

| ☐ | Bước | Link | Phải thấy |
|---|---|---|---|
| ☐ | Bổ sung hàng (16:00) | Mở bằng **menu** Tồn kho > Vận hành > Bổ sung hàng (menu mới chạy hàm tạo đề xuất; link trực tiếp tới action sẽ trống) | Đề xuất cho thứ Năm: FG01 147, FG02 75, FG04 4, FG07 2 (đã kiểm 18/11) |
| ☐ | Lệnh sản xuất | http://localhost:8069/odoo/action-mrp.mrp_production_action | WH/MO/00001–00010 xong; 00011 OEM bông lan 300 hộp đã xác nhận |
| ☐ | Làm thiếu, đóng lệnh | WH/MO/00007 | Kế hoạch 66, thực tế 58; không có lệnh bổ sung |
| ☐ | Cấp NVL ra Khu sản xuất | Mở một MO → nút phiếu chuyển | Phiếu cấp NVL (lô FEFO) |
| ☐ | Lô thành phẩm, truy xuất | Lô FG02-261116 (http://localhost:8069/odoo/action-stock.action_production_lot_form) → Truy xuất nguồn gốc | Lô NVL đã dùng, các đơn đã giao |
| ☐ | Bánh lỗi | http://localhost:8069/odoo/action-stock.action_stock_scrap | SP/00001: 5 gói Hoppi rách bao bì, gắn WH/MO/00006 |
| ☐ | QC thành phẩm | Danh sách Inspections | QC-000001–000005, 000007–000011 thành phẩm "Đạt"; QC-000012 (lệnh OEM) chờ lấy mẫu |
| ☐ | Báo cáo quản đốc | Lệnh sản xuất → Pivot; http://localhost:8069/odoo/action-mrp.action_mrp_workcenter_load_report_graph | Sản lượng theo sản phẩm / ngày; tải khu vực |

## 5. QT4 – Kho, cận hạn, kiểm kê (bpmn/QT4_kho_can_han.png)

| ☐ | Bước | Link | Phải thấy |
|---|---|---|---|
| ☐ | Tồn theo vị trí, lô | http://localhost:8069/odoo/action-stock.action_view_quants | Nhóm theo vị trí; BH/Khu cách ly có 6 ổ FG02 (lô FG02-261114, KH01 trả) và 4 hộp FG07 hết hạn (phiếu BH/INT/00001) |
| ☐ | Việc cận hạn | http://localhost:8069/odoo/action-bh_near_expiry.bh_expiry_log_action | 10 việc: FG01/FG02 lô 14/11 thu hồi ở KH01, KH04 và ở kho; FG07 hết hạn ở kho và KH08; FG08 giảm giá; FG06 theo dõi; trứng, sữa theo dõi |
| ☐ | Quy tắc theo nhóm | http://localhost:8069/odoo/action-bh_near_expiry.bh_expiry_rule_action | Bánh mì tươi 40%, bánh lạnh 34%, NVL mát 50/15%, quy tắc chung 50/30/15% |
| ☐ | Đếm thành phẩm | http://localhost:8069/odoo/action-stock.stock_move_line_action → lọc điều chỉnh tồn | Bánh tiệc trà thiếu 2 khay ngày 17/11 |
| ☐ | Kiểm kê đầu kỳ | Như trên | Điều chỉnh tồn ngày 14/11 |

## 6. QT5 – Công nợ, thu tiền (bpmn/QT5_ke_toan_cong_no.png)

| ☐ | Kiểm tra | Link | Phải thấy |
|---|---|---|---|
| ☐ | Công nợ đầu kỳ | Hóa đơn INV/2026/00001–00003 | Tham chiếu "Số dư đầu kỳ (sổ cũ)"; KH03 trả một phần |
| ☐ | Webhook ngân hàng | http://localhost:8069/odoo/action-bh_api.bh_bank_txn_action | INV/2026/00007 của KH04 "Đã ghi nhận"; 1 giao dịch "Trùng" |
| ☐ | Tuổi nợ (OCA) | http://localhost:8069/odoo/action-account_financial_report.action_aged_partner_balance_wizard | KH03 quá hạn |
| ☐ | Sổ cái, cân đối phát sinh | http://localhost:8069/odoo/action-account_financial_report.action_trial_balance_wizard | Phát sinh phải thu, phải trả, doanh thu, tiền |
| ☐ | Nhắc nợ BH3 | Hóa đơn INV/2026/00001 (KH03) | Việc "Gọi nhắc nợ" cho kế toán sau khi tác vụ định kỳ chạy |

## 7. Import, báo cáo, website, API, tự động hóa

| ☐ | Kiểm tra | Cách làm | Phải thấy |
|---|---|---|---|
| ☐ | Import thử | Khách hàng > bánh răng > Nhập bản ghi > `data/khach_hang.csv` > Kiểm tra (không bấm Nhập) | Hợp lệ (đã chạy thử dry-run) |
| ☐ | Bộ lọc, nhóm, lưu | Đơn bán: lọc Tuyến 2, nhóm theo khách, Lưu tìm kiếm | Bộ lọc trong Yêu thích |
| ☐ | Phân tích bán / mua / hóa đơn | Menu Báo cáo của từng app | Pivot, đồ thị theo khách, sản phẩm, ngày |
| ☐ | Quy tắc tự động | http://localhost:8069/odoo/action-base_automation.base_automation_act | BH1, BH2a, BH2b, BH3, BH5 bật; BH4 tắt |
| ☐ | API đối tác | http://localhost:8069/odoo/action-bh_api.bh_api_client_action | Client KH02, nhật ký 401/200/201/422; đơn S00026, S00027 do app tạo |
| ☐ | Website | http://localhost:8069/ , /shop , /contactus | Theme Bảo Hân, hotline thật, cửa hàng có ảnh |
| ☐ | BPMN | Mở `bpmn/*.bpmn` bằng Camunda Modeler desktop | 5 file mở được; xuất ảnh chính thức |

## 8. Kết quả kiểm tra ngày 18/11

- 33 màn hình trong bảng: nạp action và toàn bộ view qua API của giao diện, không lỗi; số bản ghi khớp.
- Đã kiểm dữ liệu cụ thể: S00020 bị chặn đúng thông báo; S00003 có nhãn duyệt; INV/2026/00012 tính 52/56 ổ FG02 (theo số giao); P00002 chờ duyệt, người tạo NV mua; QC-000006 không đạt; WH/MO/00007 66 → 58, xong, không lệnh bổ sung; SP/00001 gắn WH/MO/00006; webhook 1 đã ghi nhận + 1 trùng; BH1, BH2a, BH2b, BH3, BH5 bật, BH4 tắt.
- Phát hiện và đã sửa: Khu cách ly nằm trong Tồn kho (hàng trả về bị tính là hàng bán được, lô hết hạn làm quản đốc không thấy cần sản xuất) → chuyển ra ngoài Tồn kho và thêm bước thủ kho cách ly lô (QT4).
- Chưa xem bằng mắt từng màn hình (khung trình duyệt bị ẩn làm giao diện tải rất chậm); nên mở thử khi chụp ảnh.

## 9. Giới hạn đã biết

- Ngày giờ chứng từ theo lịch giả lập; ngày tạo bản ghi và nhật ký là ngày chạy script.
- Thời gian công đoạn sản xuất ghi bằng định mức (thợ không bấm giờ – có chủ đích, xem RA_SOAT mục 3.3).
- Một số menu OCA chưa có tiếng Việt (Inspections, Tests, Aged Partner Balance).
- Ảnh website là ảnh minh họa có giấy phép; khách, NCC, nhân sự, giá, định mức là giả định.
- Hóa đơn điện tử mới cấu hình, chưa phát hành thật (cần tài khoản Viettel S-Invoice).

| # | Màn hình | Vấn đề | Muốn sửa thế nào |
|---|---|---|---|
| 1 | | | |
| 2 | | | |
