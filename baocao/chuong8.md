# CHƯƠNG 8. PHƯƠNG ÁN TRIỂN KHAI, HẠ TẦNG VÀ AN NINH THÔNG TIN

## 8.1. Mô hình triển khai

Bảng: So sánh các mô hình triển khai

| Tiêu chí | Odoo Online (SaaS) | Odoo.sh (PaaS) | Tự cài – on-premise / VPS | Hybrid |
|---|---|---|---|---|
| Chi phí ban đầu | Thấp | Trung bình | Thấp (Community) đến trung bình | Trung bình |
| Module Python tự viết | Không | Có | Có | Có (phần tự cài) |
| Bản Enterprise | Có | Có | Cần mua | Có |
| Vận hành, sao lưu | Odoo lo | Odoo lo | Doanh nghiệp tự lo | Chia đôi |
| Phụ thuộc Internet | Hoàn toàn | Hoàn toàn | Không (nếu đặt tại xưởng) | Một phần |
| Một cơ sở dữ liệu chung | Có | Có | Có | Không (hai hệ thống) |

**Lựa chọn của nhóm:** Odoo 19 Community tự cài bằng Docker, một hệ thống duy nhất. Lý do: đồ án cần module Python tự viết chạy chung dữ liệu với phân hệ chuẩn; Odoo Online không cho; Hybrid (Online + tự cài) tách thành hai cơ sở dữ liệu, mất tính tích hợp. Đánh đổi: không có app Enterprise (Shop Floor, Quality, Planning, Barcode, Studio, đối soát ngân hàng) → bù bằng module OCA và thiết kế quy trình cho quản đốc.

**Khuyến nghị khi triển khai thật cho Bảo Hân:** chạy cùng bộ Docker trên một VPS tại Việt Nam (2 vCPU, 4 GB RAM, 80 GB SSD), có tên miền và HTTPS; hoặc Odoo.sh nếu muốn dùng Enterprise và không có người quản trị máy chủ.

## 8.2. Tư vấn hạ tầng

Bảng: Đề xuất hạ tầng

| Hạng mục | Đề xuất | Lý do |
|---|---|---|
| Máy chủ | VPS 2 vCPU, 4 GB RAM, 80 GB SSD, Ubuntu + Docker | Đủ cho 10–20 người dùng đồng thời |
| Mạng | Cáp quang xưởng + 4G dự phòng | Ca đêm và sáng sớm vẫn cần mở phiếu |
| Thiết bị | 1 máy tính văn phòng kinh doanh/kế toán; 1 máy tính bảng ở kho và khu nhận hàng; máy in phiếu giao, máy in nhãn lô | Thủ kho thao tác tại chỗ |
| Sao lưu | Hằng ngày ra lưu trữ ngoài máy chủ | Mục 8.5 |
| Tên miền | baohan… + chứng chỉ HTTPS | Website, cổng khách hàng, API |

## 8.3. Lộ trình và phương pháp triển khai

Phương pháp lai: khung giai đoạn kiểu Waterfall với mốc go-live cố định; trong giai đoạn cấu hình chạy sprint 1 tuần, cuối sprint cho người dùng thật thử.

Bảng: Lộ trình triển khai theo tuần

| Tuần | Giai đoạn | Việc | Đầu ra |
|---|---|---|---|
| 1 | Khảo sát | Phỏng vấn (mục 1.6, mẫu biên bản ở Phụ lục B), thu chứng từ mẫu, quan sát một ngày vận hành | Hiện trạng, yêu cầu |
| 2 | Thiết kế | Quy trình TO-BE, BPMN, ma trận quyền, dữ liệu nền | Bản thiết kế được duyệt |
| 3 | Sprint 1 | Cài đặt, cấu hình chung, dữ liệu nền, Bán hàng | Demo QT1 |
| 4 | Sprint 2 | Mua hàng, Kho, Chất lượng | Demo QT2, QT4 |
| 5 | Sprint 3 | Sản xuất, Kế toán, Automation | Demo QT3, QT5 |
| 6 | Sprint 4 | Module cận hạn, API, website, tích hợp | Demo đầy đủ |
| 7 | Kiểm thử, đào tạo | Chạy thử song song sổ cũ 1 tuần; đào tạo theo vai trò | Biên bản nghiệm thu |
| 8 | Go-live | Thứ Bảy: kiểm kê chốt tồn, chuyển công nợ; thứ Hai: vận hành thật; hỗ trợ tại chỗ 2 tuần | Hệ thống chạy |

Chuyển đổi dữ liệu (đã mô phỏng trong DB): tồn kho đầu kỳ theo lô bằng điều chỉnh tồn; công nợ phải thu, phải trả bằng hóa đơn "Số dư đầu kỳ" đối ứng TK 4211; dữ liệu nền bằng file import.

Quản lý thay đổi: đào tạo theo đúng việc từng người (quản đốc chỉ học 4 màn hình); in sẵn hướng dẫn một trang dán tại kho; giai đoạn đầu giữ song song sổ tay một tuần; giám đốc dùng báo cáo Odoo trong họp giao ban để người dùng thấy giá trị.

## 8.4. An ninh thông tin

### 8.4.1. Phân quyền

Ma trận ở mục 3.4, hiện thực bằng nhóm quyền của Odoo. Thêm quy tắc bản ghi có sẵn: nhân viên kinh doanh 1 chỉ thấy đơn của mình. API chạy dưới quyền người dùng gắn với token nên không vượt quyền.

### 8.4.2. Mật khẩu và đăng nhập

Bảng: Chính sách mật khẩu và đăng nhập

| Biện pháp | Cấu hình |
|---|---|
| Độ dài tối thiểu | Thiết lập > Quyền > Độ dài mật khẩu tối thiểu: 10 ký tự |
| Mật khẩu mạnh | Quy định nội bộ: chữ hoa, chữ thường, số, ký tự đặc biệt; đổi 90 ngày |
| Xác thực 2 bước | Bật cho giám đốc, kế toán, quản trị (có sẵn trong Odoo) |
| Tài khoản admin | Đổi mật khẩu mặc định ngay khi cài; không dùng chung |
| API key | Có hạn dùng, thu hồi khi nghỉ việc |

### 8.4.3. Vết kiểm toán (audit trail)

Theo dõi thay đổi (chatter tracking) trên chứng từ: ai đổi trạng thái, giá, số lượng, lúc nào; trạng thái việc cận hạn, cách xử lý, tổn thất có tracking; nhật ký gọi API (bh.api.log); giao dịch ngân hàng (bh.bank.txn). Hóa đơn đã xác nhận không sửa trực tiếp mà phải lập giấy báo có. Bản Enterprise có thêm "Audit Trail" kế toán; bản Community dùng tracking và khóa sổ kỳ (ngày khóa kế toán).

### 8.4.4. Sao lưu và dự phòng

Bảng: Sao lưu và dự phòng

| Biện pháp | Cách làm |
|---|---|
| Sao lưu CSDL | `docker compose exec -T db pg_dump -U odoo -Fc baohan > backup_YYYYMMDD.dump` chạy hằng ngày bằng lịch (cron / Task Scheduler) |
| Sao lưu tệp | Nén volume `odoo-data` (ảnh, tệp đính kèm) |
| Quy tắc 3-2-1 | 3 bản, 2 loại lưu trữ, 1 bản ngoài xưởng (Google Drive / ổ ngoài) |
| Thử khôi phục | Mỗi tháng khôi phục vào DB thử (`pg_restore`) |
| Mục tiêu | Mất dữ liệu tối đa 1 ngày (RPO), khôi phục trong 4 giờ (RTO) |
| Dự phòng vận hành | Mẫu phiếu giao, phiếu nhập giấy để dùng tạm khi mất mạng; nhập bù khi có mạng |

Nhóm đã sao lưu thật DB bản 1 bằng pg_dump trước khi dựng lại và dựng lại toàn bộ hệ thống bằng một lệnh (`scripts/rebuild_all.sh`).
