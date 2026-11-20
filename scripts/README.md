# Script dữ liệu và kịch bản – Bảo Hân (bản 2: vận hành thực tế)

## Dựng lại toàn bộ DB `baohan` (khoảng 5 phút)

Trong Git Bash, thư mục `odoo_local`:

```bash
bash ../scripts/rebuild_all.sh
```

Script xóa DB `baohan` rồi chạy lần lượt: cài module → áp theme → `seed_odoo.py` → `automation_rules.py` → `demo_week.py`. Sao lưu trước nếu cần (`docker compose exec -T db pg_dump -U odoo -Fc baohan > file.dump`).

| Script | Làm gì |
|---|---|
| seed_data.py | Dữ liệu nền (một nguồn duy nhất): sản phẩm, định mức theo khối lượng thực tế, khách theo tuyến, đơn cố định, hợp đồng giá, quy tắc cận hạn theo nhóm |
| seed_odoo.py | Nạp cấu hình và dữ liệu nền; chạy lại không trùng |
| automation_rules.py | 6 quy tắc tự động BH1, BH2a, BH2b, BH3, BH4 (tắt), BH5 |
| demo_week.py | Kịch bản tuần đầu go-live; phần đã chạy đánh dấu `bh_week.<phần>` |
| api_demo_calls.py | Gọi Module API và webhook ngân hàng qua HTTP |
| export_import_files.py | Xuất CSV/XLSX cho tiêu chí Import |

## Kịch bản tuần đầu go-live (14–18/11/2026)

Vì sao là "tuần go-live": Odoo kiểm ngày rút khỏi kệ của lô theo giờ thật, nên không thể giả lập lùi nhiều tuần với bánh hạn 3–5 ngày. Kịch bản bám đúng cách một dự án ERP thật bắt đầu: chuyển số dư đầu kỳ rồi vận hành.

| Thời điểm | Việc | Chứng từ |
|---|---|---|
| Thứ Bảy 14/11 15:00 | Kiểm kê chốt tồn lúc go-live (NVL theo lô DK-…, thành phẩm có lô cũ) | Điều chỉnh tồn |
| Thứ Bảy 14/11 | Chuyển công nợ tháng 10 từ sổ cũ (đối ứng TK 4211) | INV/2026/00001–00003 (KH03 quá hạn), hóa đơn NCC01, NCC03 |
| Thứ Bảy 16:00 | Nhận đơn cho thứ Hai. KH03 bị BH2b chặn vì nợ quá hạn → giám đốc gắn nhãn "Đã duyệt công nợ" → xác nhận | S00001–S00007 |
| Thứ Bảy 16:00–16:30 | Quản đốc: Bổ sung hàng → lệnh sản xuất; BH5 tạo phiếu QC; thủ kho cấp NVL ra Khu sản xuất; Mua: bổ sung NVL theo min/max → đơn mua trứng, sữa – phô mai, xúc xích | WH/MO/00001–00005, P00001–P00003 |
| Thứ Hai 05:00 | QC kiểm mẫu, quản đốc ghi sản lượng, lô theo ngày | QC-000001–000005 đạt |
| Thứ Hai 05:30–10:30 | Soạn theo tuyến (đợt), giao, tài xế về | BATCH/OUT/00001–00003 |
| Thứ Hai 07:00 | Xe NCC04 đến: QC không đạt (trứng vỡ), nhận thiếu 60 quả, không tạo đơn chờ | QC-000009 không đạt, BH/IN/00003; NCC03, NCC05 nhận đủ (BH/IN/00001–00002) |
| Thứ Hai 09:00 | KH03 chuyển 50% nợ tháng 10 | Thanh toán ngân hàng |
| Thứ Hai 17:00 | Hóa đơn hàng loạt theo số đã giao; quán trả tiền mặt, KH02 chuyển khoản. Hóa đơn NCC theo số đã nhận; NCC04 trứng trả tiền mặt | INV/2026/00004–00010; hóa đơn NCC P00001–P00003 |
| Thứ Hai tối | Đơn thứ Ba; ca đêm: mẻ bánh mì sandwich thiếu 8 ổ → đóng lệnh không làm bù; 5 gói Hoppi rách bao bì → loại bỏ | WH/MO/00006–00008, SP/00001 |
| Thứ Ba | KH07 đóng cửa → hủy giao; điểm cuối tuyến 3 hết bánh → hủy, báo khách; KH04 nhận thiếu → hóa đơn theo số thực | S00011, S00012 hủy; INV/2026/00011–00013 |
| Thứ Ba 17:00 | Đếm nhanh thành phẩm: bánh tiệc trà thiếu 2 khay | Điều chỉnh tồn |
| Thứ Ba 16:40 | NV mua đặt bột tuần (24,6 triệu) → chờ giám đốc duyệt | P00004 "Chờ duyệt" |
| Thứ Tư sáng | Giao 3 tuyến; KH01 trả 6 ổ bánh mì không bán hết → Khu cách ly, giấy báo có | BATCH/OUT/00007–00009, BH/IN/00004, RINV/2026/00001 |
| Thứ Tư chiều (đang diễn ra) | Đơn thứ Năm đã nhận; KH03 vẫn bị chặn (chờ giám đốc); đơn trường học còn là báo giá; đơn OEM 300 hộp bông lan sinh lệnh sản xuất riêng (MTO); chưa lập kế hoạch ca đêm, chưa lập hóa đơn trong ngày | S00018–S00025, WH/MO/00011 |
| Thứ Tư | Thủ kho cách ly lô hết hạn ở kho vào BH/Khu cách ly (BH/INT/00001). Module cận hạn: 10 việc (bánh mì lô thứ Bảy đang ở KH01, KH04 cần thu hồi; bánh lạnh hết hạn ở kho và ở KH08; cookies giảm giá; trứng, sữa ưu tiên dùng) | bh.expiry.log |
| Thứ Tư | App của KH02 đặt hàng qua API; ngân hàng báo KH04 chuyển khoản qua webhook | S00026–S00027 (nháp), INV/2026/00007 đã trả |

Ghi chú: ngày giờ trên chứng từ được đặt theo lịch giả lập; một số trường Odoo tự ghi (ngày tạo, nhật ký) vẫn là ngày chạy script.
