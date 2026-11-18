# Kiến thức ôn vấn đáp – Đồ án ERP Bảo Hân

Cách dùng: đọc câu hỏi, tự trả lời thành tiếng, rồi so với đáp án. Đáp án ngắn để nói trong 30–60 giây; chi tiết nằm ở chương báo cáo ghi trong ngoặc. Mọi con số trong đây khớp với dữ liệu trong hệ thống.

## 1. Câu hỏi về đề tài và lựa chọn

**1.1. Vì sao chọn Bảo Hân, không chọn Masan hay đại lý tạp hóa?**
Môn yêu cầu doanh nghiệp sản xuất. Masan quá lớn (nhiều công ty con, ngành hàng) để làm trọn trên Odoo. Đại lý tạp hóa chỉ mua bán, không sản xuất nên không có MRP, BoM, kiểm soát chất lượng trong sản xuất. Bảo Hân là xưởng thật (MST 0314345823), nhỏ (xưởng 500 m²), tự sản xuất, bán sỉ B2B, sản phẩm hạn dùng ngắn – đủ 5 phân hệ và có bài toán riêng để làm module.

**1.2. Thông tin doanh nghiệp lấy từ đâu? Có phỏng vấn không?**
Thông tin công khai (Yellow Pages, Trang Vàng): MST, địa chỉ xưởng và trụ sở, diện tích, công suất 10.000 sản phẩm/ngày, danh mục sản phẩm, khách tiêu biểu. Số liệu nội bộ là giả định, ghi rõ trong báo cáo. Nhóm có bộ 32 câu hỏi phỏng vấn (Phụ lục B) để thay giả định bằng số liệu thật. Không bịa biên bản phỏng vấn.

**1.3. Vì sao chọn 5 phân hệ này? Sao không có Nhân sự?**
Bán hàng (80% doanh thu, dòng tiền), Mua hàng (nguyên liệu tươi), Sản xuất (lõi), Kho (hạn dùng, lô), Kế toán (công nợ, giá vốn). Nhân sự không phải nỗi đau chính của case và 3 người không đủ sức làm sâu thêm phân hệ; ghi ở hạn chế.

**1.4. Vì sao dùng Odoo Community tự cài, không dùng Odoo Online bản edu?**
Odoo Online không cài được module Python tự viết. Đồ án cần module cận hạn và module API chạy chung một cơ sở dữ liệu với Bán, Mua, Kho. Đánh đổi: không có app Enterprise (Shop Floor, Planning, Barcode, Studio) → bù bằng OCA và thiết kế quy trình cho quản đốc.

**1.5. Vì sao dữ liệu chỉ có một tuần?**
Nhóm mô phỏng đúng cách dự án ERP bắt đầu: tuần go-live – thứ Bảy chuyển số dư đầu kỳ, thứ Hai đến thứ Tư vận hành. Thêm nữa, Odoo kiểm ngày rút khỏi kệ của lô theo giờ thật, nên không giả lập lùi nhiều tuần với bánh hạn 3–5 ngày được.

## 2. Kiến thức ERP chung

**2.1. ERP là gì? Khác Excel thế nào?**
Hệ thống tích hợp các nghiệp vụ trên một cơ sở dữ liệu chung; một nghiệp vụ tự cập nhật các bộ phận liên quan. Excel rời rạc, nhập lại nhiều lần, không kiểm soát chéo, không truy xuất.

**2.2. O2C, P2P là gì?**
O2C: báo giá → đơn bán → giao → hóa đơn → thu tiền (QT1, QT5). P2P: nhu cầu → RFQ → đơn mua → nhận hàng → hóa đơn NCC → trả tiền (QT2).

**2.3. Master data và transaction data khác nhau?**
Master là dữ liệu ít đổi, dùng lại nhiều lần (sản phẩm, khách, NCC, BoM, bảng giá). Transaction là dữ liệu phát sinh theo nghiệp vụ (đơn bán, phiếu kho, lệnh sản xuất, hóa đơn). Master sai thì mọi transaction sai (ví dụ định mức sai → giá thành sai).

**2.4. Yếu tố thành công / thất bại của dự án ERP?**
Thiết kế theo cách doanh nghiệp làm việc; dữ liệu sạch; người dùng tham gia sớm; lãnh đạo dùng hệ thống; phạm vi vừa sức; quản lý thay đổi. Thất bại thường do áp quy trình "đẹp" mà không ai làm, dữ liệu bẩn, đào tạo thiếu.

**2.5. Waterfall hay Agile cho dự án này?**
Lai: khung giai đoạn và mốc go-live cố định (Waterfall), trong giai đoạn cấu hình chạy sprint 1 tuần để người dùng thử sớm (Scrum). Lộ trình 8 tuần ở chương 8.

## 3. Kiến thức Odoo

**3.1. Kiến trúc Odoo?**
3 tầng: web client (OWL/JS), máy chủ Python (ORM, phân quyền, API), PostgreSQL. Mỗi tính năng là một module; module mới kế thừa module cũ bằng `_inherit` và XPath, không sửa mã gốc.

**3.2. Community khác Enterprise?**
Enterprise thêm Shop Floor, Quality, Planning, Barcode, Studio, MPS, đối soát ngân hàng, Production Analysis. Nhóm đã kiểm trong Odoo 19 Community: không có module mrp_workorder (Shop Floor) và mrp.report (Production Analysis).

**3.3. Lô, hạn dùng, FEFO hoạt động thế nào?**
Mỗi lô có ngày hết hạn; Odoo tính ngày nên dùng, ngày rút khỏi kệ, ngày cảnh báo – ở Odoo 19 là số ngày trước hạn dùng. FEFO: lô hết hạn trước xuất trước; lô quá ngày rút khỏi kệ không được giữ cho đơn.

**3.4. Tồn dự báo là gì? Liên quan kế hoạch sản xuất thế nào?**
Tồn thực + sắp nhập – sắp xuất (đã trừ đơn bán đã xác nhận). Màn hình Bổ sung hàng đề xuất sản xuất cho sản phẩm có tồn dự báo âm. Ví dụ thứ Tư: đề xuất FG01 147, FG02 75, FG04 4, FG07 2 cho đơn thứ Năm.

**3.5. Nhận 1 bước / 2 bước / 3 bước khác nhau? Vì sao chọn 1 bước?**
1 bước: nhận thẳng vào kho. 2 bước: vào khu chờ rồi chuyển vào kho. 3 bước: thêm bước kiểm chất lượng. Chọn 1 bước vì hàng mát không để khu chờ được và xưởng không có khu chờ; kiểm tại cửa trước khi xác nhận phiếu.

**3.6. Sản xuất 2 bước là gì? Vì sao?**
Bước 1: thủ kho cấp NVL từ kho ra Khu sản xuất (phiếu cấp NVL). Bước 2: lệnh sản xuất tiêu hao từ Khu sản xuất. Vì ca đêm kho không có người, thủ kho cấp trước 16:30 cho cả ca.

**3.7. MTO là gì? Dùng ở đâu?**
Make to Order – đơn bán tự sinh lệnh sản xuất riêng. Chỉ dùng cho OEM (khác bao bì, công thức): đơn S00025 300 hộp bông lan sinh WH/MO/00011. Bánh tươi không dùng MTO vì nướng theo mẻ cho tổng đơn của nhiều khách.

**3.8. Gộp lệnh sản xuất, đóng lệnh không làm bù?**
Gộp (Merge) các lệnh cùng sản phẩm thành 1 lệnh/ca. Khi làm thiếu, Odoo hỏi: tạo lệnh bổ sung hoặc đóng lệnh. Bánh tươi chọn đóng (WH/MO/00007: 66 → 58), hàng trữ có thể tạo bổ sung.

**3.9. Tiêu hao linh hoạt (consumption) là gì?**
3 mức: cho phép, cho phép kèm cảnh báo, chặn. Nhóm chọn "cho phép kèm cảnh báo": tiêu hao lệch định mức là bình thường ở bánh nhưng quản đốc phải thấy.

**3.10. Vì sao thợ không bấm giờ công đoạn? Vậy giá thành tính sao?**
Thợ tay dính bột, làm nhiều mẻ xen kẽ, và Shop Floor là Enterprise. Công đoạn vẫn khai trong BoM để tính tải lò và chi phí; khi quản đốc hoàn tất lệnh, Odoo ghi thời gian bằng định mức. Giá thành = NVL thực tế + thời gian định mức × chi phí/giờ khu vực. Giới hạn: phần nhân công là định mức.

**3.11. Batch transfer là gì?**
Gom nhiều phiếu giao của một tuyến thành một đợt để soạn một lần (module stock_picking_batch). 9 đợt = 3 tuyến × 3 ngày.

**3.12. Hợp đồng mua hàng (Blanket Order)?**
Thỏa thuận giá và số lượng dự kiến cả quý với NCC (purchase_requisition). Đơn mua hằng ngày lấy giá từ hợp đồng; 3 hợp đồng: NCC01 bột/đường/dầu, NCC03 bơ/sữa/kem, NCC04 trứng.

**3.13. Kiểm soát hóa đơn theo số đã nhận (bill control) là gì?**
Hóa đơn NCC chỉ được lập theo số lượng đã nhận, không theo số đặt – là "đối chiếu 3 bên": đơn mua – phiếu nhập – hóa đơn. Trứng vỡ: đặt nhiều hơn 60 quả so với nhận, hóa đơn chỉ tính số nhận.

## 4. Câu hỏi theo từng quy trình

**QT1 – Khách nợ quá hạn đặt hàng thì sao?**
BH2a giao việc giám đốc khi tạo đơn; BH2b chặn xác nhận. Giám đốc xem công nợ, gọi khách, đồng ý thì gắn nhãn "Đã duyệt công nợ". Ví dụ KH03: S00003 được duyệt (khách hứa trả 50%), S00020 thứ Tư vẫn bị chặn vì còn nợ quá hạn.

**QT1 – Khách nhận thiếu / không nhận / trả hàng?**
Thiếu: xác nhận số thực, hóa đơn theo số giao (INV/2026/00012: 52/56 ổ). Không nhận: hủy phiếu và đơn, ghi lý do (S00011). Trả hàng: phiếu trả vào Khu cách ly + giấy báo có (RINV/2026/00001, 6 ổ).

**QT1 – Tiền mặt tài xế thu được kiểm soát thế nào?**
Khách có nhãn "Trả tiền mặt cho tài xế"; cuối ngày kế toán ghi thanh toán vào nhật ký tiền mặt theo hóa đơn, đối chiếu tiền tài xế nộp với phiếu giao có chữ ký; chênh lệch ghi cho tài xế.

**QT2 – Trứng vỡ khi giao xử lý ra sao?**
Phiếu QC (BH1 tạo sẵn khi xác nhận đơn mua) ghi "Không đạt"; thủ kho nhận số đạt, không tạo đơn chờ; ghi chú lý do trên phiếu nhập; hóa đơn NCC theo số nhận.

**QT2 – Ai duyệt đơn mua? Vì sao admin tạo thì không phải chờ?**
Đơn trên 20 triệu chờ giám đốc duyệt (duyệt 2 cấp có sẵn trong Purchase). Người có quyền quản lý mua hàng tự duyệt được đơn của mình, nên đơn phải do nhân viên mua (quyền người dùng) tạo: P00002 24,6 triệu đang "Chờ duyệt".

**QT3 – Quản đốc làm gì trên Odoo trong một ngày?**
16:00 mở Bổ sung hàng, chốt số lượng theo mẻ, gộp lệnh; xác nhận, in phiếu; 05:00 nhập sản lượng thực tế, lô, ghi bánh lỗi, đóng lệnh; thứ Hai xem báo cáo sản lượng, bánh lỗi, tải lò.

**QT3 – Truy xuất nguồn gốc khi khách khiếu nại?**
Mở lô thành phẩm (ví dụ FG02-261116) → Truy xuất nguồn gốc: thấy lô NVL đã dùng và các khách đã nhận cùng lô → thu hồi đúng khách.

**QT4 – Module cận hạn khác tính năng có sẵn của Odoo ở đâu?**
Odoo chỉ có một ngày cảnh báo mỗi lô. Module có ngưỡng nhiều mức theo nhóm (bánh mì thu hồi ≤ 40%, cookies giảm giá ≤ 30%…), tạo việc giao người xử lý, biết lô đang nằm ở khách nào để thu hồi, đề xuất giá xả, nút hủy ghi tổn thất, báo cáo tổn thất.

**QT4 – Vì sao Khu cách ly phải nằm ngoài Tồn kho?**
Nếu nằm trong, hàng trả về và hàng hết hạn vẫn được tính là hàng bán được: có thể bị giữ cho đơn giao, và làm tồn dự báo cao nên quản đốc không thấy cần sản xuất (nhóm đã gặp đúng lỗi này với bánh lạnh và đã sửa).

**QT5 – Webhook ngân hàng hoạt động thế nào? Chống trùng ra sao?**
Ngân hàng gửi POST có secret; Odoo kiểm secret, nếu mã giao dịch đã có thì đánh dấu trùng, nếu không thì tìm số hóa đơn trong nội dung chuyển khoản (bỏ dấu "/"), ghi nhận thanh toán bằng chính wizard thanh toán của Odoo.

**QT5 – Chuyển số dư đầu kỳ làm thế nào?**
Tồn kho: điều chỉnh tồn theo lô ngày go-live. Công nợ: hóa đơn "Số dư đầu kỳ (sổ cũ)" đối ứng TK 4211 cho từng khách/NCC còn nợ, giữ đúng ngày hóa đơn gốc để tính tuổi nợ.

## 5. Kế toán (hay bị hỏi kỹ)

**5.1. Bút toán khi lập hóa đơn bán?**
Nợ 1311 / Có 511, Có 33311 (thuế đầu ra); đồng thời Nợ 632 / Có 155 (giá vốn thành phẩm). Ví dụ INV/2026/00012: Nợ 1311 4.393.180; Có 511 3.993.800; Có 33311 399.380; Nợ 632 / Có 155 3.288.683.

**5.2. Vì sao giá vốn ghi lúc lập hóa đơn, không phải lúc giao hàng?**
Odoo 19 gọi chế độ này là "Perpetual (at invoicing)": bút toán kho ghi khi lập hóa đơn. Giá trị tồn vẫn theo dõi theo từng lần nhập xuất.

**5.3. Hóa đơn NCC ghi gì?**
Nợ 152 (NVL), Nợ 1331 (thuế đầu vào) / Có 3311. Ví dụ trứng: Nợ 152 6.510.000, Nợ 1331 651.000 / Có 3311 7.161.000.

**5.4. Thanh toán ghi vào 1131 là sao?**
1131 là tài khoản tiền đang chuyển (outstanding receipts): khoản thu được ghi nhận trước, khi đối soát với sổ phụ ngân hàng sẽ chuyển sang tiền gửi. Kiến thức từ video eLearning "Payments and outstanding accounts".

**5.5. Giấy báo có hàng trả ghi gì?**
Nợ 511, Nợ 33311 / Có 1311 và Nợ 155 / Có 632 (nhận lại hàng, giảm giá vốn). Ví dụ RINV/2026/00001: 150.000 + 15.000; giá vốn 103.055.

**5.6. Giá vốn AVCO là gì? Vì sao chọn?**
Bình quân gia quyền, cập nhật sau mỗi lần nhập. Phù hợp nguyên liệu giá biến động liên tục (trứng, bơ); FIFO phức tạp hơn khi lô nhỏ, nhiều.

**5.7. Từng có lỗi gì về kế toán?**
Ban đầu giá vốn thành phẩm ghi Có 152 (TK nguyên liệu) vì nhóm thành phẩm dùng TK tồn kho mặc định. Nhóm phát hiện khi đọc bút toán thật và sửa sang 155 cho nhóm Thành phẩm, Phụ phẩm.

## 6. Module và code

**6.1. Module Odoo gồm những gì?**
`__manifest__.py` (tên, phụ thuộc, file dữ liệu), `models/` (Python, ORM), `views/` (XML), `security/ir.model.access.csv` (quyền), `data/` (dữ liệu mặc định, cron), `tests/`, `controllers/` (HTTP).

**6.2. bh_near_expiry kế thừa gì?**
`_inherit = "stock.lot"` thêm trường mức cận hạn; model mới bh.expiry.rule, bh.expiry.log; cron hằng ngày gọi `_bh_cron_check_expiry`; view kế thừa form và danh sách lô bằng XPath.

**6.3. Làm sao biết lô đang ở khách nào?**
Cộng các dòng điều chuyển đã xong của lô đến vị trí khách, trừ các dòng từ vị trí khách về (hàng trả), nhóm theo khách.

**6.4. Test tự động chạy thế nào?**
Lớp TransactionCase / HttpCase; chạy `odoo -d <db thử> -i <module> --test-tags /<module>`. bh_near_expiry 3 test, bh_api 12 test, đều đạt.

**6.5. Automation Rule khác module code ở đâu?**
Automation là cấu hình trên giao diện, code chạy trong sandbox (không import, không gán trực tiếp, không gọi hàm "_"). Module là mã Python đầy đủ, có model, view, test. Dùng Automation cho quy tắc nghiệp vụ đơn giản (chặn đơn, tạo phiếu QC); module cho tính năng mới.

## 7. API và bảo mật

**7.1. Token của bh_api bảo mật thế nào?**
Sinh ngẫu nhiên, chỉ hiện một lần, lưu bản băm SHA-256, so sánh bằng `hmac.compare_digest`; có hạn dùng, thu hồi được; phạm vi quyền; giới hạn số lần gọi mỗi phút; nhật ký mọi lần gọi; chạy dưới quyền người dùng gắn với token.

**7.2. Khách A có xem được đơn của khách B không?**
Không. Truy vấn luôn lọc theo khách gắn với token (child_of commercial partner); test "đơn khách khác bị ẩn" trả 404.

**7.3. JSON-2 khác XML-RPC?**
JSON-2 (mới ở Odoo 19): `POST /json/2/<model>/<method>`, API key trong header Bearer, tham số đặt tên. XML-RPC: đăng nhập `/xmlrpc/2/common`, gọi `execute_kw` ở `/xmlrpc/2/object`, sẽ bị thay dần. Nhóm có script cho cả hai.

**7.4. Ba hệ thống tích hợp là gì?**
Ngân hàng (webhook vào, chạy thật), app đặt hàng của khách (REST API, chạy thật), Google Sheets (webhook ra qua Automation BH4 + Apps Script), thêm Telegram và hóa đơn điện tử Viettel.

**7.5. Mật khẩu, backup, audit trail?**
Mật khẩu tối thiểu 10 ký tự, 2FA cho giám đốc/kế toán, đổi mật khẩu admin. Audit: tracking trên chứng từ, nhật ký API, giao dịch ngân hàng, hóa đơn đã xác nhận không sửa trực tiếp. Backup: pg_dump hằng ngày, quy tắc 3-2-1, thử khôi phục hằng tháng; RPO 1 ngày, RTO 4 giờ.

## 8. Website

**8.1. Website phân tích thiết kế thế nào?**
Mục tiêu (kênh nhận đơn sỉ, cổng công nợ, tìm khách OEM) → người dùng (chủ quán dùng điện thoại, bộ phận mua dùng máy tính) → yêu cầu chức năng / phi chức năng → use case → sơ đồ trang → wireframe 7 khối → design system → kiến trúc theme → kiểm thử (chương 6).

**8.2. Vì sao màu kem – socola – caramel? 60-30-10 là gì?**
Gợi cảm giác bánh mới ra lò. 60% nền kem, 30% lúa mì/socola, 10% caramel cho nút kêu gọi. Mọi cặp chữ/nền đạt WCAG AA (≥ 4,5:1), ví dụ chữ trắng trên caramel 5,7:1.

**8.3. Theme viết bằng gì? Có sửa được không cần code?**
SCSS (biến màu, font trong primary_variables; style riêng tiền tố `.x_custom_`) và QWeb kế thừa trang chủ, footer. Các khối là snippet chuẩn trong oe_structure nên nhân viên sửa chữ, ảnh bằng Website Builder.

**8.4. Đặt hàng trên web đi vào Odoo thế nào?**
Khách đăng nhập → giá theo bảng giá của khách → giỏ hàng → xác nhận → đơn bán trong Odoo; vẫn qua kiểm tra công nợ BH2a/BH2b và vào kế hoạch sản xuất 16:00 như đơn điện thoại.

## 9. Câu hỏi "bẫy" và cách trả lời

**"Quy trình này có thật không hay chỉ vẽ cho đẹp?"** – Mỗi bước trả lời được ai làm, lúc mấy giờ, thay giấy tờ nào; dữ liệu demo có ngoại lệ thật. Chỉ những gì làm được trên Odoo Community mới đưa vào; phần không làm được ghi ở hạn chế.

**"Sao không dùng Quality / Planning / Barcode của Odoo?"** – Là Enterprise. Quality thay bằng OCA quality_control_oca; Planning không cần vì quản đốc xếp ca; Barcode: nhãn lô in sẵn, số lô nhập tay ít.

**"Odoo có sẵn cảnh báo hạn dùng rồi, viết module làm gì?"** – Xem câu QT4 ở mục 4: nhiều mức theo nhóm, việc giao người, lô ở điểm bán, tổn thất.

**"Số liệu giả định thì kết quả có ý nghĩa gì?"** – Giả định được ghi rõ và có bộ câu hỏi để kiểm chứng; cấu hình, quy trình, kiểm soát vẫn đúng; thay số thật chỉ cần sửa dữ liệu nền và chạy lại script.

**"Nếu mất điện, mất mạng?"** – Dùng phiếu giấy dự phòng, nhập bù; máy chủ đặt VPS có sao lưu hằng ngày.

**"Bạn phụ trách phần nào, giải thích code / cấu hình đó?"** – Mỗi bạn chuẩn bị: quy trình chính (bảng đặc tả chương 5), API cá nhân (script trong scripts/), một quy tắc tự động hoặc một phần module.

## 10. Số liệu cần nhớ

| Nội dung | Số |
|---|---|
| Phân hệ / quy trình | 5 / 5 (QT1–QT5) |
| Sản phẩm | 12 thành phẩm, 23 NVL và bao bì, 1 phụ phẩm, 12 BoM, 5 khu vực sản xuất |
| Người dùng | 8 (+ admin) |
| Khách / NCC | 8 khách mẫu, 3 tuyến / 6 NCC, 3 hợp đồng giá |
| Quy tắc tự động | 6 (BH1, BH2a, BH2b, BH3, BH4 tắt, BH5) |
| Module tự viết | 3 (bh_near_expiry 3 test, bh_api 12 test, theme) |
| Tuần go-live | 27 đơn bán, 11 lệnh sản xuất, 9 đợt giao, 10 việc cận hạn |
| Ngưỡng | Duyệt đơn mua 20 triệu; bánh mì thu hồi ≤ 40% hạn còn lại |
