# LỜI CẢM ƠN

Nhóm xin cảm ơn thầy Văn Đức Sơn Hà và thầy Huy đã hướng dẫn môn Hoạch định nguồn lực doanh nghiệp, đặc biệt là bộ tiêu chí đồ án và các khóa học Odoo eLearning giúp nhóm hiểu cách một hệ thống ERP vận hành trong doanh nghiệp thật. Nhóm cũng cảm ơn các anh chị khóa trước đã chia sẻ báo cáo tham khảo.

Báo cáo sử dụng thông tin công khai của Công ty TNHH Bánh Bảo Hân. Các số liệu nội bộ (nhân sự, định mức, khách hàng, nhà cung cấp, giao dịch) là giả định phục vụ học tập và được ghi rõ trong từng phần.

[[PAGEBREAK]]

^^**NHẬN XÉT CỦA GIẢNG VIÊN HƯỚNG DẪN**

^^
^^
^^
^^
^^
^^
^^
^^
^^
^^
^^
^^
^^
^^

^^..…., ngày……tháng…..năm 2026
^^Người nhận xét
^^(Ký tên và ghi rõ họ tên)

[[PAGEBREAK]]

^^**BẢNG PHÂN CÔNG, ĐÁNH GIÁ THÀNH VIÊN**

Nhóm chia việc theo quy trình nghiệp vụ: mỗi thành viên phụ trách chính một quy trình (cấu hình, chạy thử, mô tả trong báo cáo, quay video), một phần phụ và một API khác nhau. Chi tiết và cơ sở chia việc ở mục 9.1.

| Họ và tên | MSSV | Phân công | Đánh giá |
|---|---|---|---|
| Lê Thị Thanh Tiền | 24521769 | QT3 Sản xuất theo mẻ (mục 5.3); QT4 phần cận hạn và module bh_near_expiry (5.4, 7.2); API JSON-2 (7.4) | Hoàn thành tốt nhiệm vụ được giao (34%) |
| Đoàn Thị Thùy Trang | 24521817 | QT1 Bán hàng (5.1); QT5 phần phải thu, đối soát ngân hàng (5.5); website (chương 6); module bh_api, tích hợp (7.3, 7.5) | Hoàn thành tốt nhiệm vụ được giao (33%) |
| Phạm Tuấn Hải | 24520442 | QT2 Mua hàng (5.2); QT4 phần kho, kiểm kê (5.4); QT5 phần phải trả (5.5); cấu hình kho (4.2); Automation Rules (7.1); API XML-RPC (7.4) | Hoàn thành tốt nhiệm vụ được giao (33%) |

Ngoài phần riêng, cả nhóm cùng làm: khảo sát và phân tích doanh nghiệp, thiết kế quy trình và BPMN, chương 1–3, chương 8–9, phụ lục, slide thuyết trình và hoàn thiện báo cáo.

[[PAGEBREAK]]

^^**MỤC LỤC**

[[TOC]]

[[PAGEBREAK]]

^^**DANH MỤC HÌNH**

[[DM_HINH]]

[[PAGEBREAK]]

^^**DANH MỤC BẢNG**

[[DM_BANG]]

[[PAGEBREAK]]

^^**DANH MỤC TỪ VIẾT TẮT VÀ THUẬT NGỮ**

| Từ viết tắt | Diễn giải |
|---|---|
| API | Application Programming Interface – giao diện lập trình ứng dụng |
| AVCO | Average Cost – phương pháp giá vốn bình quân gia quyền |
| BoM | Bill of Materials – định mức nguyên vật liệu |
| BPMN | Business Process Model and Notation – ký hiệu mô hình hóa quy trình nghiệp vụ |
| CRM | Customer Relationship Management – quản lý quan hệ khách hàng |
| ERP | Enterprise Resource Planning – hoạch định nguồn lực doanh nghiệp |
| FEFO / FIFO | First Expired, First Out – hết hạn trước xuất trước / First In, First Out – nhập trước xuất trước |
| FI | Finance – phân hệ tài chính kế toán |
| HACCP | Hazard Analysis and Critical Control Points – phân tích mối nguy và điểm kiểm soát tới hạn |
| MM | Material Management – quản lý vật tư |
| MO | Manufacturing Order – lệnh sản xuất |
| MRP | Manufacturing Resource Planning – hoạch định sản xuất (phân hệ Sản xuất của Odoo) |
| MST | Mã số thuế |
| MTO | Make to Order – sản xuất theo đơn |
| NCC | Nhà cung cấp |
| NVL | Nguyên vật liệu |
| O2C / P2P | Order to Cash – từ đơn hàng đến thu tiền / Procure to Pay – từ mua hàng đến trả tiền |
| OCA | Odoo Community Association – cộng đồng phát triển module mã nguồn mở cho Odoo |
| OEM | Original Equipment Manufacturer – gia công theo nhãn hàng của khách |
| PO / RFQ | Purchase Order – đơn mua / Request for Quotation – yêu cầu báo giá |
| QC | Quality Control – kiểm tra chất lượng |
| QT1–QT5 | Quy trình 1 đến quy trình 5 của đồ án |
| SaaS / PaaS | Software / Platform as a Service – phần mềm / nền tảng dạng dịch vụ |
| TK | Tài khoản kế toán |
| TO-BE | Quy trình sau khi áp dụng ERP |
| TP | Thành phẩm |
| VPS | Virtual Private Server – máy chủ ảo |
| Webhook | Cơ chế hệ thống ngoài gọi vào Odoo (hoặc ngược lại) khi có sự kiện |
| XML-RPC, JSON-RPC, JSON-2 | Các giao thức gọi hàm từ xa của Odoo; JSON-2 là API mới từ Odoo 19 |

[[PAGEBREAK]]

# TÓM TẮT BÁO CÁO

**Đề tài.** Triển khai hệ thống ERP Odoo 19 cho Công ty TNHH Bánh Bảo Hân – xưởng sản xuất bánh tươi, bánh cấp đông tại TP. Thủ Đức (MST 0314345823, công suất công bố khoảng 10.000 sản phẩm/ngày), bán sỉ cho quán, siêu thị, bếp ăn, trường học và gia công OEM.

**Vấn đề của doanh nghiệp.** Đơn hàng qua nhiều kênh nhưng tổng hợp bằng Excel; định mức không cập nhật nên không biết giá thành; bánh hạn dùng 3–5 ngày bị quá hạn ở kho và ở điểm bán; công nợ nhiều khách theo dõi rời rạc; kiểm kê lệch không rõ nguyên nhân.

**Những gì nhóm đã làm.**

- Phân tích nhịp vận hành một ngày của xưởng và thiết kế 5 quy trình theo đúng người làm, giờ làm: Bán hàng (QT1), Mua hàng (QT2), Sản xuất cho quản đốc (QT3), Kho – lô – cận hạn (QT4), Kế toán công nợ (QT5). Mỗi quy trình có BPMN mở được bằng Camunda, bảng đặc tả, ngoại lệ, báo cáo.
- Cài đặt Odoo 19 Community bằng Docker (một hệ thống duy nhất, tự host), bổ sung module cộng đồng OCA cho kiểm soát chất lượng và báo cáo tài chính; cấu hình VND, tiếng Việt, hệ thống tài khoản Việt Nam, 8 người dùng theo vai trò, kho nhận 1 bước – giao theo tuyến – sản xuất 2 bước, 12 định mức theo khối lượng thực tế, hợp đồng giá với nhà cung cấp, duyệt đơn mua trên 20 triệu.
- Dựng dữ liệu tuần đầu go-live (14–18/11/2026): chuyển số dư đầu kỳ, 27 đơn bán, 11 lệnh sản xuất, giao 9 đợt theo tuyến, 16 hóa đơn và giấy báo có, cùng các ngoại lệ thật (khách nợ quá hạn bị chặn đơn, trứng vỡ trả lại, mẻ bánh thiếu, khách đóng cửa, bánh trả về, hàng hết hạn vào khu cách ly).
- 6 quy tắc tự động (Automation Rules): chuẩn bị phiếu QC khi đơn mua xác nhận, chặn đơn khi nợ quá hạn, nhắc nợ, tạo phiếu QC thành phẩm, gửi webhook.
- 2 module tự viết: **bh_near_expiry** quản lý hàng cận hạn nhiều mức theo nhóm, tìm lô đang ở điểm bán để thu hồi (3 test đạt); **bh_api** cung cấp REST API có token băm, phạm vi quyền, giới hạn tần suất, nhật ký và webhook ngân hàng tự đối soát (12 test đạt).
- Theme website riêng (SCSS, QWeb, Be Vietnam Pro, đạt WCAG AA) có phân tích thiết kế, cổng đặt hàng cho khách sỉ.
- Tích hợp hệ thống ngoài: ngân hàng (webhook), app đặt hàng của khách (API), Google Sheets (Apps Script), Telegram.

**Kết quả chính.** Mỗi chứng từ trên Odoo thay một giấy tờ đang có; giá vốn ghi đúng 632/155 khi lập hóa đơn; lô thành phẩm truy được về lô nguyên liệu; quản đốc lập kế hoạch từ màn hình Bổ sung hàng trong vài phút.

**Phần việc cá nhân.** Mỗi thành viên phụ trách chính một quy trình và quay video riêng, đọc và gọi một API khác nhau (chương 7, chương 9).

[[SECTION]]
