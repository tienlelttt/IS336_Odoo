# CHƯƠNG 3. PHÂN TÍCH VÀ THIẾT KẾ GIẢI PHÁP

## 3.1. Nguyên tắc thiết kế

Nhóm thiết kế từ vị trí doanh nghiệp, không từ tính năng phần mềm:

1. Mỗi chứng từ trên Odoo thay một giấy tờ đang có (phiếu giao, phiếu nhập, sổ sản xuất, sổ công nợ). Không thêm bước nhập liệu mà không ai có thời gian làm.
2. Ai nhập, lúc nào, trên thiết bị gì phải rõ. Thợ làm bánh không dùng Odoo; quản đốc, thủ kho, kế toán, kinh doanh là người dùng.
3. Kiểm soát đặt ở nơi có rủi ro thật: tiền (công nợ, tiền mặt tài xế), hàng (hao hụt, hết hạn), an toàn thực phẩm (lô, nhiệt độ).
4. Không dùng Odoo cho việc làm tay nhanh hơn (không bấm giờ từng công đoạn, không duyệt từng đơn lặp lại).

## 3.2. Nhịp vận hành một ngày (TO-BE)

Bảng: Nhịp vận hành một ngày (TO-BE)

| Giờ | Bộ phận | Việc | Trên Odoo |
|---|---|---|---|
| 05:00 | Quản đốc, QC | Ghi sản lượng ca đêm, bánh lỗi; QC lấy mẫu | Hoàn tất lệnh sản xuất, phiếu loại bỏ, phiếu QC |
| 05:00–06:00 | Thủ kho | Soạn hàng theo tuyến | Đợt soạn hàng (batch) mỗi tuyến, lô FEFO |
| 06:00–10:00 | Tài xế | Giao, thu tiền mặt quán nhỏ, thu hồi bánh ế | Phiếu giao in sẵn |
| 07:00–09:00 | Thủ kho, QC | Nhận nguyên liệu tại cửa | Phiếu QC, phiếu nhập |
| 10:30 | Tài xế, kho, kế toán | Nộp tiền, xác nhận số thực giao, nhận hàng trả | Xác nhận phiếu giao, phiếu trả vào Khu cách ly |
| 08:00–16:00 | Kinh doanh | Nhận đơn ngày mai | Đơn bán; đơn của khách nợ quá hạn bị chặn |
| 16:00 | Quản đốc | Lập kế hoạch ca đêm | Bổ sung hàng → lệnh sản xuất; Mua nhận đề xuất mua |
| 16:30 | Thủ kho | Cấp nguyên liệu ra Khu sản xuất | Phiếu cấp NVL (sản xuất 2 bước) |
| 17:00 | Kế toán, thủ kho | Hóa đơn hàng loạt; ghi tiền mặt; đếm nhanh thành phẩm | Hóa đơn, thanh toán, điều chỉnh tồn |
| 23:00 | Hệ thống | Tính % hạn dùng còn lại mọi lô | Việc cận hạn cho sáng hôm sau |

Nhịp tuần: kiểm kê kho mát, đặt bột, thanh toán nhà cung cấp đến hạn. Nhịp tháng: kiểm kê toàn bộ, sao kê công nợ, báo cáo giá thành và hao hụt.

## 3.3. Những lựa chọn thiết kế và lý do

Bảng: Lựa chọn thiết kế và lý do thực tế

| Vấn đề | Cách làm trên Odoo | Lý do thực tế |
|---|---|---|
| Bánh tươi cho nhiều khách | Gom nhu cầu ngày mai, 1 lệnh sản xuất / sản phẩm / ca; MTO chỉ cho OEM | Xưởng nướng theo mẻ cho cả ngày |
| Thời gian công đoạn | Không bấm giờ; Odoo ghi theo định mức khi quản đốc hoàn tất lệnh | Thợ tay dính bột; Shop Floor không có ở Community |
| Duyệt đơn bán | Chỉ chặn khi khách nợ quá hạn / vượt hạn mức, giám đốc gắn nhãn để mở | Rủi ro thật là giao hàng cho khách nợ lâu |
| Nhận hàng | 1 bước, kiểm tại cửa trước khi xác nhận | Hàng mát không thể để khu chờ |
| Hàng không đạt | Không nhận, không tạo đơn chờ | NCC trứng không giao bù trong ngày |
| Giao hàng | Gom theo tuyến (batch), xác nhận khi tài xế về | 15–20 điểm/tuyến |
| Hóa đơn | Theo số đã giao, lập hàng loạt cuối ngày | Giao thiếu, trả hàng là chuyện hằng ngày |
| Mua hàng | Hợp đồng giá theo quý; đơn trên 20 triệu chờ giám đốc | NCC cố định, giá chốt theo quý |
| Hàng trả về, hết hạn | Khu cách ly nằm ngoài Tồn kho | Không được tính là hàng bán được |
| Cận hạn | Ngưỡng riêng theo nhóm bánh | Bánh mì 5 ngày khác cookies 6 tháng |

## 3.4. Cơ cấu tổ chức và ma trận phân quyền

Bảng: Ma trận phân quyền theo vai trò

| Vai trò (tài khoản) | Bán hàng | Mua hàng | Kho | Sản xuất | Chất lượng | Kế toán |
|---|---|---|---|---|---|---|
| Giám đốc | Quản trị | Quản trị (duyệt đơn mua) | Quản trị | Quản trị | Quản trị | Quản trị |
| Kinh doanh 1 | Chỉ chứng từ của mình | – | – | – | – | – |
| Kinh doanh 2 (trưởng nhóm) | Tất cả chứng từ | – | – | – | – | – |
| Mua hàng | – | Người dùng (tạo, xác nhận đơn) | Người dùng | – | – | – |
| Quản đốc | – | – | Người dùng | Quản trị | – | – |
| QC | – | – | Người dùng | – | Người dùng | – |
| Thủ kho | – | – | Người dùng | – | – | – |
| Kế toán | Xem tất cả | Người dùng | – | – | – | Quản trị |

Ma trận được hiện thực bằng nhóm quyền chuẩn của Odoo (res.groups) và gán trong `scripts/seed_odoo.py`. Kiểm soát chéo: kinh doanh không sửa giá ngoài bảng giá; mua hàng không tự duyệt đơn lớn; kho không tự áp dụng chênh lệch kiểm kê; kế toán chỉ trả tiền khi đối chiếu 3 bên.

## 3.5. Kiến trúc hệ thống

Bảng: Thành phần kiến trúc hệ thống

| Thành phần | Công nghệ | Vai trò |
|---|---|---|
| Máy chủ ứng dụng | Odoo 19 Community (Docker image odoo:19.0) | Toàn bộ phân hệ, website, API |
| Cơ sở dữ liệu | PostgreSQL 16 (Docker) | Một DB `baohan` dùng chung |
| Module bổ sung | OCA (quality_control_oca, account_financial_report, partner_statement) | Chất lượng, báo cáo tài chính |
| Module tự viết | bh_near_expiry, bh_api, theme_custom_website | Cận hạn, API, giao diện web |
| Hệ thống ngoài | Ngân hàng (webhook), app khách (REST), Google Sheets, Telegram | Tích hợp |
| Người dùng | Trình duyệt trên máy văn phòng, máy tính bảng ở kho | |

## 3.6. Đặc tả dữ liệu

### 3.6.1. Dữ liệu nền (master data)

Bảng: Đặc tả dữ liệu nền

| Đối tượng (model) | Trường chính | Đặc điểm riêng ở Bảo Hân |
|---|---|---|
| Sản phẩm (product.template) | Mã nội bộ, tên, nhóm, đơn vị, giá bán, giá vốn, loại theo dõi (lô), có hạn dùng, số ngày hạn dùng, ngày cảnh báo/rút kệ trước hạn, route, chính sách lập hóa đơn | 12 thành phẩm FG01–FG12 theo lô; 23 NVL, bao bì RM/PK; phụ phẩm BP01; hóa đơn theo số đã giao |
| Nhóm sản phẩm (product.category) | Tên, nhóm cha, chiến lược xuất, phương pháp giá vốn, định giá tồn kho, TK tồn kho | FEFO; AVCO; thành phẩm TK 155, NVL TK 152 |
| Khách hàng (res.partner) | Mã, tên, MST, bảng giá, điều khoản thanh toán, hạn mức nợ, nhân viên phụ trách, nhãn tuyến, nhãn trả tiền mặt | 8 khách mẫu chia 3 tuyến |
| Nhà cung cấp (res.partner) | Mã, tên, điều khoản thanh toán; trên sản phẩm: giá NCC, thời gian giao | NCC trứng trả tiền mặt, còn lại 30 ngày |
| Hợp đồng giá (purchase.requisition) | NCC, loại "Blanket Order", thời hạn quý, dòng (sản phẩm, số lượng dự kiến, đơn giá) | 3 hợp đồng NCC01, NCC03, NCC04 |
| Bảng giá (product.pricelist) | Tên, quy tắc (% giảm) | Sỉ quán; siêu thị – bếp ăn (–5%); OEM (–8%) |
| Định mức (mrp.bom) | Thành phẩm, số lượng mẻ, dòng NVL, công đoạn (khu vực, phút/mẻ), phụ phẩm, kiểu tiêu hao | 12 BoM; tiêu hao "cho phép kèm cảnh báo" |
| Khu vực sản xuất (mrp.workcenter) | Mã, tên, chi phí/giờ, hiệu suất | 5 khu vực; lò nướng là nút thắt |
| Kho, vị trí (stock.warehouse, stock.location) | Bước nhận/giao/sản xuất, vị trí con | Nhận 1 bước, giao 1 bước, sản xuất 2 bước; Khu cách ly ngoài Tồn kho |
| Quy tắc tái đặt hàng (stock.warehouse.orderpoint) | Sản phẩm, min, max, kích hoạt thủ công | NVL và hàng trữ; bánh tươi theo nhu cầu đơn |
| Phiếu kiểm tra (qc.test) | Câu hỏi định tính/định lượng, khoảng đạt | Kiểm NVL mát, NVL khô, mẫu thành phẩm |
| Quy tắc cận hạn (bh.expiry.rule) | Nhóm, mức, ngưỡng %, % giảm, người xử lý | Theo nhóm bánh |

### 3.6.2. Dữ liệu giao dịch (transaction data)

Bảng: Đặc tả dữ liệu giao dịch

| Chứng từ (model) | Trường chính |
|---|---|
| Đơn bán (sale.order) | Số, khách, nhân viên, ngày đặt, ngày giao, bảng giá, nhãn, dòng (sản phẩm, số lượng, đơn giá, đã giao, đã lập hóa đơn), trạng thái |
| Phiếu kho (stock.picking) | Số, loại (nhập/giao/nội bộ), đối tác, nguồn, vị trí đi/đến, ngày dự kiến/hoàn tất, dòng (sản phẩm, lô, số lượng) |
| Đợt soạn hàng (stock.picking.batch) | Số, mô tả tuyến, người phụ trách, các phiếu |
| Lô (stock.lot) | Tên lô, sản phẩm, hạn dùng, ngày rút kệ, ngày cảnh báo, mức cận hạn |
| Đơn mua (purchase.order) | Số, NCC, người mua, ngày, ngày giao dự kiến, dòng (sản phẩm, số lượng, đơn giá, đã nhận, đã lập hóa đơn), trạng thái (nháp, chờ duyệt, đã đặt) |
| Phiếu kiểm tra (qc.inspection) | Số, sản phẩm, số lượng, câu hỏi và kết quả, trạng thái (sẵn sàng, đạt, không đạt) |
| Lệnh sản xuất (mrp.production) | Số, sản phẩm, số lượng kế hoạch/thực tế, BoM, nguồn, lô thành phẩm, dòng tiêu hao NVL theo lô, phụ phẩm, công đoạn |
| Phiếu loại bỏ (stock.scrap) | Sản phẩm, lô, số lượng, vị trí, lệnh sản xuất liên quan, lý do |
| Hóa đơn / giấy báo có (account.move) | Số, khách/NCC, ngày, hạn thanh toán, dòng, thuế, trạng thái thanh toán |
| Thanh toán (account.payment) | Sổ nhật ký (tiền mặt/ngân hàng), số tiền, ngày, hóa đơn được đối soát |
| Việc cận hạn (bh.expiry.log) | Lô, nơi đang giữ (kho/khách), mức, % còn lại, số lượng, giá trị, cách xử lý, tổn thất |
| Giao dịch ngân hàng (bh.bank.txn) | Mã giao dịch, số tiền, nội dung, hóa đơn khớp, trạng thái |

## 3.7. Điểm tích hợp và bút toán tự động

Bút toán dưới đây lấy từ dữ liệu thật trong Odoo (hệ thống tài khoản Việt Nam cài sẵn).

Bảng: Điểm tích hợp và bút toán tự động

| Sự kiện | Phân hệ phát sinh → nhận | Odoo tự làm | Bút toán |
|---|---|---|---|
| Xác nhận đơn bán | Bán hàng → Kho, Sản xuất | Tạo phiếu giao; tồn dự báo giảm → đề xuất sản xuất | – |
| Lệnh sản xuất thiếu NVL | Sản xuất → Mua hàng | Đề xuất mua theo giá hợp đồng | – |
| Xác nhận đơn mua | Mua hàng → Chất lượng | BH1 chuẩn bị phiếu QC | – |
| Xác nhận phiếu nhập | Kho → Mua hàng | Cập nhật số đã nhận trên đơn mua | – |
| Hóa đơn nhà cung cấp | Mua hàng → Kế toán | Số lượng theo số đã nhận | Nợ 152, Nợ 1331 / Có 3311 |
| Xác nhận lệnh sản xuất | Sản xuất → Kho, Chất lượng | Phiếu cấp NVL; BH5 phiếu QC | – |
| Hoàn tất lệnh sản xuất | Sản xuất → Kho | Lô thành phẩm có hạn dùng; giá vốn AVCO | – (Perpetual at invoicing) |
| Xác nhận phiếu giao | Kho → Bán hàng | Số đã giao trên đơn bán | – |
| Hóa đơn bán | Bán hàng → Kế toán | Theo số đã giao | Nợ 1311 / Có 511, Có 33311; Nợ 632 / Có 155 |
| Thanh toán (chuyển khoản / tiền mặt) | Ngân hàng → Kế toán | Webhook ghi nhận | Nợ 1131 (tiền đang chuyển) / Có 1311 |
| Giấy báo có (hàng trả) | Kế toán | Giảm doanh thu, nhận lại hàng | Nợ 511, Nợ 33311 / Có 1311; Nợ 155 / Có 632 |
| Khách nợ quá hạn | Kế toán → Bán hàng | BH2b chặn đơn mới | – |
| Lô chạm ngưỡng | Kho → Bán hàng, Kế toán | Việc cận hạn; tổn thất khi hủy | – |
