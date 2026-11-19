# CHƯƠNG 1. GIỚI THIỆU ĐỀ TÀI

## 1.1. Lý do chọn đề tài

Ban đầu nhóm chọn Masan Consumer, sau đó chuyển sang một đại lý tạp hóa. Cả hai lựa chọn đều không phù hợp với yêu cầu của môn học. Masan có quá nhiều công ty con và ngành hàng để khoanh phạm vi trên Odoo. Đại lý tạp hóa thì chỉ mua đi bán lại, không có hoạt động sản xuất nên không triển khai được phân hệ Sản xuất (MRP), Chất lượng (Quality) và Lập kế hoạch (Planning).

Nhóm chọn Công ty TNHH Bánh Bảo Hân vì bốn lý do. Thứ nhất, đây là doanh nghiệp sản xuất thật, có xưởng và có công suất công bố. Thứ hai, quy mô nhỏ (xưởng khoảng 500 m²) nên dựng đủ dữ liệu trên Odoo trong thời gian một học kỳ. Thứ ba, doanh nghiệp bán chủ yếu cho khách tổ chức như quán cà phê, siêu thị, đơn vị suất ăn, trường học, nên có đủ chuỗi báo giá, đơn hàng, giao hàng, hóa đơn và công nợ. Thứ tư, sản phẩm là bánh tươi và bánh cấp đông, hạn dùng ngắn, phải quản lý theo lô. Đây là bài toán cụ thể để nhóm làm module mở rộng.

## 1.2. Nguồn thông tin và phương pháp khảo sát

Nhóm phân biệt rõ hai loại thông tin trong báo cáo:

Bảng: Nguồn thông tin và cách đánh dấu trong báo cáo

| Loại thông tin | Nguồn | Cách đánh dấu trong báo cáo |
|---|---|---|
| Thông tin công khai | Hồ sơ doanh nghiệp trên Yellow Pages Việt Nam và Trang Vàng Việt Nam (do doanh nghiệp tự cung cấp) | Ghi nguồn [1], [2] |
| Quy trình chuẩn ngành bánh | Tài liệu nghiên cứu chế biến bánh bông lan [3], hướng dẫn công bố sản phẩm [4], văn bản pháp luật về an toàn thực phẩm và nhãn hàng hóa [5], [6], tài liệu HACCP [7] | Ghi nguồn tương ứng |
| Cơ cấu tổ chức, số liệu vận hành, khó khăn hiện tại | Nhóm giả định dựa trên quy mô công bố và quy trình chuẩn ngành | Ghi "(giả định)" |

Thông tin giả định chỉ phục vụ mục đích học tập và không phải số liệu thực của Bảo Hân. Nhóm đã soạn 32 câu hỏi khảo sát và thực hiện phỏng vấn mô phỏng từ vị trí người quản lý xưởng (mục 1.6); kết quả được dùng để thiết kế 5 quy trình. Khi liên hệ được doanh nghiệp, nhóm sẽ thay các giả định bằng câu trả lời thực tế và lưu biên bản làm minh chứng khảo sát.

## 1.3. Tổng quan doanh nghiệp

Thông tin công khai [1], [2]:

Bảng: Thông tin công khai của Công ty TNHH Bánh Bảo Hân

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

Bảng: Sản phẩm đại diện trong phạm vi đồ án

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

Bảng: Cơ cấu tổ chức (giả định)

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

## 1.6. Khảo sát nghiệp vụ: phỏng vấn doanh nghiệp (mô phỏng)

Trước khi thiết kế quy trình, nhóm khảo sát cách xưởng đang vận hành qua phỏng vấn. Kết quả phỏng vấn là đầu vào cho mô tả quy trình hiện tại (mục 1.7), bài toán thực trạng (mục 1.8) và thiết kế 5 quy trình ở chương 3, chương 5.

### 1.6.1. Cách thực hiện

Nhóm chưa liên hệ được Công ty TNHH Bánh Bảo Hân nên thực hiện **phỏng vấn mô phỏng**: nhóm soạn 32 câu hỏi khảo sát theo 5 phân hệ, sau đó trả lời từ vị trí một người quản lý xưởng bánh. Câu trả lời dựa trên ba nguồn: thông tin công khai của Bảo Hân [1], [2]; quy trình chuẩn ngành bánh và quy định an toàn thực phẩm [3]–[7]; ước tính theo quy mô công bố (xưởng 500 m², khoảng 10.000 sản phẩm/ngày).

Mọi số liệu trong mục này trùng với các giả định ở Chương 1, RA_SOAT_QUY_TRINH và dữ liệu demo trên Odoo. Khi phỏng vấn được doanh nghiệp, nhóm dùng lại đúng bộ câu hỏi này và sửa những chỗ khác biệt.

Bảng: Cách thực hiện phỏng vấn mô phỏng

| Mục | Nội dung |
|---|---|
| Hình thức | Mô phỏng theo kịch bản, không phải buổi làm việc với doanh nghiệp |
| Vai được phỏng vấn | Quản lý xưởng kiêm phụ trách kinh doanh của một xưởng bánh quy mô như Bảo Hân |
| Người hỏi | Nhóm 06 |
| Thời lượng tương đương | Khoảng 60 phút, chia 5 phần theo phân hệ |

Ký hiệu: **H** là câu hỏi của nhóm, **Đ** là câu trả lời mô phỏng.

### 1.6.2. Nội dung phỏng vấn

**Phần 1. Tổng quan**

**H1. Hiện công ty có bao nhiêu nhân viên, chia những bộ phận nào?**
Đ: Khoảng 26 người. Giám đốc 1, kinh doanh 3, mua hàng 1, sản xuất có 1 quản đốc, 2 tổ trưởng và 12 thợ chia 2 ca, QC 1, kho 2, tài xế giao hàng 2, kế toán 1.

**H2. Doanh thu tháng khoảng bao nhiêu? Tỷ trọng hàng thương hiệu riêng và hàng OEM?**
Đ: Khoảng 1 tỷ đồng mỗi tháng. Hàng thương hiệu riêng bán sỉ chiếm khoảng 75%, gia công OEM khoảng 25%. OEM ít đơn nhưng mỗi đơn lớn.

**H22. Nếu có phần mềm quản lý, anh/chị muốn nó giải quyết việc gì đầu tiên?**
Đ: Ba việc: biết ngày mai cần làm bao nhiêu bánh mỗi loại, không phải cộng tay từ Zalo; biết lô nào sắp hết hạn và đang nằm ở quán nào để thu về kịp; và không giao tiếp cho khách đang nợ quá hạn.

**Phần 2. Sản phẩm và nguyên liệu**

**H3. Những sản phẩm bán chạy nhất? Mỗi loại hạn dùng bao lâu, bảo quản ở nhiệt độ nào?**
Đ: Chạy nhất là bánh mì Hoppi và bánh mì sandwich, giao mỗi sáng. Bánh mì tươi để nhiệt độ thường, hạn 4–5 ngày. Bánh ngọt, bông lan 15–30 ngày. Bánh lạnh mousse giữ 0–5 °C, chỉ 3 ngày. Cookies đóng túi kín 6 tháng. Đế pizza, pizza xúc xích, vỏ bánh cấp đông −18 °C, 6 tháng.

**H4. Đơn vị bán sỉ là gì? Một thùng bao nhiêu gói?**
Đ: Quán nhỏ đặt theo cái hoặc gói, siêu thị và bếp ăn đặt theo thùng. Ví dụ bánh mì: 1 gói 6 cái, 1 thùng 20 gói là 120 cái. Xưởng thì tính theo mẻ.

**H5. Nguyên liệu chính và nhà cung cấp chính? Có mấy kho?**
Đ: Bột mì, đường, dầu lấy của một mối cố định; men, phụ gia, socola một mối; bơ, sữa, kem một mối hàng mát; trứng một trại riêng; xúc xích, sốt pizza một mối; bao bì một xưởng in. Tổng 6 nhà cung cấp chính. Nguyên liệu chia kho khô, kho mát và kho bao bì; thành phẩm chia khu nhiệt độ thường, tủ mát, tủ đông.

**H6. Định mức một mẻ của một sản phẩm tiêu biểu? Hao hụt bao nhiêu?**
Đ: Bánh mì sandwich 400 g, mẻ 100 ổ dùng khoảng 23 kg bột, 1,5 kg đường, 0,45 kg muối, 0,3 kg men, 1,5 kg bơ, 5 lít sữa tươi, 100 túi, 5 thùng. Một mẻ bị giới hạn bởi cối trộn, khoảng 25 kg bột. Hao hụt thường 2–3% do bánh méo, cháy, rách bao; vụn bánh gom lại làm bột chiên xù.

**Phần 3. Bán hàng, giao hàng, thu tiền**

**H7. Khách đặt hàng qua kênh nào? Trước bao lâu? Có bảng giá riêng cho từng nhóm khách không?**
Đ: Chủ yếu Zalo và điện thoại, vài chuỗi lớn gửi email. Đặt trước một ngày. Có 3 bảng giá: giá sỉ cho quán, giá siêu thị – bếp ăn, giá OEM theo hợp đồng.

**H23. Mấy giờ chốt đơn cho ngày hôm sau? Bao nhiêu phần trăm là đơn cố định?**
Đ: 16 giờ chốt đơn giao sáng mai. Khoảng 70–80% là đơn cố định hằng ngày của quán, bếp ăn, trường học; khách chỉ nhắn khi tăng giảm số lượng.

**H8. Đơn OEM được báo giá thế nào? Ai duyệt?**
Đ: Kinh doanh tính theo công thức và bao bì khách yêu cầu, cộng chi phí nhân công, lò. Giám đốc duyệt giá. Hiện tính giá chủ yếu theo kinh nghiệm vì chưa có giá thành từng loại.

**H24. Có mấy xe, mấy tuyến, mỗi tuyến bao nhiêu điểm giao? Ai soạn hàng, lúc mấy giờ?**
Đ: 2 xe chạy 3 tuyến: Linh Xuân – Linh Trung, Hiệp Bình – Tam Bình, Thủ Đức – Bình Thạnh. Mỗi tuyến 15–20 điểm. Thủ kho soạn theo tuyến từ 5 giờ, xe chạy 6 giờ, giao xong khoảng 10 giờ.

**H9. Khách trả tiền khi nào? Có hạn mức nợ không?**
Đ: Quán nhỏ trả tiền mặt khi nhận. Siêu thị, bếp ăn, trường học trả sau 30 ngày, vài siêu thị lớn đòi 45 ngày. Mỗi khách trả sau có hạn mức, ví dụ bếp ăn khu công nghiệp 80 triệu, siêu thị mini 30 triệu. Khó nhất là khách đã quá hạn mà vẫn đặt, kinh doanh vẫn nhận vì sợ mất khách.

**H25. Bao nhiêu khách trả tiền mặt cho tài xế? Tài xế nộp tiền lúc nào, ai đối chiếu?**
Đ: Khoảng một nửa số điểm giao là quán nhỏ trả tiền mặt. Tài xế về khoảng 10 giờ 30, nộp tiền và phiếu giao có chữ ký cho kế toán; kế toán đối chiếu với phiếu giao.

**H10. Có nhận đổi, trả hàng cận hạn hoặc hàng lỗi không?**
Đ: Hàng lỗi do xưởng thì đổi. Bánh mì còn khoảng 2 ngày hạn mà quán chưa bán hết thì thu về ở chuyến giao sau và ghi giảm tiền cho khách.

**H26. Thu hồi ở chuyến giao sau hay đi riêng? Ai chịu chi phí?**
Đ: Thu ở chuyến giao sau, không chạy riêng. Bánh thu về để riêng, không bán lại, xưởng chịu chi phí. Hiện chỉ biết lô nào ở quán nào nhờ trí nhớ của tài xế.

**Phần 4. Mua hàng và chất lượng đầu vào**

**H11. Khi nào đặt nguyên liệu? Có tồn tối thiểu không? Có so giá không?**
Đ: Thủ kho thấy sắp hết thì báo. Có tồn tối thiểu trong đầu chứ chưa ghi ở đâu. Trứng, sữa, bơ đặt 2–3 lần mỗi tuần; bột, đường mỗi tuần một lần. Đơn lớn trên 20 triệu phải hỏi giám đốc.

**H31. Có hợp đồng giá cố định với nhà cung cấp không? Bao lâu đổi giá?**
Đ: Với mối bột, bơ sữa, trứng thì chốt giá theo quý, đặt hằng ngày theo giá đó. Chỉ hỏi giá khi có nhà cung cấp mới hoặc giá thị trường biến động mạnh.

**H12. Nhận nguyên liệu thì kiểm tra những gì? Hàng không đạt xử lý ra sao?**
Đ: QC và thủ kho kiểm ngay tại cửa khi xe còn đó: nhiệt độ hàng mát, hạn dùng, bao bì, trứng vỡ. Không đạt thì trả lại tài xế nhà cung cấp, nhận bao nhiêu ghi bấy nhiêu, họ không quay lại giao bù trong ngày. Kết quả ghi sổ giấy nên cuối tháng không biết mối nào hay giao lỗi.

**Phần 5. Sản xuất và chất lượng thành phẩm**

**H13, H27. Các công đoạn? Mỗi ngày mấy ca? Ai ghi sổ sản xuất?**
Đ: Trộn – nhào, chia bột, ủ (bánh mì), nướng, làm nguội rồi đóng gói. Ca đêm 22 giờ đến 5 giờ làm bánh mì tươi cho chuyến sáng; ca ngày 7 giờ đến 15 giờ làm bánh ngọt, cookies, hàng cấp đông và OEM. Tổ trưởng cuối ca ghi sổ: làm được bao nhiêu, bao nhiêu cái lỗi. Thợ không ghi gì.

**H14, H28. Có những máy nào? Máy nào là nút thắt?**
Đ: Cối trộn khoảng 25 kg bột mỗi mẻ, tủ ủ, lò nướng, máy đóng gói. Lò nướng là nút thắt, hỏng lò là phải dời mẻ sang ca ngày.

**H15, H29. Ai lập kế hoạch sản xuất ngày mai, dựa trên gì, lúc mấy giờ? Thợ ca đêm lấy nguyên liệu thế nào?**
Đ: Quản đốc lúc 16 giờ, sau khi chốt đơn, cộng tổng đơn và để thêm một ít tồn an toàn. Ca đêm kho không có người nên chiều thủ kho xuất sẵn nguyên liệu cho cả ca ra khu sản xuất.

**H16, H30. Kiểm thành phẩm những gì? Có máy dò kim loại không? Có HACCP không?**
Đ: Chưa có máy dò kim loại. QC lấy mẫu mỗi lô: cảm quan, cân khối lượng, đo nhiệt độ lõi bằng que đo, kiểm nhãn ngày sản xuất và hạn dùng. Áp dụng theo hướng HACCP nhưng ghi chép trên giấy.

**H17. Khi khách khiếu nại một lô, làm sao biết lô đó dùng nguyên liệu nào, ca nào?**
Đ: Phải lục sổ sản xuất và phiếu nhập, mất 1–2 ngày, nhiều khi không ra.

**Phần 6. Kho**

**H18. Xuất kho theo nguyên tắc nào? Hàng cận hạn xử lý thế nào? Mỗi tháng hủy bao nhiêu?**
Đ: Hạn gần xuất trước, nhưng làm bằng mắt nên vẫn sót. Cookies, bánh ngọt cận hạn thì giảm giá cho quán quen; bánh mì không kịp giảm giá nên thu về. Hàng hủy khoảng 3% doanh thu.

**H19. Bao lâu kiểm kê? Mất bao lâu? Thường lệch do đâu?**
Đ: Thứ Bảy đếm kho mát, cuối tháng kiểm toàn bộ, mất khoảng 2 ngày. Lệch do hao hụt sản xuất, hàng hư không ghi và ghi nhầm số.

**Phần 7. Kế toán**

**H20, H32. Đang dùng phần mềm gì? Hóa đơn lập theo từng lần giao hay gộp?**
Đ: Đơn hàng và công nợ theo dõi bằng Excel; khai thuế bằng phần mềm kế toán riêng và HTKK; hóa đơn điện tử qua nhà cung cấp dịch vụ. Hóa đơn lập theo số thực giao mỗi ngày. Khó nhất là công nợ: khoảng 15% phải thu đã quá hạn trên 30 ngày.

**H21. Có tính giá thành từng sản phẩm không?**
Đ: Chưa. Chỉ biết tổng chi phí tháng, không tách được từng loại bánh.

### 1.6.3. Kết quả đưa vào thiết kế

Bảng: Kết quả phỏng vấn đưa vào thiết kế

| Phát hiện từ phỏng vấn | Câu | Đưa vào Odoo |
|---|---|---|
| Đơn cố định, chốt 16 giờ, xưởng nướng theo mẻ cả ngày | H23, H15 | Quản đốc lập lệnh từ màn hình Bổ sung hàng, 1 lệnh/sản phẩm/ca; MTO chỉ cho OEM (QT3) |
| Khách nợ quá hạn vẫn được nhận đơn | H9 | Automation Rule BH2a/BH2b chặn xác nhận đơn, giám đốc gắn nhãn để mở (QT1) |
| 3 tuyến, 15–20 điểm/tuyến, soạn lúc 5 giờ | H24 | Soạn hàng theo đợt cho từng tuyến (QT1, QT4) |
| Quán trả tiền mặt, trả sau qua ngân hàng | H9, H25 | Thanh toán tiền mặt; webhook ngân hàng tự khớp hóa đơn (bh_api, QT5) |
| Thu hồi bánh ở quán dựa vào trí nhớ tài xế | H10, H26, H18 | Module bh_near_expiry: tìm lô cận hạn đang ở điểm bán (QT4) |
| Kiểm hàng tại cửa, không giao bù | H12 | Nhận 1 bước, phiếu QC khi xe đến, nhận thiếu không tạo đơn chờ (QT2) |
| Giá chốt theo quý, đơn trên 20 triệu hỏi giám đốc | H11, H31 | Thỏa thuận mua hàng; duyệt đơn mua trên 20.000.000 VND (QT2) |
| Ca đêm kho không có người | H29 | Sản xuất 2 bước: cấp NVL ra khu sản xuất cho cả ca (QT3) |
| Thợ không ghi sổ, tổ trưởng ghi cuối ca | H27 | Quản đốc nhập sản lượng thực tế và lô; không bấm giờ công đoạn (QT3) |
| Không có máy dò kim loại | H30 | Điểm kiểm soát chất lượng: cảm quan, khối lượng, nhiệt độ lõi, nhãn (QT3) |
| Truy xuất lô mất 1–2 ngày | H17 | Lô thành phẩm và lô NVL liên kết qua lệnh sản xuất |
| Chưa có giá thành | H21 | BoM theo khối lượng thực tế, giá vốn bình quân, bút toán 632/155 (QT5) |
| Khai thuế bằng phần mềm riêng | H20 | Odoo làm quản trị công nợ, giá vốn; không thay phần mềm khai thuế |

## 1.7. Quy trình hoạt động hiện tại

Phần này mô tả quy trình của một xưởng bánh nhỏ theo tài liệu chuẩn ngành [3], [4], [7]. Cách làm thủ công hiện tại (ghi "giả định") lấy từ phỏng vấn mô phỏng ở mục 1.6; khi phỏng vấn thật sẽ cập nhật.

### 1.7.1. Bán hàng sỉ và OEM

Khách đặt hàng qua điện thoại hoặc Zalo (giả định). Kinh doanh báo giá theo bảng giá sỉ. Với đơn OEM, kinh doanh gửi giá dựa trên công thức khách yêu cầu, giám đốc duyệt. Khách xác nhận thì kinh doanh chuyển đơn cho quản đốc. Hàng giao kèm phiếu giao. Khách sỉ nhỏ trả tiền khi nhận hàng. Siêu thị và đơn vị suất ăn thanh toán theo kỳ, thường 30–45 ngày (giả định).

### 1.7.2. Mua nguyên vật liệu

Thủ kho báo nguyên liệu sắp hết, mua hàng hỏi giá hai đến ba nhà cung cấp rồi đặt hàng. Khi nhận hàng, QC kiểm cảm quan, nhiệt độ hàng mát, hạn dùng và giấy tờ lô. Hàng đạt thì nhập kho, hàng không đạt thì trả lại. Kế toán đối chiếu đơn mua, phiếu nhập và hóa đơn trước khi thanh toán.

### 1.7.3. Sản xuất

Quy trình bánh nướng gồm các bước: chuẩn bị nguyên liệu, phối trộn nguyên liệu và phụ gia, nhào bột, chia bột, nướng, làm nguội, định hình hoặc bơm nhân, đóng gói [3]. Bánh mì có thêm bước ủ men. Trong nghiên cứu bánh bông lan [3], bánh được nướng ở 160 °C mặt trên và 180 °C mặt dưới trong 20 phút. Sản phẩm cấp đông có thêm bước cấp đông nhanh trước khi vào kho −18 °C.

Theo cách tiếp cận HACCP [7], các điểm kiểm soát tới hạn của dây chuyền bánh gồm nhiệt độ và thời gian nướng, dò kim loại sau đóng gói, và nhiệt độ bảo quản hàng lạnh và đông. Kết quả đo phải được ghi lại để chứng minh tuân thủ.

Mỗi mẻ tạo một lô thành phẩm. Nhãn ghi ngày sản xuất và hạn sử dụng theo thứ tự ngày, tháng, năm, đúng yêu cầu ghi nhãn thực phẩm [6].

### 1.7.4. Kho và giao hàng

Thành phẩm được xếp theo nhóm nhiệt độ. Hàng tươi xuất trong ngày hoặc ngày kế tiếp. Xuất kho theo nguyên tắc hết hạn trước xuất trước. Cuối tháng kho kiểm kê nguyên liệu và thành phẩm.

### 1.7.5. Kế toán và công nợ

Kế toán lập hóa đơn theo phiếu giao, theo dõi công nợ từng khách theo kỳ hạn, nhắc nợ khi quá hạn. Phía phải trả, kế toán thanh toán nhà cung cấp theo điều khoản đã thỏa thuận.

## 1.8. Bài toán thực trạng (rút ra từ phỏng vấn mô phỏng, cần kiểm chứng)

1. Đơn hàng nhận qua nhiều kênh (điện thoại, Zalo, email) và tổng hợp trên Excel. Kế hoạch sản xuất lập từ bảng này nên dễ thiếu hoặc dư so với đơn. Bánh tươi làm dư thì phải bỏ, làm thiếu thì giao trễ.
2. Định mức nguyên liệu không cập nhật theo công thức mới. Doanh nghiệp khó tính giá thành từng loại bánh, nên giá OEM chủ yếu dựa vào kinh nghiệm.
3. Hạn dùng ngắn và nhiều mức nhiệt bảo quản. Lô được theo dõi bằng sổ tay. Hàng cận hạn ở kho và ở điểm bán thường chỉ được phát hiện khi đã quá muộn để bán.
4. Khi siêu thị hoặc đơn vị suất ăn khiếu nại một lô bánh, doanh nghiệp mất nhiều thời gian truy ngược lô nguyên liệu, ca sản xuất và người kiểm tra.
5. Kết quả kiểm nguyên liệu đầu vào và kiểm trong công đoạn ghi trên giấy, khó thống kê nhà cung cấp nào hay giao hàng không đạt.
6. Công nợ nhiều khách với kỳ hạn khác nhau nhưng được theo dõi trên Excel, dễ quên nhắc nợ và khó biết khách nào sắp vượt hạn mức.
7. Kiểm kê cuối tháng mất nhiều thời gian. Số liệu sổ sách và thực tế lệch nhưng không rõ do hao hụt sản xuất, hư hỏng hay ghi sai.

## 1.9. Phạm vi dự án

### 1.9.1. Phạm vi nghiệp vụ

Nhóm chọn 5 phân hệ thực sự cần cho một xưởng bánh 20–30 người và đúng danh sách nhóm quy trình của môn học (Sales, Purchase, Inventory/MM, Manufacturing, FI). Kiểm soát chất lượng không tách thành phân hệ riêng mà nằm trong Mua hàng (kiểm đầu vào) và Sản xuất (kiểm mẫu thành phẩm), vì xưởng nhỏ chỉ có một người QC.

Bảng: Phạm vi nghiệp vụ: 5 quy trình và phân hệ Odoo

| # | Quy trình | Phân hệ Odoo | Người dùng chính |
|---|---|---|---|
| QT1 | Nhận đơn, giao hàng theo tuyến, thu tiền (Order to Cash) | Bán hàng, Kho, Kế toán | Nhân viên kinh doanh, thủ kho, kế toán |
| QT2 | Đặt nguyên liệu theo hợp đồng giá, kiểm tại cửa, nhận hàng, trả tiền (Procure to Pay) | Mua hàng, Kho, Chất lượng (OCA), Kế toán | Nhân viên mua hàng, QC, thủ kho, giám đốc |
| QT3 | Kế hoạch mẻ hằng ngày và ghi sản lượng (Manufacturing) | Sản xuất, Kho, Chất lượng (OCA) | Quản đốc (thợ không dùng Odoo) |
| QT4 | Lô, hạn dùng, cận hạn, cách ly, kiểm kê (Material Management) | Kho, module bh_near_expiry | Thủ kho |
| QT5 | Công nợ, thu tiền mặt và chuyển khoản, đối soát (Accounting) | Kế toán, module bh_api | Kế toán, giám đốc |

Không thuộc phạm vi (trình bày lý do ở chương 9): nhân sự và tiền lương, lập lịch ca chi tiết cho thợ (Planning), quét mã vạch (Barcode), bán lẻ tại quầy (POS), bảo trì máy, kê khai thuế.

### 1.9.2. Phạm vi kỹ thuật

- Nền tảng: một hệ thống duy nhất là Odoo 19 Community tự cài (self-hosted) bằng Docker, gồm PostgreSQL 16 và Odoo 19. Nhóm chọn tự cài vì Odoo Online không cho cài module Python tự viết, trong khi đồ án cần module tùy chỉnh chạy chung một cơ sở dữ liệu với các phân hệ chuẩn.
- Phân hệ chuẩn: Sales, Purchase và Purchase Agreements, Inventory (lô, hạn dùng, gom phiếu theo tuyến), Manufacturing, Invoicing với hệ thống tài khoản Việt Nam, hóa đơn điện tử Viettel (cấu hình), Website/eCommerce, CRM, Automation Rules.
- Module cộng đồng OCA cho Odoo 19: quality_control_oca (phiếu kiểm tra chất lượng), account_financial_report (sổ cái, cân đối phát sinh, tuổi nợ), partner_statement (sao kê công nợ).
- Module tự viết: bh_near_expiry (quản lý hàng cận hạn), bh_api (API cho đối tác và webhook ngân hàng), theme_custom_website (giao diện website).
- Tích hợp hệ thống ngoài: cổng biến động số dư ngân hàng (webhook), app đặt hàng của khách sỉ (REST API), Google Sheets (Apps Script), Telegram (Bot API).

## 1.10. Mục tiêu dự án

Mục tiêu được đặt dưới dạng chỉ số đo được. Số liệu nền là giả định và sẽ cập nhật sau khảo sát.

Bảng: Mục tiêu dự án và chỉ số đo

| Mục tiêu | Chỉ số | Hiện tại (giả định) | Sau triển khai |
|---|---|---|---|
| Giảm hàng hủy do quá hạn | Giá trị hàng hủy / doanh thu | 3% | dưới 1% |
| Lập kế hoạch sản xuất theo đơn | Tỷ lệ đơn giao đủ, đúng hạn | 85% | từ 95% |
| Biết giá thành từng sản phẩm | Số sản phẩm có giá thành tính tự động | 0 | 12/12 sản phẩm trong phạm vi |
| Truy xuất nguồn gốc | Thời gian truy từ lô thành phẩm về lô nguyên liệu | 1–2 ngày | dưới 5 phút |
| Kiểm soát công nợ | Nợ quá hạn trên 30 ngày / tổng phải thu | 15% | dưới 5% |
| Kiểm kê | Thời gian kiểm kê toàn kho | 2 ngày | 4 giờ (đếm theo vị trí, lô in sẵn) |

## 1.11. Các bên liên quan và nhân sự dự án

Phía doanh nghiệp là các chức danh theo cơ cấu tổ chức giả định ở mục 1.5; mỗi chức danh là người dùng chính (key user) của một quy trình, tham gia khảo sát, chạy thử và nghiệm thu. Phía nhóm dự án là 3 thành viên, chia việc theo quy trình (chi tiết ở mục 9.1).

Bảng: Các bên liên quan của dự án

| Bên liên quan | Vai trò trong dự án | Quy trình liên quan |
|---|---|---|
| Giám đốc (giả định) | Bảo trợ dự án; duyệt phạm vi, đơn mua trên 20 triệu, mở chặn công nợ; nghiệm thu go-live | QT1; QT2; QT5 |
| Quản đốc xưởng (giả định) | Người dùng chính phân hệ Sản xuất; cung cấp định mức, lịch ca | QT3 |
| Nhân viên kinh doanh (giả định) | Nhập đơn, bảng giá theo khách | QT1 |
| Nhân viên mua hàng, QC (giả định) | Đặt NVL theo hợp đồng giá; kiểm hàng tại cửa và kiểm mẫu thành phẩm | QT2; QT3 |
| Thủ kho (giả định) | Nhận, cấp, soạn, giao hàng; xử lý cận hạn; kiểm kê | QT1; QT4 |
| Kế toán (giả định) | Hóa đơn, thu chi, đối soát, công nợ, giá vốn | QT5 |
| Khách hàng sỉ, nhà cung cấp, ngân hàng | Bên ngoài: đặt hàng qua API, giao NVL, gửi biến động số dư qua webhook | QT1; QT2; QT5 |
| Giảng viên hướng dẫn: ThS. Văn Đức Sơn Hà | Hướng dẫn, đánh giá đồ án | Toàn bộ |

Bảng: Nhân sự nhóm dự án

| Thành viên | MSSV | Vai trò trong dự án |
|---|---|---|
| Lê Thị Thanh Tiền | 24521769 | Phụ trách QT1 Bán hàng; module bh_api, API REST; chốt BPMN, gom báo cáo |
| Đoàn Thị Thùy Trang | 24521817 | Phụ trách QT2 Mua hàng và QT5 Công nợ; API XML-RPC; Automation phiếu QC, Google Sheets, website |
| Phạm Tuấn Hải | 24520442 | Phụ trách QT3 Sản xuất và QT4 Kho; API JSON-2; dữ liệu demo, module bh_near_expiry, Telegram |

## 1.12. Sản phẩm chuyển giao và tiêu chí thành công

Sản phẩm chuyển giao (danh sách và vị trí thư mục ở Phụ lục A):

- Hệ thống Odoo 19 Community cài bằng Docker, cấu hình cho Bảo Hân, kèm script dựng lại toàn bộ trong khoảng 5 phút.
- Dữ liệu nền (sản phẩm, NVL, định mức, khách hàng, nhà cung cấp, bảng giá) dạng file import và dữ liệu tuần đầu go-live 14–18/11/2026.
- 6 sơ đồ BPMN (tổng quan và 5 quy trình) dạng file .bpmn mở bằng Camunda Modeler, kèm ảnh.
- Module bh_near_expiry, module bh_api, theme website, các Automation Rules và tích hợp với hệ thống ngoài.
- Báo cáo, hướng dẫn cài đặt và kiểm tra, video thao tác của từng thành viên, slide thuyết trình.

Tiêu chí đánh giá thành công:

1. Đủ các tiêu chí của môn học: cài đặt, cấu hình, dữ liệu nền, tối thiểu 4 quy trình hoàn chỉnh có BPMN, API, Automation Rules, module mới, tích hợp từ 3 hệ thống ngoài, website.
2. Năm quy trình chạy trọn trên dữ liệu tuần go-live, gồm cả các tình huống ngoại lệ, không phát sinh lỗi hệ thống.
3. Số liệu khớp nhau giữa các phân hệ: tồn kho sau nhập, xuất, sản xuất đúng định mức; hóa đơn theo số thực giao; bút toán giá vốn và công nợ đúng tài khoản.
4. Mỗi người dùng chỉ thấy và làm được phần việc theo vai trò (ma trận phân quyền ở mục 3.4).
5. Các chỉ số ở mục 1.10 đo được trên hệ thống sau go-live.

## 1.13. Căn cứ pháp lý và chuẩn ngành áp dụng

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
