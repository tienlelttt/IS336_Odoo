# Hướng dẫn tích hợp Odoo (Bảo Hân) với hệ thống bên ngoài

Tiêu chí: giao tiếp với ít nhất 3 hệ thống khác qua API/Webhook. Odoo chạy local ở http://localhost:8069, DB `baohan`.

| # | Hệ thống ngoài | Chiều | Cơ chế | Trạng thái kiểm thử |
|---|---|---|---|---|
| 1 | Cổng biến động số dư ngân hàng (định dạng SePay) | Ngân hàng → Odoo | Webhook vào `POST /api/bh/v1/webhook/bank` (module bh_api) | Đã chạy qua HTTP thật: khớp hóa đơn INV/2026/00004, tự ghi nhận thanh toán, gửi trùng bị bỏ qua, sai secret bị từ chối |
| 2 | App đặt hàng của khách sỉ (chuỗi trà sữa) | App → Odoo | REST API có token (module bh_api) | Đã chạy qua HTTP thật: xem sản phẩm, tạo đơn S00006, xem công nợ (scripts/api_demo_calls.py) |
| 3 | Google Sheets | Odoo → Sheets | Automation Rule BH4 gửi webhook → Google Apps Script | Phía Odoo đã kiểm bằng máy nhận tạm: nhận đúng JSON việc cận hạn. Phía Google cần nhóm tự triển khai (mục 2) |
| 4 | Telegram | Odoo → Telegram | Module bh_near_expiry gọi Bot API khi có việc cận hạn | Code có sẵn, cần bot token (mục 3) |

## 1. Webhook ngân hàng

1. Trong Odoo: Thiết lập > Kỹ thuật > Tham số hệ thống, đặt `bh_api.bank_webhook_secret` (môi trường local đang là `bh-local-webhook-secret`).
2. Ở SePay (hoặc dịch vụ tương tự): khai báo webhook URL `https://<địa-chỉ-public>/api/bh/v1/webhook/bank`, kiểu xác thực "API Key", giá trị là secret trên. Máy local cần đường hầm (ví dụ ngrok) để có địa chỉ public.
3. Khách chuyển khoản với nội dung chứa số hóa đơn (có hoặc không có dấu `/`). Odoo tự ghi nhận thanh toán. Xem kết quả: Thiết lập > API & Tích hợp > Giao dịch ngân hàng.
4. Thử không cần ngân hàng: `BH_API_TOKEN=<token> python scripts/api_demo_calls.py INV/2026/00004 3845600`.

## 2. Google Sheets (Apps Script)

1. Tạo Google Sheet mới, chọn Tiện ích mở rộng > Apps Script, dán nội dung `google_sheets_apps_script.gs`, đổi `SECRET`.
2. Triển khai > Tùy chọn triển khai mới > Loại: Ứng dụng web. Thực thi với tư cách: Tôi. Người có quyền truy cập: Bất kỳ ai. Sao chép URL dạng `https://script.google.com/macros/s/<ID>/exec`.
3. Trong Odoo: Tham số hệ thống `bh_demo.sheets_webhook_url` = `<URL ở bước 2>?key=<SECRET>`.
4. Chạy lại `scripts/automation_rules.py` (hoặc sửa URL trực tiếp trong quy tắc BH4 và bật quy tắc).
5. Kiểm thử: mở một lô có hạn dùng, bấm "Kiểm tra ngay" trên tab Cận hạn; dòng mới xuất hiện trong sheet `CanHan`.

## 3. Telegram

1. Trên Telegram, chat với @BotFather, lệnh `/newbot`, lấy token.
2. Thêm bot vào nhóm của quản lý, lấy `chat_id` (gửi tin trong nhóm rồi mở `https://api.telegram.org/bot<token>/getUpdates`).
3. Trong Odoo đặt tham số `bh_near_expiry.telegram_bot_token` và `bh_near_expiry.telegram_chat_id`.
4. Tác vụ "Bảo Hân: Kiểm tra hàng cận hạn hằng ngày" sẽ gửi tóm tắt mỗi khi có việc cận hạn mới.

Không đưa token, secret thật vào báo cáo hay mã nguồn nộp bài.
