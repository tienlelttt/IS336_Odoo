# CHƯƠNG 9. PHÂN CÔNG VÀ KẾT LUẬN

## 9.1. Phân công công việc

Nguyên tắc: mỗi thành viên phụ trách chính một quy trình (không trùng), quay video riêng, đọc và gọi một API khác nhau. Khối lượng cân theo độ khó đã chấm (tầm quan trọng, độ phức tạp cấu hình, ngoại lệ, tích hợp, kiến thức nền).

Bảng: Phân công công việc

| Hạng mục | 24521769 – Lê Thị Thanh Tiền | 24521817 – Đoàn Thị Thùy Trang | 24520442 – Phạm Tuấn Hải |
|---|---|---|---|
| Vai trò | B | A | C |
| Quy trình chính, video | QT3 Sản xuất | QT1 Bán hàng | QT2 Mua hàng |
| Phần phụ | QT4 phần cận hạn; module bh_near_expiry | QT5 phần phải thu, đối soát ngân hàng; module bh_api; website | QT4 phần kho, kiểm kê; QT5 phần phải trả, báo cáo tài chính; Automation Rules |
| API cá nhân | JSON-2 (đọc lệnh sản xuất, lô) | bh_api (đơn từ app khách, webhook ngân hàng) | XML-RPC (tạo đơn mua) |
| Phần báo cáo phụ trách | 5.3, 5.4 (cận hạn), 7.2, 7.4 (JSON-2) | 5.1, 5.5 (phải thu), chương 6, 7.3, 7.5 | 4.2 (kho), 5.2, 5.4 (kho, kiểm kê), 5.5 (phải trả), 7.1, 7.4 (XML-RPC) |
| Tỷ lệ đóng góp | 34% | 33% | 33% |

Phần làm chung cả nhóm: tóm tắt, chương 1–3, chương 8–9, phụ lục, slide thuyết trình.

Điểm độ khó (thang 5 cho mỗi tiêu chí, cộng 6 tiêu chí): QT1 27, QT3 25, QT5 23, QT4 22, QT2 20. Cộng cả phần phụ: A khoảng 39, B khoảng 36, C khoảng 42. A nặng về số ngoại lệ và điểm tích hợp; B là phần sản xuất cốt lõi của doanh nghiệp sản xuất; C điểm cao nhất nhưng phần phụ là thao tác ngắn, lặp lại (kiểm kê, thanh toán nhà cung cấp, chạy báo cáo).

## 9.2. Kiến thức đã học và áp dụng

Bảng: Kiến thức đã học và áp dụng

| Kiến thức môn học | Áp dụng trong đồ án |
|---|---|
| ERP tích hợp một cơ sở dữ liệu | Một đơn bán tác động kinh doanh, kho, sản xuất, kế toán |
| O2C, P2P, sản xuất | 5 quy trình theo vai trò và giờ làm thật |
| Phân tích nghiệp vụ, BPMN | 1 sơ đồ tổng quan và 5 sơ đồ quy trình có lane, ngoại lệ, mở bằng Camunda |
| Dữ liệu nền và giao dịch | Đặc tả, import, chuyển đổi dữ liệu go-live |
| Kế toán tích hợp | Giá vốn AVCO, ghi 632/155 khi lập hóa đơn; tiền đang chuyển 1131 |
| Phân quyền, kiểm soát nội bộ | Ma trận quyền, duyệt đơn mua, chặn đơn công nợ |
| Tùy biến ERP | 2 module Python, theme, Automation Rules |
| Tích hợp hệ thống | REST API có token, webhook, JSON-2, XML-RPC |
| Quản lý dự án | Lộ trình lai Waterfall + Scrum, go-live, quản lý thay đổi |

## 9.3. Ưu điểm

- Quy trình bám nhịp vận hành thật của một xưởng bánh nhỏ, mỗi chứng từ thay một giấy tờ có sẵn.
- Dữ liệu demo có ngoại lệ thật (nợ quá hạn, hàng vỡ, mẻ thiếu, khách đóng cửa, hàng trả, hết hạn) chứ không chỉ "luồng đẹp".
- Kiểm soát đặt đúng chỗ rủi ro: tiền, hạn dùng, an toàn thực phẩm.
- Module tự viết giải bài toán Odoo chuẩn chưa có (cận hạn tại điểm bán), có test tự động.
- Toàn bộ hệ thống dựng lại được bằng một lệnh, dữ liệu có thể kiểm chứng.

## 9.4. Nhược điểm và hạn chế

- Số liệu nội bộ là giả định; chưa phỏng vấn được doanh nghiệp thật, mới phỏng vấn mô phỏng (mục 1.6).
- Dùng Community nên không có Shop Floor, Planning, quét mã vạch, Studio, đối soát ngân hàng tự động; thời gian công đoạn ghi theo định mức.
- Dữ liệu demo chỉ một tuần go-live; báo cáo xu hướng dài hạn chưa có ý nghĩa.
- Hóa đơn điện tử, Google Sheets, Telegram mới ở mức cấu hình / code, chưa chạy với tài khoản thật.
- Website chạy local, ảnh minh họa.

## 9.5. Yếu tố thành công khi triển khai ERP

1. Thiết kế từ cách doanh nghiệp làm việc, không từ tính năng phần mềm.
2. Dữ liệu nền sạch và chuẩn hóa trước khi nhập.
3. Người dùng chính tham gia thử từ sớm (quản đốc, thủ kho).
4. Lãnh đạo dùng báo cáo của hệ thống để ra quyết định.
5. Phạm vi vừa sức: 5 phân hệ cần thiết, làm sâu.
6. Hiểu luồng tích hợp tài chính ở từng bước nghiệp vụ.

## 9.6. Bài học rút ra

- **Quản lý thay đổi:** một quy trình "đẹp" trên giấy (thợ bấm giờ, giám đốc duyệt mọi đơn) sẽ thất bại nếu không ai làm; phải hỏi "ai làm, lúc nào".
- **Làm sạch dữ liệu:** tên nhãn có dấu phẩy làm hỏng import; định mức sai làm giá thành sai.
- **Luồng tài chính:** cấu hình sai tài khoản tồn kho làm giá vốn thành phẩm ghi vào TK nguyên liệu – phát hiện nhờ đọc bút toán thật.
- **Hiểu phần mềm theo phiên bản:** Odoo 19 đổi nhiều (định giá tồn kho ghi khi lập hóa đơn, số ngày cảnh báo tính trước hạn dùng, quy tắc tái đặt hàng 0/0 bị xóa sau khi đặt).
- **Kiểm chứng:** mọi nội dung trong báo cáo đã đối chiếu với dữ liệu thật trong hệ thống.

## 9.7. Hướng phát triển

- Phỏng vấn Bảo Hân, thay giả định bằng số liệu thật.
- Đưa hệ thống lên VPS, tên miền, HTTPS; mở cổng đặt hàng cho khách sỉ.
- Kết nối tài khoản thật: hóa đơn điện tử Viettel, ngân hàng, Telegram, Google Sheets.
- Dự báo nhu cầu bánh tươi theo thứ trong tuần (máy học đơn giản) để gợi ý số mẻ.
- Cảm biến nhiệt độ kho mát, tủ đông gửi dữ liệu vào Odoo qua API.
- Nâng lên Enterprise / Odoo.sh khi cần Shop Floor, quét mã vạch.
