# CHƯƠNG 9. PHÂN CÔNG VÀ KẾT LUẬN

## 9.1. Phân công công việc

Nguyên tắc: mỗi thành viên phụ trách chính một quy trình (không trùng), quay video riêng, đọc và gọi một API khác nhau. Khối lượng cân theo độ khó đã chấm (tầm quan trọng, độ phức tạp cấu hình, ngoại lệ, tích hợp, kiến thức nền).

| Hạng mục | 24521769 – Lê Thị Thanh Tiền | 24521817 – Đoàn Thị Thùy Trang | 24520442 – Phạm Tuấn Hải |
|---|---|---|---|
| Quy trình chính, video | [QT gán] | [QT gán] | [QT gán] |
| Phần phụ | | | |
| API cá nhân | | | |
| Chương báo cáo | | | |
| Tỷ lệ đóng góp | % | % | % |

Gợi ý theo vai trò (nhóm tự gắn tên theo thế mạnh):

| Vai trò | Quy trình chính | Phần phụ | API cá nhân |
|---|---|---|---|
| A | QT1 Bán hàng | QT5 phần phải thu, đối soát ngân hàng; Module API; Website | bh_api |
| B | QT3 Sản xuất | QT4 phần cận hạn (module bh_near_expiry) | JSON-2 |
| C | QT2 Mua hàng | QT4 phần kho, kiểm kê; QT5 phần phải trả, báo cáo tài chính; Automation | XML-RPC |

## 9.2. Kiến thức đã học và áp dụng

| Kiến thức môn học | Áp dụng trong đồ án |
|---|---|
| ERP tích hợp một cơ sở dữ liệu | Một đơn bán tác động kinh doanh, kho, sản xuất, kế toán |
| O2C, P2P, sản xuất | 5 quy trình theo vai trò và giờ làm thật |
| Phân tích nghiệp vụ, BPMN | 5 sơ đồ có lane, ngoại lệ, mở bằng Camunda |
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

- Số liệu nội bộ là giả định; chưa phỏng vấn được doanh nghiệp (bộ câu hỏi ở Phụ lục A).
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
