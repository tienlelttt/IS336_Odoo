# Kịch bản quay video thao tác ERP – Nhóm 06

Theo tiêu chí môn học: mỗi bạn tự quay, **có mặt (webcam) và giọng nói**, khớp với thao tác trên màn hình, thể hiện được (1) Odoo do chính mình cài, (2) biết thiết lập và nhập liệu căn bản, (3) làm trọn 1 quy trình. Thêm phần kỹ năng dữ liệu (import, lọc, nhóm, pivot) và API cá nhân.

Tên file nộp: `Thao tác ERP - MSSV - Họ và tên.mp4`, dài 10–12 phút.

| Bạn | Quy trình quay | API cá nhân | Tài khoản dùng trong video |
|---|---|---|---|
| Lê Thị Thanh Tiền – 24521769 | QT1 Bán hàng | REST qua module bh_api | admin, kinhdoanh2, giamdoc, thukho, ketoan |
| Đoàn Thị Thùy Trang – 24521817 | QT2 Mua hàng | XML-RPC | admin, muahang, giamdoc, qc, thukho, ketoan |
| Phạm Tuấn Hải – 24520442 | QT3 Sản xuất | JSON-2 | admin, quandoc, thukho, qc |

Mọi bước trong 3 kịch bản đã được **chạy thử bằng đúng các tài khoản trên** (ngày 19/11, có hoàn tác nên không đổi dữ liệu): đơn bị chặn đúng thông báo, giao thiếu không tạo đơn chờ, hóa đơn theo số giao, QC đạt, nhận thiếu không tạo đơn chờ, quản đốc đặt lệnh từ Bổ sung hàng, làm thiếu đóng lệnh, loại bỏ đúng lô. Số tiền, số lượng ghi trong kịch bản là kết quả lần chạy thử đó.

## Phần A. Chuẩn bị (làm trước khi bấm quay)

1. **Dựng hệ thống trên máy của chính mình** (để video đúng là "Odoo do người quay cài"): làm theo `HUONG_DAN_CAI_DAT.md` mục 1.1–1.4. Dựng lại ngay trước khi quay để dữ liệu sạch: Git Bash tại `odoo_local` → `bash ../scripts/rebuild_all.sh` (khoảng 5 phút).
2. Kiểm tra: mở http://localhost:8069, đăng nhập `admin` / `admin` được.
3. **OBS Studio**: nguồn "Display Capture" (cả màn hình) + "Video Capture Device" (webcam, thu nhỏ góc dưới phải, không che nút Odoo) + micro. Xuất 1920×1080, 30 fps, MP4. Thu thử 10 giây, nghe lại tiếng.
4. Trình duyệt: phóng to 110–125% (Ctrl +) cho chữ dễ đọc; tắt thông báo Windows; đóng tab không liên quan.
5. Mở sẵn: Docker Desktop, Git Bash ở thư mục `DoAn_HoanChinh`, một cửa sổ ẩn danh (Ctrl Shift N) để đăng nhập tài khoản thứ hai mà không phải đăng xuất.
6. Mật khẩu 8 tài khoản nghiệp vụ: `BaoHan#2026` (chỉ dùng cho máy local, xem `data/README.md`).
7. Đọc to kịch bản 1 lần trước khi quay. Quay từng phần, lỗi thì quay lại phần đó rồi ghép.

Lưu ý:
- Số trên màn hình Bổ sung hàng và số chứng từ (S000xx, P000xx, WH/MO/000xx) có thể khác nếu dựng lại vào ngày khác hoặc đã thao tác trước đó. Nói theo số đang hiện trên màn hình.
- Vài màn hình của module OCA còn tiếng Anh (Quality Control, Inspections, nút Confirm). Cứ nói "phiếu kiểm tra chất lượng" và bấm đúng nút tiếng Anh.
- Menu "Tồn kho > Hoạt động > **Tuyển dụng**" thật ra là đợt soạn hàng (bản dịch tiếng Việt của Odoo dịch sai chữ "Jobs"). Khi quay nên nói rõ điều này.
- Ký hiệu trong kịch bản: **Bấm** là thao tác, **Nói** là lời thoại gợi ý (đọc tự nhiên, không cần thuộc từng chữ), **Thấy** là kết quả phải xuất hiện trên màn hình.

## Phần B. Đoạn mở đầu và chứng minh tự cài (chung cho cả 3 bạn, khoảng 1 phút 30)

| Bước | Bấm | Nói | Thấy |
|---|---|---|---|
| B1 | Bật webcam, màn hình là Docker Desktop | "Em là [họ tên], MSSV [MSSV], nhóm 06 môn Hoạch định nguồn lực doanh nghiệp. Đề tài của nhóm là triển khai Odoo 19 cho Công ty TNHH Bánh Bảo Hân, một xưởng sản xuất bánh ở TP Thủ Đức. Trong video này em trình bày quy trình [tên quy trình]." | |
| B2 | Docker Desktop > Containers | "Odoo này em tự cài trên máy em bằng Docker: một container PostgreSQL 16 và một container Odoo 19 Community." | 2 container `odoo_local-db-1`, `odoo_local-odoo-1` đang chạy |
| B3 | Git Bash: `cd odoo_local` rồi `docker compose ps` | "Kiểm tra bằng dòng lệnh, cả hai dịch vụ đều đang chạy, Odoo mở ở cổng 8069." | 2 dòng trạng thái running |
| B4 | Trình duyệt: http://localhost:8069, đăng nhập `admin` / `admin` | "Đăng nhập bằng tài khoản quản trị em tạo khi cài." | Trang chủ Odoo, các ứng dụng |
| B5 | Cài đặt > Người dùng & Công ty > Người dùng | "Đây là danh sách người dùng của hệ thống: tài khoản quản trị và 8 người dùng theo vai trò của xưởng: giám đốc, kinh doanh, mua hàng, quản đốc, QC, thủ kho, kế toán." | 9 người dùng; tài khoản "Quản trị hệ thống" có avatar |

## Phần C. Kịch bản Lê Thị Thanh Tiền – QT1 Bán hàng

### C1. Thiết lập và nhập liệu căn bản (khoảng 2 phút)

| Bước | Bấm | Nói | Thấy |
|---|---|---|---|
| C1.1 | Cài đặt > Người dùng & Công ty > Công ty > Công ty TNHH Bánh Bảo Hân | "Thông tin công ty: tên, mã số thuế 0314345823, địa chỉ TP Thủ Đức, tiền tệ VND." | MST, địa chỉ, VND |
| C1.2 | Cài đặt > Dịch thuật > Ngôn ngữ | "Hệ thống bật hai ngôn ngữ tiếng Việt và tiếng Anh; người dùng tự chọn ngôn ngữ của mình." | Tiếng Việt, English đang dùng |
| C1.3 | Bán hàng > Sản phẩm > Bảng giá | "Bảo Hân bán sỉ cho ba nhóm khách nên có ba bảng giá: giá sỉ quán, giá siêu thị – bếp ăn giảm 5%, giá OEM theo hợp đồng." | 3 bảng giá |
| C1.4 | Bán hàng > Đơn hàng > Khách hàng > Mới. Tên: `Quán cà phê Phố Núi (KH video)`. Tab Bán hàng & Mua hàng: Bảng giá `Giá sỉ quán`. Thẻ: `Tuyến 1`. Lưu | "Em tạo một khách hàng mới. Bảng giá gắn vào khách, nên khi lập đơn giá tự lấy đúng, nhân viên không tự gõ giá. Thẻ Tuyến 1 cho biết khách nằm trên tuyến giao số 1." | Khách mới đã lưu |

### C2. Quy trình QT1 – Nhận đơn, giao hàng, thu tiền (khoảng 5 phút)

Mở hình `bpmn/QT1_ban_hang.png` 15 giây trước khi làm. **Nói:** "Quy trình bán hàng của Bảo Hân: khách đặt bánh cho ngày mai trước 16 giờ, hệ thống chặn đơn nếu khách nợ quá hạn, sáng hôm sau thủ kho soạn hàng theo tuyến, tài xế giao, cuối ngày kế toán lập hóa đơn theo số thực giao và thu tiền."

| Bước | Bấm | Nói | Thấy |
|---|---|---|---|
| C2.1 | Cửa sổ ẩn danh: đăng nhập `kinhdoanh2@baohan.local` | "Em đăng nhập vai trò trưởng nhóm kinh doanh, người nhận đơn qua Zalo, điện thoại." | Menu chỉ có các app được cấp quyền |
| C2.2 | Bán hàng > Đơn hàng > Đơn hàng > Mới. Khách hàng: `Quán cà phê Mộc` | "Quán cà phê Mộc đặt bánh cho sáng mai. Chọn khách là bảng giá sỉ quán tự điền." | Bảng giá: Giá sỉ quán |
| C2.3 | Tab Thông tin khác > Ngày giao hàng: ngày mai 06:00 | "Ngày giao là sáng mai, đơn này sẽ thành nhu cầu cho kế hoạch sản xuất chiều nay." | |
| C2.4 | Tab Chi tiết đơn hàng > Thêm sản phẩm: `Bánh tiệc trà (khay 20 cái)` số lượng 2; `Cookies bơ socola (túi 250g)` số lượng 10 | "Quán lấy 2 khay bánh tiệc trà và 10 túi cookies." | Tổng 682.000 đ |
| C2.5 | Xác nhận | "Khách không có nợ quá hạn nên đơn được xác nhận ngay." | Trạng thái Đơn bán hàng, có nút Giao hàng |
| C2.6 | Mới. Khách: `Siêu thị mini Hiệp Bình`. Sản phẩm `Cookies bơ socola` 30. Xác nhận | "Bây giờ là khách siêu thị mini, khách này đang có hóa đơn quá hạn. Em bấm xác nhận." | Hộp lỗi: "Không thể xác nhận đơn S000xx: khách Siêu thị mini Hiệp Bình (KH mẫu) có 1 hóa đơn quá hạn. Cần giám đốc gắn nhãn 'Đã duyệt công nợ'." |
| C2.7 | Đóng hộp lỗi, kéo xuống khung trao đổi bên phải | "Đây là quy tắc tự động BH2 nhóm em viết: chặn xác nhận đơn khi khách nợ quá hạn hoặc vượt hạn mức, đồng thời giao việc cho giám đốc. Trước đây giám đốc phải nhớ trong đầu khách nào đang nợ." | Hoạt động "Duyệt công nợ: có 1 hóa đơn quá hạn" giao giám đốc |
| C2.8 | Cửa sổ thường: đăng xuất admin, đăng nhập `giamdoc@baohan.local`. Biểu tượng đồng hồ (hoạt động) góc trên > mở việc Duyệt công nợ | "Giám đốc thấy việc cần duyệt. Sau khi gọi khách, giám đốc đồng ý cho giao đơn này." | Mở đúng đơn của siêu thị |
| C2.9 | Trường Thẻ: chọn `Đã duyệt công nợ`. Khung trao đổi: Ghi chú "Khách hẹn trả ngày 25". Lưu. Bấm Xác nhận | "Giám đốc gắn nhãn Đã duyệt công nợ và ghi lý do. Có nhãn thì đơn mới xác nhận được, và lịch sử lưu lại ai duyệt, lý do gì." | Đơn chuyển trạng thái Đơn bán hàng |
| C2.10 | Đăng xuất, đăng nhập `thukho@baohan.local`. Tồn kho > Hoạt động > Lệnh chuyển hàng > Giao hàng. Tìm phiếu của Quán cà phê Mộc, tích chọn | "5 giờ sáng thủ kho soạn hàng. Mỗi tuyến xe có 15 đến 20 điểm giao nên soạn theo tuyến chứ không theo từng đơn." | Phiếu BH/OUT/000xx sẵn sàng |
| C2.11 | Thao tác (bánh răng) > Thêm vào lô > Đợt soạn mới > Xác nhận. Mở Tồn kho > Hoạt động > Tuyển dụng > Lệnh chuyển hàng theo đợt | "Em gom phiếu vào một đợt soạn hàng. Menu này Odoo dịch là Tuyển dụng nhưng thật ra là đợt soạn hàng." | Đợt BATCH/OUT/000xx |
| C2.12 | Mở phiếu giao của Quán cà phê Mộc, dòng Cookies: sửa Số lượng 10 thành 9; mở chi tiết dòng để thấy số lô | "Hệ thống tự giữ lô hết hạn trước theo FEFO. Khách nhận thiếu 1 túi vì túi rách, thủ kho ghi số thực giao là 9." | Lô được chọn sẵn |
| C2.13 | Xác nhận > Không có đơn hàng tách kiện | "Bánh giao thiếu không giao bù, nên em chọn không tạo đơn hàng tách kiện." | Phiếu Hoàn tất |
| C2.14 | Đăng xuất, đăng nhập `ketoan@baohan.local`. Bán hàng > Cần lập hoá đơn > Đơn hàng cần xuất hóa đơn > mở đơn Quán cà phê Mộc > Tạo hoá đơn > Tạo bản nháp | "Cuối ngày kế toán lập hóa đơn cho các đơn đã giao. Chính sách lập hóa đơn là theo số đã giao." | Hóa đơn nháp: Cookies 9, Bánh tiệc trà 2 |
| C2.15 | Xác nhận | "Hóa đơn chỉ tính 9 túi cookies đúng số khách nhận, tổng 632.500 đồng. Khi xác nhận, Odoo ghi nhận doanh thu, công nợ và giá vốn hàng bán." | INV/2026/000xx, 632.500 đ |
| C2.16 | Thanh toán > Sổ nhật ký: Cash > Tạo thanh toán | "Quán nhỏ trả tiền mặt cho tài xế, tài xế nộp lại kế toán, kế toán ghi vào sổ tiền mặt." | Nhãn Đã thanh toán |
| C2.17 | Khung trao đổi của hóa đơn hoặc nút Bút toán | "Khách trả sau thì tiền chuyển khoản được webhook ngân hàng tự ghi nhận, phần đó thuộc quy trình công nợ của bạn Trang." | |

### C3. Kỹ năng dữ liệu (khoảng 1 phút 30)

| Bước | Bấm | Nói | Thấy |
|---|---|---|---|
| C3.1 | Bán hàng > Đơn hàng > Khách hàng > biểu tượng bánh răng > Nhập bản ghi > Tải tệp `data/khach_hang.csv` > Kiểm thử | "Nhóm chuẩn bị file CSV có sẵn tên trường của Odoo để nhập danh sách khách khi go-live. Kiểm thử báo hợp lệ. Em không bấm Nhập vì dữ liệu đã có, nhập nữa sẽ trùng." | Thông báo hợp lệ |
| C3.2 | Đơn hàng: chọn vài đơn > Thao tác > Xuất | "Xuất ngược ra Excel cũng chọn trường như vậy." | Hộp chọn trường xuất |
| C3.3 | Ô tìm kiếm: Bộ lọc `Đơn bán hàng`, Nhóm theo `Khách hàng`; Yêu thích > Lưu bộ lọc hiện tại, tên "Đơn bán theo khách" | "Lọc đơn đã xác nhận, nhóm theo khách và lưu lại để mở nhanh mỗi ngày." | Bộ lọc nằm trong Yêu thích |
| C3.4 | Bán hàng > Báo cáo > Bán hàng > chế độ Pivot: hàng Khách hàng, cột Ngày đặt hàng theo ngày; chuyển Đồ thị | "Báo cáo doanh thu theo khách theo ngày cho giám đốc." | Bảng pivot, đồ thị |

### C4. API cá nhân: REST qua module bh_api (khoảng 1 phút 30)

| Bước | Bấm | Nói | Thấy |
|---|---|---|---|
| C4.1 | Đăng nhập admin. Cài đặt > API & Tích hợp > API đối tác > `App đặt hàng - Chuỗi trà sữa Lá Xanh` | "Module bh_api nhóm em viết cho app đặt hàng của khách sỉ. Mỗi đối tác có phạm vi quyền riêng: xem tồn, đặt đơn, xem công nợ; có hạn token và giới hạn số lần gọi." | Phạm vi quyền, hạn, giới hạn |
| C4.2 | Sinh token mới > sao chép > Đã sao chép | "Token chỉ hiện một lần, Odoo chỉ lưu bản băm nên lộ cơ sở dữ liệu cũng không lộ token." | Token dạng chuỗi dài |
| C4.3 | Git Bash ở `DoAn_HoanChinh`: `BH_API_TOKEN=<dán token> python scripts/api_demo_calls.py` | "Script đóng vai app của khách: gọi không có token bị từ chối 401, có token thì xem được sản phẩm theo bảng giá của khách, rồi tạo đơn bằng POST /orders." | HTTP 401, 200, 201 kèm số đơn S000xx |
| C4.4 | Odoo: Bán hàng > Đơn hàng > Báo giá > mở đơn vừa tạo; quay lại API đối tác > tab nhật ký | "Đơn từ app vào thẳng Odoo, kinh doanh chỉ kiểm rồi xác nhận. Mỗi lần gọi đều ghi nhật ký." | Đơn nháp của Chuỗi trà sữa Lá Xanh; nhật ký 401/200/201 |

### C5. Kết (15 giây)

**Nói:** "Như vậy em đã trình bày quy trình bán hàng từ lúc khách đặt đến lúc thu tiền, cùng kiểm soát công nợ và API cho app đặt hàng. Cảm ơn thầy đã xem."

## Phần D. Kịch bản Đoàn Thị Thùy Trang – QT2 Mua hàng

### D1. Thiết lập và nhập liệu căn bản (khoảng 2 phút)

| Bước | Bấm | Nói | Thấy |
|---|---|---|---|
| D1.1 | Cài đặt > Kỹ thuật > Email > Máy chủ thư đi > `Gmail SMTP - Bảo Hân` | "Cấu hình gửi mail qua Gmail: smtp.gmail.com, cổng 587, STARTTLS. Mật khẩu là mật khẩu ứng dụng của Gmail; em không nhập trên video." | Thông số máy chủ |
| D1.2 | Cài đặt > Thiết lập chung > Công ty > Cấu hình bố cục chứng từ | "Mẫu chứng từ dùng khung Boxed màu nâu caramel theo nhận diện Bảo Hân, chân trang có MST và số điện thoại." | Xem trước mẫu |
| D1.3 | Mua hàng > Cấu hình > Cài đặt > Duyệt đơn hàng | "Đơn mua từ 20 triệu phải giám đốc duyệt." | Duyệt 2 cấp, 20.000.000 |
| D1.4 | Mua hàng > Sản phẩm > Sản phẩm > Mới: `Bột cacao (NVL video)`, Theo dõi tồn kho. Tab Mua hàng > Thêm dòng: nhà cung cấp `NCC mẫu 02 - Men, phụ gia, socola`, giá 150.000, thời gian giao 3 ngày. Lưu | "Tạo một nguyên liệu mới, gắn nhà cung cấp và giá mua, để khi thiếu hệ thống đề xuất mua đúng chỗ." | Sản phẩm đã lưu |
| D1.5 | Mua hàng > Đơn hàng > Hợp đồng mua hàng > `BO00003` | "Bảo Hân chốt giá theo quý với nhà cung cấp chính. Ví dụ hợp đồng trứng gà với NCC04." | Hợp đồng đã xác nhận |

### D2. Quy trình QT2 – Đặt nguyên liệu, kiểm tại cửa, nhận hàng, trả tiền (khoảng 5 phút)

Mở `bpmn/QT2_mua_hang.png` 15 giây. **Nói:** "Sau khi quản đốc lập kế hoạch lúc 16 giờ 30, nhân viên mua hàng đặt nguyên liệu theo giá hợp đồng. Khi xe nhà cung cấp đến, QC kiểm tại cửa, chỉ nhận phần đạt, kế toán chỉ trả tiền cho số đã nhận."

| Bước | Bấm | Nói | Thấy |
|---|---|---|---|
| D2.1 | Cửa sổ ẩn danh: đăng nhập `muahang@baohan.local`. Mua hàng > Đơn hàng > Yêu cầu báo giá > Mới. Nhà cung cấp: `NCC mẫu 04 - Trứng gà`. Sản phẩm `Trứng gà` 3.000 | "Đặt 3.000 quả trứng. Đơn giá 3.100 đồng tự lấy từ hợp đồng giá quý, nhân viên không tự sửa giá." | Đơn giá 3.100, tổng 10.230.000 đ |
| D2.2 | Xác nhận đơn hàng | "Đơn dưới 20 triệu nên xác nhận được ngay, sau đó gửi PDF cho nhà cung cấp qua email hoặc Zalo." | Trạng thái Đơn mua hàng, nút Nhận |
| D2.3 | Mua hàng > Đơn hàng > Đơn mua hàng > mở `P00004` (NCC01 bột mì, 24.612.500 đ) | "Đơn bột tuần này 24,6 triệu, vượt ngưỡng nên đang chờ duyệt; nhân viên mua hàng không tự duyệt được." | Trạng thái Chờ phê duyệt |
| D2.4 | Cửa sổ thường: đăng nhập `giamdoc@baohan.local`, mở P00004 > Phê duyệt đơn hàng | "Giám đốc duyệt, đơn chuyển thành đơn mua và sinh phiếu nhập." | Trạng thái Đơn mua hàng |
| D2.5 | Đăng xuất, đăng nhập `qc@baohan.local`. Quality Control > Inspections > Inspections > mở phiếu mới nhất (trạng thái Ready) của trứng gà | "Khi đơn mua xác nhận, quy tắc tự động BH1 tạo sẵn phiếu kiểm tra. Xe đến là QC kiểm ngay tại cửa, trước khi nhận." | Phiếu QC-000xx, 3 câu kiểm |
| D2.6 | Nhập: Nhiệt độ hàng khi nhận `4` (chuẩn 0–5 °C); Bao bì nguyên vẹn `Đạt`; Hạn dùng còn ít nhất 2/3 `Đạt`. Bấm Confirm | "Trứng là hàng mát, nhiệt độ phải từ 0 đến 5 độ. Nếu nhập 7 độ thì phiếu không đạt và không nhận hàng." | Trạng thái Success |
| D2.7 | Đăng xuất, đăng nhập `thukho@baohan.local`. Tồn kho > Hoạt động > Lệnh chuyển hàng > Phiếu nhập kho > mở phiếu trứng của NCC04 | "Thủ kho nhận số đạt." | Phiếu BH/IN/000xx |
| D2.8 | Dòng Trứng gà > biểu tượng chi tiết: Tên số lô/sê-ri `NCC04-261120`, Ngày hết hạn: 21 ngày sau, Số lượng `2940`. Lưu | "Ghi số lô và hạn dùng in trên khay. 60 quả bị vỡ trả lại tài xế, chỉ nhận 2.940 quả." | |
| D2.9 | Xác nhận > Không có đơn hàng tách kiện. Khung trao đổi: ghi chú "60 quả vỡ, trả lại xe" | "Nhà cung cấp trứng không giao bù trong ngày nên không tạo đơn chờ. Hàng tự vào kho mát theo quy tắc cất hàng." | Phiếu Hoàn tất; đơn mua đã nhận 2.940 |
| D2.10 | Đăng xuất, đăng nhập `ketoan@baohan.local`. Mở đơn mua trứng > Tạo hóa đơn | "Hóa đơn nhà cung cấp chỉ lấy số đã nhận: 2.940 quả, đây là đối chiếu ba bên đơn mua, phiếu nhập, hóa đơn." | Hóa đơn nháp số lượng 2.940 |
| D2.11 | Điền Ngày hóa đơn > Xác nhận > Thanh toán > Sổ nhật ký Cash > Tạo thanh toán | "Nhà cung cấp trứng nhận tiền mặt khi giao. Tổng 10.025.400 đồng." | Hóa đơn đã thanh toán |

### D3. Kỹ năng dữ liệu (khoảng 1 phút 30)

| Bước | Bấm | Nói | Thấy |
|---|---|---|---|
| D3.1 | Mua hàng > Đơn hàng > Nhà cung cấp > bánh răng > Nhập bản ghi > `data/nha_cung_cap.csv` > Kiểm thử | "File nhà cung cấp chuẩn bị sẵn để import khi go-live; kiểm thử hợp lệ, không bấm Nhập để tránh trùng." | Hợp lệ |
| D3.2 | Mua hàng > Đơn hàng > Đơn mua hàng: Nhóm theo Nhà cung cấp; Yêu thích > Lưu bộ lọc hiện tại "Đơn mua theo NCC" | "Nhóm đơn theo nhà cung cấp và lưu lại." | Bộ lọc trong Yêu thích |
| D3.3 | Mua hàng > Báo cáo > Mua hàng > Pivot: hàng Nhà cung cấp, cột Ngày đặt hàng theo tháng; Đồ thị | "Giá trị mua theo nhà cung cấp để giám đốc xem khi đàm phán hợp đồng quý sau." | Pivot, đồ thị |

### D4. API cá nhân: XML-RPC (khoảng 1 phút 30)

| Bước | Bấm | Nói | Thấy |
|---|---|---|---|
| D4.1 | Đăng nhập admin > avatar góc phải > Tùy chọn của tôi > tab Bảo mật tài khoản > Khóa API mới > nhập mật khẩu admin > đặt tên "XML-RPC video", chọn thời hạn > Tạo khóa > sao chép | "XML-RPC là API lâu đời của Odoo: gọi /xmlrpc/2/common để đăng nhập lấy uid, rồi /xmlrpc/2/object với execute_kw để đọc, tạo, sửa bất kỳ model nào theo quyền của người dùng. Em dùng khóa API thay cho mật khẩu." | Khóa hiện một lần |
| D4.2 | Git Bash ở `DoAn_HoanChinh`: `ODOO_USER=admin ODOO_API_KEY=<dán khóa> python scripts/api_ca_nhan/xmlrpc_tao_don_mua.py` | "Script đóng vai hệ thống bên ngoài, tạo yêu cầu báo giá xúc xích và sốt gửi NCC05." | "Phiên bản: 19.0", "Đã tạo P000xx trạng thái draft tổng ..." |
| D4.3 | Mua hàng > Đơn hàng > Yêu cầu báo giá > mở P000xx | "Yêu cầu báo giá đã nằm trong Odoo, nguồn ghi Tạo qua XML-RPC." | Nguồn: Tạo qua XML-RPC |

### D5. Kết

**Nói:** "Em đã trình bày quy trình mua nguyên liệu từ đề xuất đến trả tiền, có duyệt đơn lớn, kiểm tra chất lượng tại cửa và đối chiếu ba bên. Phần công nợ phải thu và phải trả em trình bày trong báo cáo mục 5.5. Cảm ơn thầy."

## Phần E. Kịch bản Phạm Tuấn Hải – QT3 Sản xuất

### E1. Thiết lập và nhập liệu căn bản (khoảng 2 phút)

| Bước | Bấm | Nói | Thấy |
|---|---|---|---|
| E1.1 | Cài đặt > Người dùng & Công ty > Người dùng > `Quản đốc` (quandoc) > tab Quyền truy cập | "Phân quyền theo vai trò: quản đốc có quyền quản lý sản xuất và người dùng kho, không có quyền kế toán." | Sản xuất: Quản trị viên; Tồn kho: Người dùng |
| E1.2 | Người dùng > Mới: tên `Tổ trưởng ca đêm (video)`, đăng nhập `totruong@baohan.local`; quyền Sản xuất: Người dùng, Tồn kho: Người dùng. Lưu | "Tạo người dùng cho tổ trưởng ca đêm, người ghi sản lượng cuối ca." | Người dùng mới |
| E1.3 | Tồn kho > Cấu hình > Cài đặt: Vị trí lưu trữ, Số lô & sê-ri, Ngày hết hạn, Tuyến nhiều bước | "Bật quản lý lô, hạn dùng và nhiều vị trí vì bánh có hạn ngắn." | Các ô đã bật |
| E1.4 | Sản xuất > Sản phẩm > Sản phẩm > Mới: `Bánh mì bơ tỏi (TP video)`, Theo dõi tồn kho theo lô; tab có Ngày hết hạn: thời gian sử dụng 5 ngày. Lưu | "Tạo một thành phẩm theo lô, hạn dùng 5 ngày, để khi sản xuất xong lô nào hệ thống tự tính hạn." | Sản phẩm đã lưu |
| E1.5 | Sản xuất > Sản phẩm > Danh mục vật tư > `[FG02] Bánh mì sandwich trắng 400g` | "Định mức theo mẻ 100 ổ: khoảng 23 kg bột, đường, muối, men, bơ, túi, thùng. Tab Công đoạn để tính tải lò và chi phí theo thời gian định mức; tab Phụ phẩm là vụn bánh; tiêu hao cho phép kèm cảnh báo." | Các tab Thành phần, Công đoạn, Phụ phẩm |

### E2. Quy trình QT3 – Sản xuất theo mẻ cho quản đốc (khoảng 5 phút)

Mở `bpmn/QT3_san_xuat.png` 15 giây. **Nói:** "Ở Bảo Hân, thợ làm bánh không dùng Odoo. Người dùng Odoo trên sàn sản xuất là quản đốc: 16 giờ lập kế hoạch mẻ cho ngày mai, thủ kho cấp nguyên liệu cho cả ca, 5 giờ sáng ghi sản lượng thực tế."

| Bước | Bấm | Nói | Thấy |
|---|---|---|---|
| E2.1 | Cửa sổ ẩn danh: đăng nhập `quandoc@baohan.local`. Tồn kho > Hoạt động > Mua sắm > Bổ sung hàng (phải mở bằng menu) | "16 giờ chốt đơn. Màn hình Bổ sung hàng cho thấy tồn dự báo đã trừ các đơn bán đã xác nhận cho ngày mai." | Đề xuất: Hoppi 147, sandwich trắng 75, nguyên cám 4, mousse 2 (số theo ngày dựng) |
| E2.2 | Tích dòng `[FG02] Bánh mì sandwich trắng 400g` > bấm Đơn hàng | "Quản đốc chốt số lượng rồi đặt. Odoo gom nhu cầu của nhiều quán thành một lệnh cho mỗi sản phẩm mỗi ca, không phải mỗi đơn một lệnh." | Thông báo đã tạo WH/MO/000xx |
| E2.3 | Bấm số lệnh trong thông báo (hoặc Sản xuất > Hoạt động > Lệnh sản xuất) | "Lệnh 75 ổ đã xác nhận; cột thành phần báo có đủ nguyên liệu. Nếu thiếu, quản đốc báo mua hoặc dời mẻ." | Trạng thái Đã xác nhận; Thành phần: Có hàng |
| E2.4 | In > Lệnh sản xuất | "In phiếu sản xuất có công thức và số lượng cho thợ làm theo." | Phiếu PDF |
| E2.5 | Nút phiếu chuyển `Lấy thành phần` WH/PC/000xx. Cửa sổ thường: đăng nhập `thukho@baohan.local`, mở phiếu này > Xác nhận | "Sản xuất 2 bước: 16 giờ 30 thủ kho cấp nguyên liệu cho cả ca ra khu sản xuất, lô giữ theo FEFO, vì ban đêm kho không có người." | Phiếu Hoàn tất |
| E2.6 | Đăng xuất, đăng nhập `qc@baohan.local`. Quality Control > Inspections > Inspections > phiếu mới nhất của sandwich trắng | "Khi lệnh sản xuất xác nhận, quy tắc tự động BH5 tạo phiếu kiểm mẫu. 5 giờ sáng QC lấy mẫu." | Phiếu 4 câu kiểm |
| E2.7 | Nhập: Nhiệt độ lõi `95` (chuẩn 92–99 °C); Cảm quan `Đạt`; Khối lượng `Đạt`; Nhãn `Đạt`. Confirm | "Nhiệt độ lõi đo bằng que đo, phải từ 92 đến 99 độ thì bánh chín." | Success |
| E2.8 | Đăng xuất, đăng nhập `quandoc@baohan.local`, mở lệnh FG02. Số lượng sản xuất: sửa `75` thành `70`. Số lô: gõ `FG02-261120` > tạo mới | "Theo sổ ca, ca đêm làm được 70 ổ. Lô đặt theo mã sản phẩm và ngày để truy xuất." | |
| E2.9 | Sản xuất > hộp cảnh báo tiêu hao: Xác nhận > hộp làm thiếu: Không có đơn hàng tách kiện | "Odoo cảnh báo tiêu hao lệch so với định mức vì nguyên liệu đã cấp cho 75 ổ, em xác nhận. Làm thiếu 5 ổ: bánh tươi không làm bù hôm sau nên em đóng lệnh, không tạo lệnh bổ sung." | Trạng thái Hoàn tất, 70 ổ |
| E2.10 | Tồn kho > Sản phẩm > Số lô/sê-ri > `FG02-261120` | "Hạn dùng tự tính 5 ngày, thành phẩm tự vào kho thành phẩm nhiệt độ thường." | Hạn dùng +5 ngày; vị trí BH/Tồn kho/TP nhiệt độ thường |
| E2.11 | Sản xuất > Hoạt động > Loại bỏ > Mới: sản phẩm FG02, Lô `FG02-261120`, Số lượng 2, Vị trí nguồn `BH/Tồn kho/TP nhiệt độ thường`, lệnh sản xuất vừa làm. Xác nhận | "2 ổ bị méo khi kiểm, ghi phiếu loại bỏ gắn với lệnh để đo tỷ lệ hư hỏng." | Phiếu SP/000xx hoàn tất |
| E2.12 | Mở lại lệnh sản xuất > Truy xuất nguồn gốc | "Lô thành phẩm truy ngược được lô bột, lô bơ đã dùng; khi khách khiếu nại chỉ mất vài phút thay vì 1–2 ngày." | Báo cáo truy xuất nguồn gốc |
| E2.13 | Tồn kho > Cận hạn > Việc cần xử lý | "Lô thành phẩm sau đó được module cận hạn nhóm viết theo dõi mỗi đêm: bánh mì còn dưới 40% hạn thì thu hồi ở chuyến giao sau. Phần kho em trình bày trong báo cáo mục 5.4." | Danh sách việc cận hạn |

### E3. Kỹ năng dữ liệu (khoảng 1 phút 30)

| Bước | Bấm | Nói | Thấy |
|---|---|---|---|
| E3.1 | Sản xuất > Sản phẩm > Sản phẩm > bánh răng > Nhập bản ghi > `data/san_pham_thanh_pham.csv` > Kiểm thử | "File 12 thành phẩm chuẩn bị sẵn để import; kiểm thử hợp lệ, không bấm Nhập để tránh trùng." | Hợp lệ |
| E3.2 | Sản xuất > Hoạt động > Lệnh sản xuất: Bộ lọc Hoàn tất, Nhóm theo Sản phẩm; Yêu thích > Lưu bộ lọc hiện tại "Lệnh đã xong theo sản phẩm" | "Quản đốc xem lại sản lượng tuần mỗi thứ Hai." | Bộ lọc trong Yêu thích |
| E3.3 | Chế độ Pivot: hàng Sản phẩm, cột Ngày; đo Số lượng đã sản xuất. Sản xuất > Báo cáo > Công đoạn | "Sản lượng theo sản phẩm theo ngày và tải các khu vực sản xuất, lò nướng là nút thắt." | Pivot, biểu đồ tải |

### E4. API cá nhân: JSON-2 (khoảng 1 phút 30)

| Bước | Bấm | Nói | Thấy |
|---|---|---|---|
| E4.1 | Đăng nhập admin > avatar > Tùy chọn của tôi > tab Bảo mật tài khoản > Khóa API mới > tên "JSON-2 video" > Tạo khóa > sao chép | "JSON-2 là API mới của Odoo 19: gọi POST /json/2/tên-model/tên-hàm, xác thực bằng khóa API trong header Authorization." | Khóa hiện một lần |
| E4.2 | Git Bash ở `DoAn_HoanChinh`: `ODOO_API_KEY=<dán khóa> python scripts/api_ca_nhan/json2_doc_lenh_san_xuat.py` | "Script đọc các lệnh sản xuất đã xong và lô thành phẩm đang cận hạn, ví dụ để đưa lên bảng báo cáo ở xưởng." | Danh sách lệnh, có lệnh vừa làm 75 → 70 ghi "(làm thiếu)"; danh sách lô cận hạn |

### E5. Kết

**Nói:** "Em đã trình bày quy trình sản xuất theo mẻ: quản đốc lập kế hoạch từ đơn đã chốt, cấp nguyên liệu 2 bước, kiểm mẫu, ghi sản lượng thực tế, đóng lệnh khi làm thiếu và truy xuất lô. Cảm ơn thầy."

## Phần F. Kiểm tra trước khi nộp

- Video có mặt, có tiếng, không bị webcam che nút bấm.
- Có cảnh Docker Desktop và trang Người dùng của admin trên máy của chính mình.
- Có ít nhất một thao tác thiết lập và một lần tạo dữ liệu.
- Quy trình chạy trọn từ đầu đến cuối, nói rõ mỗi bước thay giấy tờ nào và kiểm soát gì.
- Có import (kiểm thử), lọc, nhóm, lưu bộ lọc, pivot.
- Có gọi API cá nhân và thấy kết quả trong Odoo.
- Đặt tên đúng: `Thao tác ERP - MSSV - Họ và tên.mp4`.
