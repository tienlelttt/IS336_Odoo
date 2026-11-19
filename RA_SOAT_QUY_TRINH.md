# Thiết kế quy trình vận hành thực tế – Công ty TNHH Bánh Bảo Hân

Bản 2 (18/11/2026), thay cho bản rà soát trước. Viết từ vị trí doanh nghiệp: quy trình phải là việc nhân viên thật sự làm mỗi ngày, Odoo chỉ ghi lại và kiểm soát việc đó.

## 0. Nguyên tắc thiết kế

1. **Mỗi chứng từ trên Odoo thay một giấy tờ đang có**: phiếu giao hàng, phiếu nhập kho, sổ sản xuất, sổ công nợ. Không tạo thêm bước nhập liệu mà không ai có thời gian làm.
2. **Ai nhập, lúc nào, trên thiết bị gì** phải rõ. Thợ làm bánh không nhập liệu; tổ trưởng ghi sản lượng cuối ca; thủ kho dùng máy tính bảng ở kho; tài xế chỉ cần phiếu giao in sẵn.
3. **Kiểm soát chỉ đặt ở nơi có rủi ro thật**: tiền (công nợ, thu tiền mặt), hàng (hao hụt, hết hạn), an toàn thực phẩm (lô, hạn dùng, nhiệt độ hàng mát).
4. **Không dùng Odoo cho việc làm tay nhanh hơn**: ví dụ không bấm giờ từng công đoạn, không duyệt từng đơn hàng lặp lại.
5. **Giả định ghi rõ** và có câu hỏi kiểm chứng ở Phụ lục A (mục 7).

## 1. Một ngày vận hành của xưởng (giả định, cần kiểm chứng)

| Giờ | Bộ phận | Việc thực tế | Trên Odoo |
|---|---|---|---|
| 06:00–10:00 | Tài xế (2 xe, 3 tuyến) | Giao bánh theo tuyến; quán nhỏ trả tiền mặt; thu hồi bánh ế, cận hạn theo thỏa thuận; khách ký phiếu giao | Phiếu giao in từ Odoo (có lô, hạn dùng); không thao tác trên máy |
| 07:00–09:00 | Thủ kho + QC | Nhận trứng, sữa, bơ (2–3 lần/tuần), bột, đường (1 lần/tuần) tại cửa kho; kiểm nhiệt độ, hạn dùng, trứng vỡ | Phiếu nhập: nhập lô, hạn dùng, số lượng đạt; phiếu QC |
| 10:30–11:00 | Tài xế → Kế toán, Kho | Nộp tiền mặt, phiếu giao có chữ ký; giao lại hàng thu hồi | Kế toán ghi thu tiền mặt; kho nhận hàng trả vào Khu cách ly |
| 08:00–16:00 | Kinh doanh | Nhận đơn qua Zalo, điện thoại, cổng khách hàng, app của khách; phần lớn là đơn cố định hằng ngày có điều chỉnh | Đơn bán cho ngày giao hôm sau; khách nợ quá hạn bị chặn xác nhận |
| 07:00–15:00 | Ca ngày sản xuất | Bánh ngọt, cookies, cấp đông, đơn OEM | Lệnh sản xuất ca ngày |
| 16:00 | Chốt đơn | Hết giờ nhận đơn giao sáng mai | — |
| 16:00–16:30 | Quản đốc | Xem tổng nhu cầu ngày mai (đơn đã chốt + tồn tối thiểu), lên số mẻ; báo mua nếu thiếu nguyên liệu | Bổ sung hàng → sinh 1 lệnh sản xuất / sản phẩm / ca |
| 16:30–17:30 | Thủ kho | Xuất nguyên liệu cho ca đêm ra khu sản xuất (một phiếu cho cả ca) | Phiếu cấp NVL; lô giữ theo FEFO |
| 17:00 | Thủ kho | Đếm nhanh thành phẩm tồn cuối ngày (vài phút) | Điều chỉnh tồn vị trí thành phẩm |
| 22:00–05:00 | Ca đêm sản xuất | Làm bánh mì tươi cho chuyến giao sáng | Không thao tác |
| 05:00 | Tổ trưởng ca đêm | Ghi sản lượng thực tế, bánh lỗi vào sổ sản xuất; QC lấy mẫu kiểm | Hoàn tất lệnh sản xuất; phiếu hủy bánh lỗi; phiếu QC |
| 05:00–06:00 | Thủ kho | Soạn hàng theo tuyến, xếp lên xe | Soạn hàng theo đợt (batch) cho từng tuyến |
| 23:00 | Hệ thống | Tính % hạn dùng còn lại của từng lô | Việc cận hạn cho ngày hôm sau |

Nhịp tuần: kiểm kê kho mát (thứ Bảy); đặt bột, đường; thanh toán nhà cung cấp đến hạn.
Nhịp tháng: kiểm kê toàn bộ; gửi sao kê công nợ cho khách trả sau; báo cáo giá thành, hao hụt, doanh thu; xem lại hạn mức nợ.

## 2. Những gì đã bỏ hoặc sửa so với thiết kế trước, và vì sao

| Thiết kế trước | Thiết kế mới | Lý do thực tế |
|---|---|---|
| Mỗi đơn bán bánh tươi sinh một lệnh sản xuất (MTO) | Gom nhu cầu ngày mai thành 1 lệnh / sản phẩm / ca qua màn hình Bổ sung hàng; MTO chỉ dùng cho đơn OEM | Hàng chục quán đặt cùng loại bánh mì; xưởng nướng theo mẻ cho cả ngày, không nướng riêng cho từng khách. OEM khác bao bì, công thức nên phải làm riêng |
| Thợ bấm Bắt đầu / Kết thúc từng công đoạn | Công đoạn chỉ dùng để tính công suất lò và chi phí theo thời gian định mức; tổ trưởng ghi sản lượng cuối ca | Thợ tay dính bột, làm nhiều mẻ xen kẽ; bấm giờ từng bước là không ai làm và số liệu sẽ sai |
| Giám đốc duyệt mọi báo giá trên 10 triệu | Chặn xác nhận đơn khi khách có nợ quá hạn hoặc vượt hạn mức; giám đốc gắn nhãn "Đã duyệt công nợ" để mở. Báo giá chỉ dùng cho khách mới và OEM | Đơn lặp lại hằng ngày của bếp ăn dễ vượt 10 triệu nhưng không có rủi ro mới. Rủi ro thật là khách nợ lâu vẫn được giao hàng |
| Nhận hàng 2 bước: khu chờ → kiểm → nhập kho | Nhận 1 bước, kiểm ngay tại cửa trước khi xác nhận phiếu; hàng không đạt trả lại tài xế NCC ngay | Hàng mát không thể nằm khu chờ; xưởng 500 m² không có khu chờ riêng; thực tế kiểm khi xe còn ở cửa |
| Phiếu QC tạo sau khi nhận xong | Phiếu QC tạo khi phiếu nhập ở trạng thái Sẵn sàng (xe đến) | Phải kiểm trước khi nhận thì mới từ chối được |
| QC sản xuất có máy dò kim loại | Kiểm mẫu mỗi lô: cảm quan, khối lượng, nhãn ngày, nhiệt độ lõi (que đo) | Xưởng nhỏ thường không có máy dò kim loại; que đo nhiệt và cân mẫu là đủ khả thi |
| Sản xuất 1 bước (thợ tự lấy NVL trong kho) | Sản xuất 2 bước: thủ kho cấp NVL ra khu sản xuất một lần cho cả ca | Thủ kho chịu trách nhiệm tồn; xưởng làm ca đêm khi kho không có người |
| Giao 2 bước, mỗi đơn một phiếu | Soạn hàng theo đợt (batch) cho từng tuyến xe, rồi giao từng khách | Tài xế giao 15–20 điểm/tuyến; soạn theo tuyến nhanh hơn và ít nhầm |
| Hóa đơn tạo thủ công theo đơn | Cuối ngày tạo hóa đơn hàng loạt cho mọi đơn đã giao, theo số lượng thực giao; hóa đơn điện tử qua nhà cung cấp (Viettel S-Invoice có sẵn module) | Giao hằng ngày nhiều khách; hóa đơn điện tử là bắt buộc ở Việt Nam |
| Thu tiền chỉ qua chuyển khoản | Quán nhỏ trả tiền mặt cho tài xế; tài xế nộp quỹ; bếp ăn, siêu thị trả sau qua ngân hàng (webhook) | Đúng tập quán giao bánh sỉ |
| Mua hàng: hỏi giá, so sánh mỗi lần | Hợp đồng giá theo quý với NCC chính (thỏa thuận mua hàng); hằng ngày chỉ đặt theo giá hợp đồng; hỏi giá chỉ khi có NCC mới hoặc giá biến động | NCC trứng, sữa, bột là cố định; không ai đi hỏi giá mỗi lần đặt |
| Mức cận hạn giống nhau cho mọi bánh | Quy tắc riêng theo nhóm: bánh mì tươi còn ≤ 40% → thu hồi ở chuyến giao sau; bánh ngọt, cookies, cấp đông theo 50/30/15% | Bánh mì 5 ngày không có thời gian "giảm giá" như cookies 6 tháng |
| Nhận NVL bị "giao bù" khi không đạt | Không đạt thì không nhận; nhận ít hơn đặt, không tạo đơn chờ; hóa đơn NCC chỉ theo số đã nhận | Thực tế NCC trứng không quay lại giao bù trong ngày |

## 3. Năm phân hệ

### 3.1. Bán hàng – QT1 Nhận đơn, giao hàng, thu tiền

**Bối cảnh.** Khách chia 3 nhóm, khác nhau về cách đặt và trả tiền:

| Nhóm | Ví dụ (KH mẫu) | Đặt hàng | Thanh toán | Đổi trả |
|---|---|---|---|---|
| Quán cà phê, trà sữa, tạp hóa | KH01, KH02 | Đơn cố định hằng ngày, điều chỉnh qua Zalo | Tiền mặt cho tài xế hoặc chuyển khoản ngay | Thu hồi bánh mì quá hạn ở chuyến sau |
| Bếp ăn, siêu thị, trường học | KH03, KH04, KH05 | Đơn theo tuần, có hợp đồng | Trả sau 30 ngày, có hạn mức nợ | Trả hàng cận hạn theo hợp đồng |
| OEM | KH06 | Hợp đồng, báo giá riêng, đơn theo lô | Trả sau 30 ngày | Theo lô, có truy xuất |

**Luồng.**

| # | Ai | Việc | Trên Odoo | Thay cho |
|---|---|---|---|---|
| 1 | Kinh doanh | Khách mới / OEM: gửi báo giá theo bảng giá hoặc giá thương lượng | Báo giá; giảm giá vượt mức cho phép → giám đốc duyệt | Báo giá Word |
| 2 | Kinh doanh / khách | Nhận đơn ngày mai (Zalo, điện thoại); khách lớn tự đặt trên cổng hoặc qua API | Đơn bán, ngày giao = ngày mai; đơn cố định: nhân bản đơn tuần trước | Sổ ghi đơn |
| 3 | Hệ thống | Khách có hóa đơn quá hạn hoặc vượt hạn mức → không cho xác nhận, giao việc giám đốc | Automation chặn xác nhận; giám đốc gắn nhãn "Đã duyệt công nợ" | Giám đốc nhớ trong đầu |
| 4 | Kinh doanh | Xác nhận đơn trước 16:00 | Đơn bán xác nhận → nhu cầu cho kế hoạch sản xuất | |
| 5 | Thủ kho | 05:00 soạn hàng theo tuyến (đợt) | Đợt soạn hàng theo tuyến; lô giữ theo FEFO | Danh sách soạn viết tay |
| 6 | Tài xế | Giao, khách ký phiếu giao; nhận hàng thu hồi | In phiếu giao có lô, hạn dùng | Phiếu giao viết tay |
| 7 | Thủ kho | Tài xế về: xác nhận số giao thực tế (khách nhận thiếu → ghi số thực), nhận hàng trả vào Khu cách ly | Xác nhận phiếu giao; phiếu trả hàng | |
| 8 | Kế toán | Tạo hóa đơn hàng loạt cho đơn đã giao; phát hành hóa đơn điện tử | Hóa đơn theo số đã giao | Hóa đơn giấy |
| 9 | Kế toán | Ghi tiền mặt tài xế nộp; chuyển khoản tự ghi nhận qua webhook | Thanh toán tiền mặt / ngân hàng | Sổ quỹ |
| 10 | Kế toán | Hàng trả, hàng thiếu → giấy báo có | Credit note | |
| 11 | Kế toán | Cuối tháng gửi sao kê công nợ; quá hạn → nhắc nợ | Sao kê (OCA), BH3 | Sổ công nợ Excel |

**Kiểm soát.** Giá lấy từ bảng giá theo khách, nhân viên không sửa giá ngoài mức cho phép; chặn đơn khi nợ quá hạn; hóa đơn chỉ theo số thực giao; tiền mặt tài xế đối chiếu với phiếu giao trong ngày.

**Ngoại lệ.** Khách đổi số lượng sau 16:00 (giao từ tồn dự phòng, không sửa kế hoạch); khách không có mặt nhận hàng (giao lại hoặc hoàn về, phiếu giao ghi 0); thiếu hàng do mẻ hỏng (giao thiếu, không tạo đơn chờ cho bánh tươi, giảm trừ hóa đơn); khách chuyển khoản sai nội dung (giao dịch "không khớp", đối soát tay); khách trả hàng lỗi (phiếu trả + credit note).

**Báo cáo.** Người dùng: đơn ngày mai theo tuyến, đơn chưa giao, đơn chưa xuất hóa đơn. Quản lý: doanh thu theo khách / sản phẩm / tuyến / tháng, tỷ lệ hàng trả theo khách, tuổi nợ, khách bị chặn.

**Không làm trên Odoo.** Định tuyến xe tối ưu (tài xế quen tuyến); ký nhận điện tử (khách ký giấy, ảnh chụp đính kèm nếu cần).

**Bài học eLearning Sales.** Your First Quotation, Quotation Templates, Online Quotation, Invoicing Policies (delivered), Pricelists, Delivery; Accounting: Customer invoice from SO, Credit note, Payment follow-up; Inventory: Batch Transfers, Custom Returns.

### 3.2. Mua hàng – QT2 Đặt nguyên liệu, nhận hàng, trả tiền

**Bối cảnh.** 6 NCC cố định. Hàng mát (trứng, sữa, bơ, kem) giao 2–3 lần/tuần, hạn ngắn, không được tồn nhiều. Hàng khô (bột, đường) đặt mỗi tuần theo xe. Giá chốt theo quý; đơn bột lớn cần giám đốc duyệt. NCC trứng nhận tiền mặt khi giao; NCC lớn trả theo kỳ.

**Luồng.**

| # | Ai | Việc | Trên Odoo | Thay cho |
|---|---|---|---|---|
| 1 | Giám đốc + Mua | Mỗi quý chốt giá với NCC chính | Thỏa thuận mua hàng (giá, thời hạn) | Hợp đồng giấy, Excel giá |
| 2 | Hệ thống / Mua | 16:30 sau khi lập kế hoạch sản xuất: NVL dưới mức tối thiểu hoặc không đủ cho lệnh sản xuất | Bổ sung hàng → đơn mua nháp theo giá thỏa thuận, gom theo NCC | Thủ kho gọi điện |
| 3 | Mua | Gửi đơn cho NCC (email/Zalo, PDF từ Odoo) | Xác nhận đơn mua; trên 20 triệu → chờ giám đốc duyệt | |
| 4 | Thủ kho + QC | Xe NCC đến: kiểm nhiệt độ hàng mát, hạn dùng, bao bì, đếm trứng vỡ | Phiếu QC tự tạo khi phiếu nhập sẵn sàng | Sổ kiểm hàng |
| 5 | Thủ kho | Nhận số đạt, ghi lô và hạn dùng in trên bao; hàng không đạt trả lại xe | Xác nhận phiếu nhập theo số thực nhận, không tạo đơn chờ; ghi chú lý do | Phiếu nhập kho |
| 6 | Hệ thống | Hàng tự vào đúng vị trí (kho mát / khô / bao bì) theo nhóm | Quy tắc cất hàng | |
| 7 | Kế toán | Hóa đơn NCC đến: Odoo đề xuất số lượng theo số đã nhận; lệch giá → không xác nhận | Hóa đơn NCC (đối chiếu đơn mua – phiếu nhập – hóa đơn) | Đối chiếu tay |
| 8 | Kế toán | NCC trứng: trả tiền mặt khi nhận; NCC khác: thanh toán theo hạn mỗi thứ Sáu | Thanh toán tiền mặt / ngân hàng | |
| 9 | Thủ kho | Phát hiện lỗi sau khi nhận (bơ hỏng) | Phiếu trả NCC; kế toán giấy báo có NCC | |

**Kiểm soát.** Chỉ mua theo giá thỏa thuận; duyệt đơn lớn; không nhận hàng mát không đạt nhiệt độ; chỉ trả tiền cho số đã nhận.

**Ngoại lệ.** NCC giao thiếu (nhận số thực, đơn còn lại tự đóng hoặc đặt lại); NCC giao trễ làm thiếu NVL ca đêm (quản đốc đổi thứ tự mẻ, kinh doanh báo khách); giá NCC tăng giữa quý (cập nhật thỏa thuận, giám đốc duyệt); hàng không đạt (không nhận, ghi lý do trên phiếu QC để đánh giá NCC).

**Báo cáo.** Người dùng: đơn mua chờ giao hôm nay, đơn chờ hóa đơn. Quản lý: giá trị mua theo NCC / tháng, biến động giá, tỷ lệ không đạt theo NCC, công nợ phải trả đến hạn.

**Không làm trên Odoo.** Đấu thầu, so sánh nhiều NCC mỗi lần (không phù hợp quy mô).

**Bài học eLearning Purchase.** Your First RFQ, Paying your First Vendor, Purchase Lead Times, Reordering Rules, Vendor Pricelists, Approvals & Warnings, Bill Control, Blanket Orders; Quality: Quality Checks for Incoming Shipments.

### 3.3. Sản xuất – QT3 Odoo cho quản đốc xưởng

**Nguyên tắc.** Trên sàn sản xuất, người dùng Odoo là **quản đốc** (và tổ trưởng ca đêm ghi sản lượng cuối ca). Thợ làm theo phiếu sản xuất in ra, không chạm máy tính. Odoo phục vụ 4 việc của quản đốc: lên kế hoạch mẻ, đảm bảo đủ nguyên liệu, ghi nhận kết quả, xem hiệu quả. Cách này cũng khớp giới hạn của bản Community: màn hình Shop Floor (cho thợ thao tác công đoạn) và báo cáo Production Analysis không có trong Community (đã kiểm: không có module mrp_workorder, không có model mrp.report).

**Bối cảnh.** 2 ca: ca đêm làm bánh mì tươi (giao sáng), ca ngày làm bánh ngọt, cookies, cấp đông, OEM. Nút thắt là lò nướng. Một mẻ bị giới hạn bởi cối trộn (khoảng 25 kg bột).

**Công việc của quản đốc trên Odoo trong một ngày.**

| # | Giờ | Ai | Việc | Màn hình Odoo (Community) | Thay cho |
|---|---|---|---|---|---|
| 1 | 16:00 | Quản đốc | Xem nhu cầu ngày mai | Tồn kho > Bổ sung hàng: tồn dự báo đã trừ đơn bán đã xác nhận (đã kiểm: FG02 tồn 40, dự báo -35) | Cộng tay từ sổ đơn |
| 2 | 16:10 | Quản đốc | Chốt số lượng, làm tròn theo mẻ (bội số trên quy tắc), bấm Đặt hàng | Bổ sung hàng → lệnh sản xuất; nhiều lệnh cùng sản phẩm thì chọn và Gộp (Merge) | Phiếu kế hoạch |
| 3 | 16:15 | Quản đốc | Xem cột Nguyên liệu: lệnh "Chờ" → báo Mua (QT2) hoặc dời mẻ | Danh sách lệnh sản xuất, lọc theo trạng thái nguyên liệu | Gọi thủ kho hỏi |
| 4 | 16:20 | Quản đốc | Xác nhận lệnh, in phiếu sản xuất (công thức, số lượng, NVL) cho thợ | Lệnh sản xuất > Xác nhận > In | Phiếu viết tay |
| 5 | 16:30 | Thủ kho | Cấp NVL cho cả ca ra Khu sản xuất | Phiếu cấp NVL (sản xuất 2 bước), lô giữ theo FEFO | Phiếu xuất kho |
| 6 | 22:00–05:00 | Thợ | Làm bánh theo phiếu | Không thao tác | |
| 7 | 05:00 | QC | Lấy mẫu mỗi lô: cảm quan, khối lượng, nhãn ngày, nhiệt độ lõi | Phiếu QC (OCA) tự tạo khi lệnh xác nhận (BH5); QC nhập kết quả | Sổ QC |
| 8 | 05:15 | Tổ trưởng / Quản đốc | Ghi sản lượng thực tế từ sổ ca | Lệnh sản xuất: nhập số lượng, lô (mã SP-ngày); hạn dùng tự tính | Sổ sản xuất |
| 9 | 05:15 | Tổ trưởng / Quản đốc | Ghi bánh lỗi | Nút Loại bỏ trên lệnh (thành phẩm lỗi ghi được khi lệnh đã xong; NVL hỏng ghi được trước) | Sổ hàng hủy |
| 10 | 05:20 | Quản đốc | Hoàn tất lệnh. Làm ít hơn kế hoạch: bánh tươi chọn "Đóng lệnh, không tạo lệnh bổ sung"; cookies, cấp đông có thể "Tạo lệnh bổ sung" | Hộp thoại khi làm thiếu (đã kiểm: có cả hai lựa chọn) | |
| 11 | 05:20 | Hệ thống | Trừ NVL theo định mức; ghi phụ phẩm vụn bánh; nhập thành phẩm vào vị trí theo nhiệt độ; ghi thời gian công đoạn bằng thời gian định mức; tính giá thành | Tự động | Ghi tay |
| 12 | 17:00 | Thủ kho | Đếm NVL dư ở Khu sản xuất; trả về kho hoặc điều chỉnh hao hụt | Điều chỉnh tồn vị trí Khu sản xuất | |
| 13 | Thứ Hai | Quản đốc | Xem tuần trước: sản lượng, bánh lỗi, tiêu hao so định mức, tải lò | Pivot / đồ thị trên Lệnh sản xuất, Lịch sử điều chuyển, Hiệu suất và Tải khu vực sản xuất | Excel |
| 14 | Cuối tháng | Quản đốc + Kế toán | Giá thành từng sản phẩm, đề xuất sửa định mức | Chi phí trên lệnh; tính lại giá vốn từ BoM | Excel |

**Cách dùng các tính năng MRP cho đúng quy mô.**

| Tính năng (bài học eLearning MRP) | Dùng thế nào ở Bảo Hân | Lý do |
|---|---|---|
| Bill of Materials Basics | BoM theo mẻ (ví dụ 100 ổ), định mức gram thực tế | Giá thành, trừ kho đúng |
| Work Center Basics, Work Center Parameters | 4–5 khu vực có chi phí/giờ và lịch 2 ca; công đoạn thời gian cố định | Odoo tính tải lò và chi phí theo định mức |
| MO & Work Order Basics | Công đoạn chỉ để lập kế hoạch và tính chi phí; quản đốc hoàn tất cả lệnh | Thợ không bấm giờ; Shop Floor không có ở Community |
| Manufacturing Planning | "Lên kế hoạch" lệnh để xem lò có quá tải không | Lò là nút thắt |
| Split and Merge MOs | Gộp lệnh cùng sản phẩm cùng ca | 1 lệnh / sản phẩm / ca |
| Replenishment Methods for Manufacturing | Quy tắc bổ sung thủ công cho hàng trữ; bánh tươi xem nhu cầu theo đơn qua Bổ sung hàng | Quản đốc quyết định cuối cùng |
| MTO Manufacturing | Chỉ cho sản phẩm OEM | OEM theo đơn, bao bì riêng |
| Manufacture in 2 Steps | Cấp NVL ra Khu sản xuất trước ca | Kho đóng cửa ban đêm |
| Manufacture with Lots | Lô thành phẩm theo ngày; lô NVL giữ theo FEFO lúc cấp | Truy xuất khi khiếu nại |
| Flexible Consumption | "Cho phép kèm cảnh báo" (Odoo có 3 mức: cho phép, cho phép kèm cảnh báo, chặn) | Tiêu hao lệch là bình thường, nhưng phải thấy |
| By-Products | Vụn bánh từ bánh mì cắt lát | Có thật, bán làm thức ăn chăn nuôi hoặc bột chiên |
| Scrap Orders | Bánh cháy, méo, rách bao bì | Đo tỷ lệ hư hỏng |
| Manufacturing Backorders | Bánh tươi: đóng lệnh; hàng trữ: tạo lệnh bổ sung | Bánh tươi không làm bù hôm sau |
| Production Costs, FIFO/AVCO/Standard | AVCO; chi phí = NVL thực tế + thời gian định mức × chi phí/giờ khu vực | Nguyên liệu giá biến động |
| Production Analysis, OEE | Bản Community: pivot trên Lệnh sản xuất và báo cáo Hiệu suất khu vực sản xuất | Production Analysis là của Enterprise |
| Shop Floor, MPS, Maintenance | Không dùng | Shop Floor, MPS chỉ có ở Enterprise; Maintenance để hướng phát triển |

**Định mức thực tế.** BoM theo mẻ, ví dụ bánh mì sandwich 400 g: 1 mẻ 100 ổ cần khoảng 23 kg bột, 1,5 kg đường, 0,45 kg muối, 0,3 kg men, 1,5 kg bơ, 100 túi, 5 thùng. Định mức hiện có trong DB cần chỉnh lại (bản cũ dùng 40 kg bột cho 100 ổ, quá cao).

**Giới hạn chấp nhận, ghi rõ trong báo cáo.** Thời gian công đoạn ghi bằng định mức, nên phần nhân công trong giá thành là giá thành định mức. Muốn đo thật cần máy tính bảng ở xưởng và bản Enterprise (Shop Floor), để ở hướng phát triển.

**Kiểm soát.** Lô thành phẩm truy được về lô NVL đã cấp; bánh lỗi phải có phiếu loại bỏ có lý do; tiêu hao lệch định mức hiện cảnh báo; NVL dư ở Khu sản xuất được đếm mỗi chiều.

**Ngoại lệ.** Thiếu NVL (dời mẻ, làm thiếu, kinh doanh báo khách); lò hỏng (dời lệnh sang ca ngày, ghi chú lệnh); mẻ hỏng (loại bỏ cả mẻ, làm lại nếu kịp giờ giao); làm dư (vào tồn, module cận hạn theo dõi); OEM (lệnh riêng theo đơn, lô riêng, bao bì của khách).

**Báo cáo cho quản đốc.** Lệnh ngày mai theo ca; NVL cần cấp; sản lượng theo sản phẩm / ngày (pivot lệnh sản xuất); tỷ lệ bánh lỗi (phiếu loại bỏ / sản lượng); tiêu hao NVL so định mức; tải và hiệu suất khu vực; giá thành mẻ.

### 3.4. Kho – QT4 Lô, hạn dùng, cận hạn, kiểm kê

**Bối cảnh.** Kho nhỏ, 1 thủ kho chính + 1 phụ ca sáng. Rủi ro lớn nhất: bánh và NVL mát hết hạn, nhầm lô khi giao, hao hụt khu sản xuất.

**Vị trí.** Kho khô, Kho mát, Tủ đông NVL, Kho bao bì, Khu sản xuất, TP nhiệt độ thường, TP lạnh, TP đông, Khu cách ly (hàng trả về, hàng chờ hủy).

**Luồng.**

| # | Nhịp | Ai | Việc | Trên Odoo |
|---|---|---|---|---|
| 1 | Hằng ngày 23:00 | Hệ thống | Tính % hạn còn lại mọi lô (ở kho và đang ở khách) | Module cận hạn |
| 2 | Sáng | Thủ kho | Xem việc cận hạn: bánh mì đang ở quán còn ≤ 40% → in danh sách thu hồi cho tài xế chuyến sau | Việc cận hạn, lọc "đang ở điểm bán" |
| 3 | Sáng | Kinh doanh | Cookies, cấp đông còn ≤ 30% → chào bếp ăn, trường học giá xả | Giá đề xuất trên việc cận hạn |
| 4 | Khi tài xế về | Thủ kho | Nhận hàng thu hồi vào Khu cách ly | Phiếu trả hàng |
| 5 | Hằng tuần | Giám đốc + Thủ kho | Duyệt hủy hàng trong Khu cách ly (hoặc làm vụn bánh bán thức ăn chăn nuôi) | Nút Hủy lô → phiếu hủy, ghi tổn thất |
| 6 | Hằng ngày 17:00 | Thủ kho | Đếm nhanh thành phẩm | Điều chỉnh tồn vị trí TP |
| 7 | Thứ Bảy | Thủ kho | Kiểm kê kho mát, tủ đông theo lô | Điều chỉnh tồn; chênh lệch lớn → giám đốc xem trước khi áp dụng |
| 8 | Cuối tháng | Thủ kho + Kế toán | Kiểm kê toàn bộ | Điều chỉnh tồn; báo cáo chênh lệch |

**Quy tắc cận hạn theo nhóm (thay cho quy tắc chung).**

| Nhóm | Hạn dùng | Theo dõi | Giảm giá | Thu hồi / cách ly |
|---|---|---|---|---|
| Bánh mì tươi | 5 ngày | — | — | còn ≤ 40% (2 ngày) |
| Bánh lạnh | 3 ngày | — | — | còn ≤ 34% (1 ngày) |
| Bánh ngọt | 15–30 ngày | ≤ 50% | ≤ 30% (giảm 20%) | ≤ 15% |
| Cookies, cấp đông | 180 ngày | ≤ 50% | ≤ 30% (giảm 20%) | ≤ 15% |
| NVL mát | 10–120 ngày | ≤ 50% | — | ≤ 15% (không dùng sản xuất) |

**Kiểm soát.** FEFO tự động; lô quá ngày rút khỏi kệ không được giữ cho đơn; chênh lệch kiểm kê phải có người duyệt; hàng trả về không vào kho bán trước khi kiểm.

**Báo cáo.** Tồn theo vị trí / lô / hạn dùng; việc cận hạn và tổn thất theo nhóm / tháng; chênh lệch kiểm kê; tỷ lệ hàng thu hồi theo khách.

**Không làm trên Odoo.** Quét mã vạch (Barcode chỉ có ở Enterprise; nhãn lô in sẵn, nhập tay số lô ít); theo dõi nhiệt độ tủ tự động (cần cảm biến, để ở hướng phát triển).

**Bài học eLearning Inventory.** Warehouses & Locations, Putaway Rules, Lots & Serial Numbers, Working with Perishable Products, Expiration Dates, FEFO, Inventory Adjustments & Cycle Counts, Batch Transfers, Custom Returns, Scrap.

### 3.5. Kế toán – QT5 Công nợ, thu chi, giá vốn

**Bối cảnh.** 1 kế toán. Doanh nghiệp nhỏ ở Việt Nam thường vẫn khai thuế bằng phần mềm kế toán riêng (ví dụ MISA) và HTKK. Odoo làm phần quản trị: công nợ, thu chi, giá vốn, giá trị tồn; hóa đơn điện tử qua nhà cung cấp.

**Luồng.**

| # | Nhịp | Việc | Trên Odoo |
|---|---|---|---|
| 1 | Cuối ngày | Tạo hóa đơn cho mọi đơn đã giao trong ngày, phát hành hóa đơn điện tử | Tạo hóa đơn hàng loạt; module l10n_vn_edi_viettel (cần tài khoản Viettel S-Invoice) |
| 2 | Cuối ngày | Ghi tiền mặt tài xế nộp, đối chiếu với phiếu giao | Thanh toán nhật ký tiền mặt |
| 3 | Liên tục | Chuyển khoản của khách tự ghi nhận | Webhook ngân hàng (module bh_api) |
| 4 | Khi có | Hàng trả, hàng thiếu → giấy báo có | Credit note |
| 5 | Khi hóa đơn NCC đến | Đối chiếu 3 bên, xác nhận | Hóa đơn NCC |
| 6 | Thứ Sáu | Trả NCC đến hạn | Thanh toán NCC theo hạn |
| 7 | Cuối tháng | Sao kê công nợ khách trả sau; tuổi nợ; nhắc nợ | Sao kê, tuổi nợ (OCA), BH3 |
| 8 | Cuối tháng | Giá trị tồn, giá vốn, sổ cái, cân đối phát sinh để đối chiếu với phần mềm kế toán thuế | Báo cáo OCA; xuất Excel |

**Kiến thức từ video eLearning Accounting (thư mục Odoo_HocTap/videos).**
- Trạng thái hóa đơn: chưa trả → trả một phần → đang thanh toán (đã ghi nhận, chưa đối soát ngân hàng) → đã trả (sau đối soát). Tài khoản tiền đang chuyển (outstanding receipts / payments) giữ số tiền trong khoảng giữa ghi nhận và đối soát.
- Điều khoản thanh toán: hạn trả, chia nhiều đợt, chiết khấu trả sớm. Siêu thị, bếp ăn dùng "30 ngày"; có thể đề xuất "2/7 net 30" (giảm 2% nếu trả trong 7 ngày) để thu tiền nhanh hơn.
- Ở Bảo Hân, webhook ngân hàng ghi nhận thanh toán ngay khi tiền về, nên đối soát là tự động; giao dịch không khớp mới cần kế toán xử lý tay.

**Kiểm soát.** Hóa đơn theo số thực giao; tiền mặt đối chiếu hằng ngày; chặn bán khi nợ quá hạn; chỉ trả NCC khi đã đối chiếu 3 bên.

**Ngoại lệ.** Khách trả thiếu / thừa (hóa đơn trả một phần, khoản trả trước cấn trừ sau); chuyển khoản không rõ nội dung; tài xế nộp thiếu tiền (chênh lệch ghi nợ tài xế); NCC tăng giá không báo (hóa đơn lệch, không xác nhận).

**Báo cáo.** Tuổi nợ phải thu / phải trả, sao kê từng khách, dòng tiền thu theo ngày, doanh thu – giá vốn – lãi gộp theo sản phẩm, giá trị tồn.

**Không làm trên Odoo.** Kê khai thuế, báo cáo tài chính theo mẫu nộp cơ quan thuế (dùng phần mềm kế toán riêng; Odoo xuất số liệu để đối chiếu).

**Bài học eLearning Accounting.** Customer invoice from SO, Issue a credit note, Register a vendor bill, Payment terms, Payments and outstanding accounts, Customer payment follow-up, Taxes and VAT, Inventory valuation, Financial reports.

## 4. Điểm tích hợp

| Sự kiện | Từ | Đến | Odoo tự làm |
|---|---|---|---|
| Đơn bán xác nhận | Bán hàng | Sản xuất, Kho | Tồn dự báo giảm → xuất hiện trong Bổ sung hàng; đơn OEM sinh lệnh riêng |
| Lệnh sản xuất thiếu NVL | Sản xuất | Mua hàng | Bổ sung hàng đề xuất đơn mua theo giá thỏa thuận |
| Xe NCC đến | Mua hàng | Chất lượng | Tạo phiếu QC khi phiếu nhập sẵn sàng |
| Phiếu nhập xác nhận | Kho | Mua hàng, Kế toán | Số đã nhận cập nhật đơn mua; hóa đơn NCC chỉ theo số này |
| Lệnh sản xuất xác nhận | Sản xuất | Kho, Chất lượng | Phiếu cấp NVL; phiếu QC thành phẩm |
| Lệnh hoàn tất | Sản xuất | Kho, Kế toán | Lô thành phẩm, hạn dùng; giá vốn bình quân cập nhật |
| Phiếu giao xác nhận | Kho | Bán hàng, Kế toán | Số đã giao trên đơn → hóa đơn |
| Hóa đơn bán | Kế toán | Hóa đơn điện tử | Phát hành qua nhà cung cấp |
| Tiền về | Ngân hàng | Kế toán | Webhook ghi nhận thanh toán |
| Lô chạm ngưỡng | Kho | Bán hàng, Kế toán | Việc cận hạn; tổn thất khi hủy |
| Khách nợ quá hạn | Kế toán | Bán hàng | Chặn xác nhận đơn |

## 5. Thay đổi cấu hình Odoo (đã áp dụng 18/11, trừ ghi chú)

| # | Thay đổi | Lý do |
|---|---|---|
| 1 | Nhận hàng 1 bước; phiếu QC tạo khi phiếu nhập sẵn sàng (sửa BH1) | Kiểm tại cửa trước khi nhận |
| 2 | Sản xuất 2 bước (cấp NVL rồi sản xuất); thêm vị trí Khu sản xuất | Thủ kho cấp cho cả ca |
| 3 | Bỏ quy tắc min/max cho bánh tươi; giữ cho cookies, cấp đông; route MTO chỉ cho FG05 OEM | Kế hoạch theo tổng đơn ngày mai |
| 4 | Sửa định mức BoM theo khối lượng thực tế | Giá thành đúng |
| 5 | Cài stock_picking_batch; đợt soạn hàng theo tuyến | Giao theo tuyến |
| 6 | Chính sách hóa đơn theo số đã giao; tạo hóa đơn hàng loạt | Hóa đơn đúng thực giao |
| 7 | Sửa BH2: chặn xác nhận đơn khi khách nợ quá hạn / vượt hạn mức, mở bằng nhãn "Đã duyệt công nợ" | Kiểm soát rủi ro tiền thật |
| 8 | BH5: tạo phiếu QC khi lệnh sản xuất được xác nhận | QC lấy mẫu mỗi lô |
| 9 | Quy tắc cận hạn theo nhóm (bảng 3.4) | Bánh tươi khác bánh khô |
| 10 | Cài purchase_requisition; thỏa thuận giá theo quý với NCC chính; duyệt đơn mua trên 20 triệu | Mua theo giá hợp đồng |
| 11 | Nhật ký tiền mặt cho tài xế nộp | Thu tiền mặt |
| 12 | Cài l10n_vn_edi_viettel ở mức cấu hình (đã cài; chưa có tài khoản Viettel nên chưa phát hành thật) | Hóa đơn điện tử |
| 13 | Tạo lại dữ liệu demo theo 1 tuần vận hành (thay kịch bản hiện tại) | Dữ liệu sát thực tế |
| 14 | Vẽ lại 5 BPMN theo bản này | Đồng bộ tài liệu |

Đã dựng lại DB từ đầu bằng scripts/rebuild_all.sh; dữ liệu là tuần đầu go-live 14–18/11 (scripts/README.md). Riêng mục 3 (min/max 0 cho bánh tươi): Odoo tự xóa quy tắc 0/0 sau khi đặt, nên nhu cầu bánh tươi được đề xuất tự động khi quản đốc mở màn hình Bổ sung hàng – đúng như thiết kế.

## 6. Đánh giá độ khó, tầm quan trọng và phân công

### 6.1. Chấm điểm từng quy trình (1 thấp – 5 cao)

| Tiêu chí | QT1 Bán hàng | QT2 Mua hàng | QT3 Sản xuất | QT4 Kho, cận hạn | QT5 Kế toán |
|---|---|---|---|---|---|
| Tầm quan trọng với doanh nghiệp | 5 (80% doanh thu, dòng tiền) | 4 | 5 (lõi của doanh nghiệp sản xuất) | 4 (hao hụt, an toàn thực phẩm) | 4 |
| Tầm quan trọng với môn học | 4 | 4 | 5 (yêu cầu cốt lõi: doanh nghiệp sản xuất) | 4 (gắn module tự viết) | 4 (HD yêu cầu làm rõ luồng tài chính) |
| Độ phức tạp cấu hình Odoo | 4: bảng giá, chặn công nợ, soạn theo tuyến, trả hàng, hóa đơn hàng loạt | 3: thỏa thuận giá, duyệt, QC tại cửa | 4: BoM, khu vực, 2 bước, lô, phụ phẩm, phế phẩm, bổ sung hàng | 4: vị trí, FEFO, kiểm kê, module tự viết | 3: phần lớn là kết quả của 4 quy trình kia |
| Số ngoại lệ phải xử lý | 5 | 3 | 3 | 3 | 3 |
| Số điểm tích hợp | 5: Kho, Sản xuất, Kế toán, API, Website, hóa đơn điện tử | 3 | 4: Bán, Mua, Kho, QC, Kế toán | 3 | 5: nhận từ mọi quy trình |
| Kiến thức nền cần có | Trung bình | Trung bình | Cao: định mức, giá thành, lô | Trung bình (đọc được code module) | Cao: bút toán, giá vốn, thuế |
| **Tổng** | **27** | **20** | **25** | **22** | **23** |

Kết luận:
- Sau khi thiết kế lại cho sát thực tế, **Sản xuất không còn khó nhất**: đã bỏ bấm giờ công đoạn và gộp lệnh theo ca, nên thao tác còn ít. Cái khó còn lại là hiểu định mức, lô, giá thành.
- **Bán hàng nặng nhất** vì nhiều nhóm khách, nhiều ngoại lệ và chạm vào mọi phân hệ khác.
- **Sản xuất quan trọng nhất về mặt chấm điểm**: môn yêu cầu doanh nghiệp sản xuất, nên phần này phải được làm chắc và người phụ trách phải thuyết trình tốt nhất.
- **Kế toán khó về kiến thức** nhưng ít thao tác; nên tách: phải thu đi cùng Bán hàng, phải trả đi cùng Mua hàng, vì người làm quy trình hiểu rõ chứng từ của quy trình đó.

### 6.2. Phân công (cân theo điểm, mỗi người chính 1 quy trình không trùng)

| Vai trò | Quy trình chính (quay video) | Phần phụ | Tổng điểm | Hợp với người |
|---|---|---|---|---|
| A | QT1 Bán hàng (27) | QT5 phần phải thu, đối soát ngân hàng (≈12); Module API; Website | ≈ 39 | Giao tiếp tốt, chịu được nhiều tình huống, đọc được code API |
| B | QT3 Sản xuất (25) | QT4 phần cận hạn (module bh_near_expiry) (≈11) | ≈ 36 | Tư duy hệ thống, tỉ mỉ với số liệu định mức, thuyết trình chắc vì đây là phần thầy hỏi nhiều |
| C | QT2 Mua hàng (20) | QT4 phần vị trí, kiểm kê (≈11); QT5 phần phải trả, giá vốn, báo cáo tài chính (≈11); Automation Rules | ≈ 42 | Cẩn thận, có nền kế toán hoặc chịu học bút toán |

Ghi chú:
- C có tổng điểm cao nhất nhưng các phần phụ đều là thao tác ngắn, lặp lại (kiểm kê, thanh toán NCC, chạy báo cáo); A và B có phần phụ cần đọc code.
- Nhóm chốt lại (19/11), khác đề xuất A/B/C ở trên: Lê Thị Thanh Tiền – QT1 Bán hàng, bh_api (REST), BPMN, gom báo cáo; Phạm Tuấn Hải – QT3 Sản xuất + QT4 Kho (cùng dữ liệu kho), JSON-2, dữ liệu demo, bh_near_expiry, Telegram; Đoàn Thị Thùy Trang – QT2 Mua hàng + QT5 Công nợ, XML-RPC, Automation QC, Google Sheets, website. Đóng góp 34/33/33%. Chi tiết: chương 9 báo cáo.
- Phần làm chung: Chương 1–2, mô hình triển khai, bảo mật, kết luận, slide; mỗi người một API khác nhau (A: Module API bh_api; B: JSON-2 API đọc lệnh sản xuất, lô; C: XML-RPC tạo đơn mua).

## 7. Giả định cần kiểm chứng khi phỏng vấn

Bổ sung vào Phụ lục A (câu 23–32): giờ chốt đơn; tỷ lệ đơn cố định; số tuyến xe và điểm giao; chính sách thu hồi bánh ế; tỷ lệ khách trả tiền mặt; ca sản xuất và người ghi sổ sản xuất; dung lượng cối trộn và lò; có máy dò kim loại không; phần mềm kế toán và hóa đơn điện tử đang dùng; hợp đồng giá với NCC.
