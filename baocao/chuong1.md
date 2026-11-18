# CHƯƠNG 1. GIỚI THIỆU ĐỀ TÀI

## 1.1. Lý do chọn đề tài

Ban đầu nhóm chọn Masan Consumer, sau đó chuyển sang một đại lý tạp hóa. Cả hai lựa chọn đều không phù hợp với yêu cầu của môn học. Masan có quá nhiều công ty con và ngành hàng để khoanh phạm vi trên Odoo. Đại lý tạp hóa thì chỉ mua đi bán lại, không có hoạt động sản xuất nên không triển khai được phân hệ Sản xuất (MRP), Chất lượng (Quality) và Lập kế hoạch (Planning).

Nhóm chọn Công ty TNHH Bánh Bảo Hân vì bốn lý do. Thứ nhất, đây là doanh nghiệp sản xuất thật, có xưởng và có công suất công bố. Thứ hai, quy mô nhỏ (xưởng khoảng 500 m²) nên dựng đủ dữ liệu trên Odoo trong thời gian một học kỳ. Thứ ba, doanh nghiệp bán chủ yếu cho khách tổ chức như quán cà phê, siêu thị, đơn vị suất ăn, trường học, nên có đủ chuỗi báo giá, đơn hàng, giao hàng, hóa đơn và công nợ. Thứ tư, sản phẩm là bánh tươi và bánh cấp đông, hạn dùng ngắn, phải quản lý theo lô. Đây là bài toán cụ thể để nhóm làm module mở rộng.

## 1.2. Nguồn thông tin và phương pháp khảo sát

Nhóm phân biệt rõ hai loại thông tin trong báo cáo:

| Loại thông tin | Nguồn | Cách đánh dấu trong báo cáo |
|---|---|---|
| Thông tin công khai | Hồ sơ doanh nghiệp trên Yellow Pages Việt Nam và Trang Vàng Việt Nam (do doanh nghiệp tự cung cấp) | Ghi nguồn [1], [2] |
| Quy trình chuẩn ngành bánh | Tài liệu nghiên cứu chế biến bánh bông lan [3], hướng dẫn công bố sản phẩm [4], văn bản pháp luật về an toàn thực phẩm và nhãn hàng hóa [5], [6], tài liệu HACCP [7] | Ghi nguồn tương ứng |
| Cơ cấu tổ chức, số liệu vận hành, khó khăn hiện tại | Nhóm giả định dựa trên quy mô công bố và quy trình chuẩn ngành | Ghi "(giả định)" |

Thông tin giả định chỉ phục vụ mục đích học tập và không phải số liệu thực của Bảo Hân. Nhóm đã soạn 32 câu hỏi khảo sát và thực hiện phỏng vấn mô phỏng từ vị trí người quản lý xưởng (Phụ lục B); kết quả được dùng để thiết kế 5 quy trình. Khi liên hệ được doanh nghiệp, nhóm sẽ thay các giả định bằng câu trả lời thực tế và lưu biên bản làm minh chứng khảo sát.

## 1.3. Tổng quan doanh nghiệp

Thông tin công khai [1], [2]:

| Hạng mục | Nội dung |
|---|---|
| Tên doanh nghiệp | Công ty TNHH Bánh Bảo Hân |
| Mã số thuế | 0314345823 |
| Năm thành lập | 2017 |
| Loại hình | Công ty trách nhiệm hữu hạn, nhà sản xuất |
| Trụ sở | 86 Đường 11, KP.5, P. Linh Xuân, TP. Thủ Đức, TP. Hồ Chí Minh |
| Xưởng sản xuất | 71 Đường 20, KP.4, P. Hiệp Bình Chánh, TP. Thủ Đức, TP. Hồ Chí Minh |
| Mặt bằng xưởng | Khoảng 500 m², 2 tầng. Tầng trệt 300 m² sản xuất. Tầng 1 khoảng 200 m² gồm kho nguyên liệu và văn phòng |
| Công suất công bố | Nhận gia công OEM bánh tươi theo yêu cầu, khoảng 10.000 sản phẩm/ngày |
| Thị trường | Toàn quốc |
| Khách hàng | Quán cà phê, trà sữa, quán ăn, tiệc trà, hội nghị; đối tác tiêu biểu: Aeon Mall, Dussmann, Metromart, Kizuna, Đại học FPT và một số trường THPT. Hướng tới siêu thị, cửa hàng tiện lợi, nhà phân phối |

Bảo Hân có hai mảng chính. Mảng thứ nhất là sản phẩm mang thương hiệu riêng, bán sỉ cho quán và đại lý. Mảng thứ hai là gia công OEM, sản xuất theo công thức và bao bì khách đặt.

## 1.4. Cơ cấu sản phẩm và nguyên vật liệu

### 1.4.1. Sản phẩm

Danh mục công khai [1] gồm bánh mì Hoppi, bánh tiệc trà, bánh lạnh, pizza đông lạnh, cookies, bánh cấp đông, đế pizza, vỏ bánh, gia công OEM bánh bông lan và bánh mì. Trang Vàng còn liệt kê bánh mì sandwich đen, bánh mì nguyên cám, đế bánh lớn, đế bánh nhỏ, bánh pizza xúc xích [2].

Trong phạm vi đồ án, nhóm chọn 12 sản phẩm đại diện, chia theo điều kiện bảo quản. Điều kiện bảo quản quyết định hạn dùng và kho chứa. Hạn dùng dưới đây là giả định của nhóm, tham khảo mức phổ biến của từng loại bánh.

| Nhóm | Sản phẩm đại diện | Bảo quản | Hạn dùng (giả định) |
|---|---|---|---|
| Bánh mì tươi | Bánh mì Hoppi, sandwich trắng, sandwich đen, bánh mì nguyên cám | Nhiệt độ thường | 4–5 ngày |
| Bánh ngọt | Bông lan cắt lát (OEM), bánh tiệc trà | Nhiệt độ thường | 15–30 ngày |
| Bánh lạnh | Bánh lạnh mousse | 0–5 °C | 3 ngày |
| Bánh khô | Cookies bơ | Nhiệt độ thường, túi kín | 6 tháng |
| Cấp đông | Đế pizza nhỏ, đế pizza lớn, pizza xúc xích, vỏ bánh | −18 °C | 6 tháng |

Mỗi sản phẩm có nhiều đơn vị tính: cái, gói, thùng (ví dụ 1 thùng = 20 gói = 120 cái). Bán sỉ tính theo thùng, sản xuất tính theo mẻ.

### 1.4.2. Nguyên vật liệu (giả định)

Nhóm chia nguyên vật liệu thành ba kho theo điều kiện bảo quản, vì Odoo cần tách vị trí kho để đi đúng tuyến xuất nhập:

- Kho khô: bột mì, đường, muối, men, bột nở, phụ gia, cacao, dầu ăn.
- Kho mát: bơ, trứng, sữa tươi, kem tươi, phô mai, xúc xích. Đây là nhóm có hạn dùng ngắn, phải quản lý theo lô và xuất theo nguyên tắc hết hạn trước xuất trước (FEFO).
- Kho bao bì: túi in nhãn, khay, thùng carton, tem lô và hạn dùng.

Ví dụ định mức (BoM) cho 1 mẻ 100 bánh mì sandwich trắng 400 g: 23 kg bột mì (vừa một cối trộn 25 kg), 1,5 kg đường, 0,45 kg muối, 0,3 kg men, 1,5 kg bơ, 5 lít sữa tươi, 100 túi, 5 thùng carton. Định mức thật sẽ được thay khi có số liệu khảo sát.

## 1.5. Cơ cấu tổ chức (giả định)

Với công suất khoảng 10.000 sản phẩm/ngày và xưởng 300 m², nhóm ước tính doanh nghiệp có khoảng 26 nhân sự:

| Bộ phận | Số người | Nhiệm vụ chính |
|---|---|---|
| Giám đốc | 1 | Duyệt giá OEM, chiết khấu, đơn vượt hạn mức công nợ, đơn mua lớn, lệnh hủy hàng |
| Kinh doanh | 3 | Tìm khách, báo giá, nhận đơn sỉ và OEM, chăm sóc khách, xử lý đổi trả |
| Mua hàng | 1 | Lập yêu cầu báo giá, đặt nguyên liệu và bao bì, theo dõi nhà cung cấp |
| Kế hoạch – sản xuất | 1 quản đốc, 2 tổ trưởng, 12 công nhân (2 ca) | Lập kế hoạch sản xuất theo đơn và dự báo, vận hành các công đoạn |
| Kiểm soát chất lượng (QC) | 1 | Kiểm nguyên liệu đầu vào, kiểm trong công đoạn, kiểm thành phẩm, lưu mẫu |
| Kho | 2 | Kho nguyên liệu (khô, mát, bao bì) và kho thành phẩm (thường, lạnh, đông) |
| Giao hàng | 2 | Giao theo tuyến, nhận hàng trả về |
| Kế toán | 1 | Hóa đơn, công nợ, thanh toán nhà cung cấp, giá thành, thuế |

Kiểm soát chéo: kinh doanh không tự sửa giá ngoài bảng giá; kho không tự điều chỉnh tồn khi chưa được duyệt; kế toán đối chiếu đơn mua, phiếu nhập và hóa đơn trước khi trả tiền.

## 1.6. Quy trình hoạt động hiện tại

Phần này mô tả quy trình của một xưởng bánh nhỏ theo tài liệu chuẩn ngành [3], [4], [7]. Cách làm thủ công hiện tại (ghi "giả định") sẽ được thay bằng kết quả phỏng vấn.

### 1.6.1. Bán hàng sỉ và OEM

Khách đặt hàng qua điện thoại hoặc Zalo (giả định). Kinh doanh báo giá theo bảng giá sỉ. Với đơn OEM, kinh doanh gửi giá dựa trên công thức khách yêu cầu, giám đốc duyệt. Khách xác nhận thì kinh doanh chuyển đơn cho quản đốc. Hàng giao kèm phiếu giao. Khách sỉ nhỏ trả tiền khi nhận hàng. Siêu thị và đơn vị suất ăn thanh toán theo kỳ, thường 30–45 ngày (giả định).

### 1.6.2. Mua nguyên vật liệu

Thủ kho báo nguyên liệu sắp hết, mua hàng hỏi giá hai đến ba nhà cung cấp rồi đặt hàng. Khi nhận hàng, QC kiểm cảm quan, nhiệt độ hàng mát, hạn dùng và giấy tờ lô. Hàng đạt thì nhập kho, hàng không đạt thì trả lại. Kế toán đối chiếu đơn mua, phiếu nhập và hóa đơn trước khi thanh toán.

### 1.6.3. Sản xuất

Quy trình bánh nướng gồm các bước: chuẩn bị nguyên liệu, phối trộn nguyên liệu và phụ gia, nhào bột, chia bột, nướng, làm nguội, định hình hoặc bơm nhân, đóng gói [3]. Bánh mì có thêm bước ủ men. Trong nghiên cứu bánh bông lan [3], bánh được nướng ở 160 °C mặt trên và 180 °C mặt dưới trong 20 phút. Sản phẩm cấp đông có thêm bước cấp đông nhanh trước khi vào kho −18 °C.

Theo cách tiếp cận HACCP [7], các điểm kiểm soát tới hạn của dây chuyền bánh gồm nhiệt độ và thời gian nướng, dò kim loại sau đóng gói, và nhiệt độ bảo quản hàng lạnh và đông. Kết quả đo phải được ghi lại để chứng minh tuân thủ.

Mỗi mẻ tạo một lô thành phẩm. Nhãn ghi ngày sản xuất và hạn sử dụng theo thứ tự ngày, tháng, năm, đúng yêu cầu ghi nhãn thực phẩm [6].

### 1.6.4. Kho và giao hàng

Thành phẩm được xếp theo nhóm nhiệt độ. Hàng tươi xuất trong ngày hoặc ngày kế tiếp. Xuất kho theo nguyên tắc hết hạn trước xuất trước. Cuối tháng kho kiểm kê nguyên liệu và thành phẩm.

### 1.6.5. Kế toán và công nợ

Kế toán lập hóa đơn theo phiếu giao, theo dõi công nợ từng khách theo kỳ hạn, nhắc nợ khi quá hạn. Phía phải trả, kế toán thanh toán nhà cung cấp theo điều khoản đã thỏa thuận.

## 1.7. Bài toán thực trạng (giả định, cần kiểm chứng khi phỏng vấn)

1. Đơn hàng nhận qua nhiều kênh (điện thoại, Zalo, email) và tổng hợp trên Excel. Kế hoạch sản xuất lập từ bảng này nên dễ thiếu hoặc dư so với đơn. Bánh tươi làm dư thì phải bỏ, làm thiếu thì giao trễ.
2. Định mức nguyên liệu không cập nhật theo công thức mới. Doanh nghiệp khó tính giá thành từng loại bánh, nên giá OEM chủ yếu dựa vào kinh nghiệm.
3. Hạn dùng ngắn và nhiều mức nhiệt bảo quản. Lô được theo dõi bằng sổ tay. Hàng cận hạn ở kho và ở điểm bán thường chỉ được phát hiện khi đã quá muộn để bán.
4. Khi siêu thị hoặc đơn vị suất ăn khiếu nại một lô bánh, doanh nghiệp mất nhiều thời gian truy ngược lô nguyên liệu, ca sản xuất và người kiểm tra.
5. Kết quả kiểm nguyên liệu đầu vào và kiểm trong công đoạn ghi trên giấy, khó thống kê nhà cung cấp nào hay giao hàng không đạt.
6. Công nợ nhiều khách với kỳ hạn khác nhau nhưng được theo dõi trên Excel, dễ quên nhắc nợ và khó biết khách nào sắp vượt hạn mức.
7. Kiểm kê cuối tháng mất nhiều thời gian. Số liệu sổ sách và thực tế lệch nhưng không rõ do hao hụt sản xuất, hư hỏng hay ghi sai.

## 1.8. Phạm vi dự án

### 1.8.1. Phạm vi nghiệp vụ

Nhóm chọn 5 phân hệ thực sự cần cho một xưởng bánh 20–30 người và đúng danh sách nhóm quy trình của môn học (Sales, Purchase, Inventory/MM, Manufacturing, FI). Kiểm soát chất lượng không tách thành phân hệ riêng mà nằm trong Mua hàng (kiểm đầu vào) và Sản xuất (kiểm mẫu thành phẩm), vì xưởng nhỏ chỉ có một người QC.

| # | Quy trình | Phân hệ Odoo | Người dùng chính |
|---|---|---|---|
| QT1 | Nhận đơn, giao hàng theo tuyến, thu tiền (Order to Cash) | Bán hàng, Kho, Kế toán | Nhân viên kinh doanh, thủ kho, kế toán |
| QT2 | Đặt nguyên liệu theo hợp đồng giá, kiểm tại cửa, nhận hàng, trả tiền (Procure to Pay) | Mua hàng, Kho, Chất lượng (OCA), Kế toán | Nhân viên mua hàng, QC, thủ kho, giám đốc |
| QT3 | Kế hoạch mẻ hằng ngày và ghi sản lượng (Manufacturing) | Sản xuất, Kho, Chất lượng (OCA) | Quản đốc (thợ không dùng Odoo) |
| QT4 | Lô, hạn dùng, cận hạn, cách ly, kiểm kê (Material Management) | Kho, module bh_near_expiry | Thủ kho |
| QT5 | Công nợ, thu tiền mặt và chuyển khoản, đối soát (Accounting) | Kế toán, module bh_api | Kế toán, giám đốc |

Không thuộc phạm vi (trình bày lý do ở chương 9): nhân sự và tiền lương, lập lịch ca chi tiết cho thợ (Planning), quét mã vạch (Barcode), bán lẻ tại quầy (POS), bảo trì máy, kê khai thuế.

### 1.8.2. Phạm vi kỹ thuật

- Nền tảng: một hệ thống duy nhất là Odoo 19 Community tự cài (self-hosted) bằng Docker, gồm PostgreSQL 16 và Odoo 19. Nhóm chọn tự cài vì Odoo Online không cho cài module Python tự viết, trong khi đồ án cần module tùy chỉnh chạy chung một cơ sở dữ liệu với các phân hệ chuẩn.
- Phân hệ chuẩn: Sales, Purchase và Purchase Agreements, Inventory (lô, hạn dùng, gom phiếu theo tuyến), Manufacturing, Invoicing với hệ thống tài khoản Việt Nam, hóa đơn điện tử Viettel (cấu hình), Website/eCommerce, CRM, Automation Rules.
- Module cộng đồng OCA cho Odoo 19: quality_control_oca (phiếu kiểm tra chất lượng), account_financial_report (sổ cái, cân đối phát sinh, tuổi nợ), partner_statement (sao kê công nợ).
- Module tự viết: bh_near_expiry (quản lý hàng cận hạn), bh_api (API cho đối tác và webhook ngân hàng), theme_custom_website (giao diện website).
- Tích hợp hệ thống ngoài: cổng biến động số dư ngân hàng (webhook), app đặt hàng của khách sỉ (REST API), Google Sheets (Apps Script), Telegram (Bot API).

## 1.9. Mục tiêu dự án

Mục tiêu được đặt dưới dạng chỉ số đo được. Số liệu nền là giả định và sẽ cập nhật sau khảo sát.

| Mục tiêu | Chỉ số | Hiện tại (giả định) | Sau triển khai |
|---|---|---|---|
| Giảm hàng hủy do quá hạn | Giá trị hàng hủy / doanh thu | 3% | dưới 1% |
| Lập kế hoạch sản xuất theo đơn | Tỷ lệ đơn giao đủ, đúng hạn | 85% | từ 95% |
| Biết giá thành từng sản phẩm | Số sản phẩm có giá thành tính tự động | 0 | 12/12 sản phẩm trong phạm vi |
| Truy xuất nguồn gốc | Thời gian truy từ lô thành phẩm về lô nguyên liệu | 1–2 ngày | dưới 5 phút |
| Kiểm soát công nợ | Nợ quá hạn trên 30 ngày / tổng phải thu | 15% | dưới 5% |
| Kiểm kê | Thời gian kiểm kê toàn kho | 2 ngày | 4 giờ (quét mã vạch) |

## 1.10. Căn cứ pháp lý và chuẩn ngành áp dụng

- Nghị định 15/2018/NĐ-CP hướng dẫn Luật An toàn thực phẩm: sản phẩm bánh phải tự công bố, kèm phiếu kiểm nghiệm còn hiệu lực 12 tháng; cơ sở sản xuất phải có giấy chứng nhận đủ điều kiện an toàn thực phẩm, trừ các trường hợp được miễn [5]. Cục An toàn thực phẩm đã soạn dự thảo sửa đổi nghị định này năm 2025, nhóm cần kiểm tra văn bản hiện hành trước khi nộp.
- Nghị định 43/2017/NĐ-CP, sửa đổi bởi Nghị định 111/2021/NĐ-CP về nhãn hàng hóa: nhãn thực phẩm bắt buộc có định lượng, ngày sản xuất, hạn sử dụng, thành phần [6]. Đây là lý do mỗi lô thành phẩm trên Odoo phải có ngày sản xuất và hạn sử dụng.
- HACCP: phân tích mối nguy, xác định điểm kiểm soát tới hạn, giới hạn tới hạn, giám sát và lưu hồ sơ [7]. Trên Odoo, các điểm kiểm soát này được dựng thành điểm kiểm soát chất lượng (Quality Control Point).

## Tài liệu tham khảo chương 1

[1] Yellow Pages Việt Nam, "Công ty TNHH Bánh Bảo Hân", https://www.yellowpages.vn/lgs/1187841909/cong-ty-tnhh-banh-bao-han.html

[2] Trang Vàng Việt Nam, danh mục sản phẩm của Công ty TNHH Bánh Bảo Hân, https://trangvangvietnam.com/groupspdv/491277/de-pizza.html

[3] Đỗ Thị Cẩm Vân và cộng sự, "Nghiên cứu chế biến bánh bông lan nhân chuối tiêu hồng", Tạp chí Khoa học và Công nghệ, ĐH Công nghiệp Hà Nội, tập 61, số 5(B), 2025, https://vjol.info.vn/dhcnhn/article/view/125634

[4] ACC Group, "Quy trình thực hiện việc công bố chất lượng bánh bông lan", https://accgroup.vn/quy-trinh-thuc-hien-cong-bo-chat-luong-banh-bong-lan

[5] Chính phủ, Nghị định 15/2018/NĐ-CP, https://thuvienphapluat.vn/van-ban/The-thao-Y-te/Nghi-dinh-15-2018-ND-CP-huong-dan-Luat-an-toan-thuc-pham-341254.aspx

[6] Chính phủ, Nghị định 111/2021/NĐ-CP sửa đổi Nghị định 43/2017/NĐ-CP về nhãn hàng hóa, https://thuvienphapluat.vn/van-ban/Thuong-mai/Nghi-dinh-111-2021-ND-CP-sua-doi-Nghi-dinh-43-2017-ND-CP-497099.aspx

[7] Registrar Corp, "Điểm kiểm soát tới hạn (CCP) trong HACCP", https://www.registrarcorp.com/vi/blog/food-beverage/food-safety/critical-control-points/

[8] Odoo eLearning: Inventory, MRP – Manufacturing & Shop Floor, Sales, Purchase, Planning, Quality, Barcode, Accounting and Invoicing, https://www.odoo.com/slides
