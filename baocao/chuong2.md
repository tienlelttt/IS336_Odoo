# CHƯƠNG 2. CƠ SỞ LÝ THUYẾT

## 2.1. Hệ thống hoạch định nguồn lực doanh nghiệp (ERP)

### 2.1.1. Khái niệm

ERP (Enterprise Resource Planning) là hệ thống phần mềm tích hợp các nghiệp vụ cốt lõi của doanh nghiệp – bán hàng, mua hàng, kho, sản xuất, kế toán, nhân sự – trên **một cơ sở dữ liệu chung**. Một nghiệp vụ phát sinh ở bộ phận này tự động cập nhật dữ liệu cho bộ phận khác: xác nhận giao hàng làm giảm tồn kho, đồng thời tạo căn cứ lập hóa đơn và ghi giá vốn.

### 2.1.2. Đặc điểm

| Đặc điểm | Ý nghĩa với Bảo Hân |
|---|---|
| Tích hợp | Một đơn bán đi qua kinh doanh, kho, sản xuất, kế toán mà không nhập lại |
| Dữ liệu dùng chung | Kinh doanh thấy tồn kho thật khi chốt đơn; quản đốc thấy nhu cầu từ đơn đã xác nhận |
| Mô-đun hóa | Chỉ cài 5 phân hệ cần thiết, mở rộng sau |
| Theo quy trình chuẩn | Áp dụng thực hành tốt có sẵn trong phần mềm (FEFO, đối chiếu 3 bên) |
| Thời gian thực | Công nợ, tồn, giá vốn cập nhật ngay khi chứng từ được xác nhận |

### 2.1.3. Lợi ích và hạn chế

Lợi ích: giảm nhập liệu trùng, kiểm soát chéo giữa bộ phận, truy xuất nguồn gốc, báo cáo tức thời, chuẩn hóa quy trình. Hạn chế: chi phí và thời gian triển khai, đòi hỏi thay đổi thói quen làm việc (quản lý thay đổi), dữ liệu đầu vào phải sạch, có thể không vừa với quy trình đặc thù nếu không tùy chỉnh.

### 2.1.4. Các nhóm quy trình chuẩn

- **Order to Cash (O2C):** báo giá → đơn bán → giao hàng → hóa đơn → thu tiền.
- **Procure to Pay (P2P):** nhu cầu → yêu cầu báo giá → đơn mua → nhận hàng → hóa đơn nhà cung cấp → thanh toán.
- **Plan to Produce:** nhu cầu → lệnh sản xuất → cấp nguyên liệu → sản xuất → nhập thành phẩm.
- **Record to Report:** ghi nhận bút toán → đối soát → báo cáo tài chính.

## 2.2. Nền tảng Odoo 19

### 2.2.1. Giới thiệu

Odoo là bộ ứng dụng doanh nghiệp mã nguồn mở của Bỉ, viết bằng Python, dùng PostgreSQL. Có hai phiên bản: **Community** (miễn phí, LGPL) và **Enterprise** (trả phí, thêm các app như Shop Floor, Quality, Planning, Barcode, Studio, MPS, đối soát ngân hàng). Odoo triển khai được trên Odoo Online (SaaS), Odoo.sh (PaaS) hoặc tự cài (on-premise).

### 2.2.2. Kiến trúc

| Tầng | Thành phần |
|---|---|
| Trình diễn | Web client (framework OWL, JavaScript), website QWeb |
| Ứng dụng | Máy chủ Odoo (Python): ORM, phân quyền, workflow, API (JSON-RPC, XML-RPC, JSON-2 mới ở Odoo 19) |
| Dữ liệu | PostgreSQL; tệp đính kèm trong filestore |

Mỗi tính năng là một **module** (thư mục có `__manifest__.py`, models, views, security, data). Module mới kế thừa module có sẵn bằng `_inherit` (thêm trường, ghi đè hàm) và XPath (sửa giao diện) mà không sửa mã gốc. Đây là cách nhóm viết bh_near_expiry, bh_api và theme.

### 2.2.3. Các phân hệ dùng trong đồ án

| Phân hệ | Khái niệm chính |
|---|---|
| Sales | Báo giá, đơn bán, bảng giá (pricelist), chính sách lập hóa đơn (theo số đặt / số giao), hạn mức nợ |
| Purchase | Yêu cầu báo giá (RFQ), đơn mua (PO), thỏa thuận mua hàng (Blanket Order), duyệt 2 cấp, kiểm soát hóa đơn theo số đã nhận |
| Inventory | Kho, vị trí, lô, hạn dùng, chiến lược xuất (FIFO/FEFO), quy tắc cất hàng, quy tắc tái đặt hàng, gom phiếu (Batch), điều chỉnh tồn |
| Manufacturing | Định mức (BoM), khu vực sản xuất (Work Center), công đoạn, lệnh sản xuất (MO), phụ phẩm, phế phẩm, sản xuất 1/2/3 bước, MTO |
| Invoicing/Accounting | Hóa đơn, giấy báo có, thanh toán, điều khoản thanh toán, nhật ký, hệ thống tài khoản, định giá tồn kho |
| Website | Trang web, eCommerce, cổng khách hàng (portal) |
| Automation Rules | Quy tắc tự động: điều kiện kích hoạt (trigger) + hành động (cập nhật, tạo hoạt động, chạy code, gửi webhook) |

### 2.2.4. Các khái niệm kho – kế toán quan trọng

- **Lô và hạn dùng (product_expiry):** mỗi lô có ngày hết hạn; Odoo tính thêm ngày nên dùng trước, ngày rút khỏi kệ, ngày cảnh báo. Ở Odoo 19, các khoảng thời gian này là **số ngày trước hạn dùng**.
- **FEFO (First Expired, First Out):** lô hết hạn trước được xuất trước; lô đã qua ngày rút khỏi kệ không được giữ cho đơn giao.
- **Tồn dự báo:** tồn thực + hàng sắp nhập – hàng sắp xuất (đã trừ đơn bán đã xác nhận). Màn hình Bổ sung hàng đề xuất sản xuất/mua dựa trên con số này.
- **Giá vốn bình quân gia quyền (AVCO):** giá vốn cập nhật sau mỗi lần nhập.
- **Định giá tồn kho tự động (perpetual):** ở Odoo 19 là "Perpetual (at invoicing)" – bút toán kho ghi khi lập hóa đơn: hóa đơn bán ghi Nợ 632 / Có 155; hóa đơn nhà cung cấp ghi Nợ 152 / Có 331.
- **Tài khoản tiền đang chuyển (outstanding receipts/payments):** khoản thanh toán ghi nhận trước, đối soát với sổ phụ ngân hàng sau (video eLearning Accounting "Payments and outstanding accounts").

## 2.3. Ngôn ngữ mô hình hóa BPMN 2.0

| Ký hiệu | Ý nghĩa | Dùng trong đồ án |
|---|---|---|
| Pool / Lane | Tổ chức / vai trò thực hiện | Mỗi lane là một vai trò ở Chương 1 (kể cả "Hệ thống Odoo") |
| Start / End event | Bắt đầu, kết thúc | Bắt đầu bằng sự kiện thật ("16:00 chốt đơn") |
| Timer start event | Bắt đầu theo thời gian | Kế hoạch hằng ngày, kiểm tra cận hạn 23:00 |
| User task / Service task | Việc người làm / hệ thống làm | Phân biệt rõ việc của người và việc Odoo tự động |
| Send / Receive task | Gửi / chờ nhận thông tin | Gửi đơn mua, chờ nguyên liệu |
| Exclusive gateway | Rẽ nhánh theo điều kiện | Ngoại lệ: nợ quá hạn, QC không đạt, làm thiếu |
| Sequence flow | Thứ tự | |

Các file BPMN được tạo theo chuẩn BPMN 2.0 có phần hiển thị (DI), mở được bằng Camunda Modeler bản desktop.

## 2.4. Chuẩn ngành thực phẩm liên quan đến dữ liệu ERP

- Nghị định 43/2017/NĐ-CP, sửa đổi bởi Nghị định 111/2021/NĐ-CP: nhãn thực phẩm bắt buộc có ngày sản xuất, hạn sử dụng → mỗi lô thành phẩm phải có hạn dùng.
- Nghị định 15/2018/NĐ-CP: tự công bố sản phẩm, điều kiện an toàn thực phẩm.
- HACCP: kiểm soát điểm tới hạn (nhiệt độ nướng, nhiệt độ hàng mát) và lưu hồ sơ → phiếu kiểm tra chất lượng trên Odoo.
- Nghị định 123/2020/NĐ-CP: hóa đơn điện tử → module l10n_vn_edi_viettel.

## 2.5. Phương pháp triển khai ERP

| Phương pháp | Đặc điểm | Phù hợp |
|---|---|---|
| Waterfall | Tuần tự: khảo sát → thiết kế → cấu hình → kiểm thử → go-live | Phạm vi rõ, ít thay đổi |
| Agile/Scrum | Vòng lặp ngắn (sprint), demo thường xuyên | Yêu cầu thay đổi, cần phản hồi người dùng |
| Lai (Hybrid) | Khung giai đoạn của Waterfall, trong giai đoạn cấu hình chạy sprint | Dự án ERP vừa và nhỏ |

Nhóm chọn phương pháp lai (chương 8): mốc go-live cố định, nhưng cấu hình từng phân hệ theo sprint 1 tuần và cho người dùng thử ngay.
