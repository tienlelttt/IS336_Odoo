# Dữ liệu nền (master data) – Bảo Hân

Nguồn gốc duy nhất: `scripts/seed_data.py`. Thông tin công ty là thông tin công khai; nhân sự, khách hàng (KH mẫu), nhà cung cấp (NCC mẫu), giá, định mức là **giả định** phục vụ học tập.

## File trong thư mục này (dùng cho tiêu chí Import/Export)

| File | Model Odoo | Nội dung |
|---|---|---|
| master_data_bao_han.xlsx | nhiều sheet | Gộp 4 file CSV dưới, mỗi sheet một loại |
| san_pham_thanh_pham.csv | product.template | 12 thành phẩm, theo lô, có hạn dùng |
| nguyen_vat_lieu.csv | product.template | 23 nguyên vật liệu và bao bì, kèm nhà cung cấp, giá mua, thời gian giao |
| khach_hang.csv | res.partner | 8 khách mẫu, bảng giá, điều khoản thanh toán, hạn mức nợ, tuyến giao, nhãn trả tiền mặt |
| nha_cung_cap.csv | res.partner | 6 nhà cung cấp mẫu |

Cột là tên kỹ thuật của trường nên Odoo tự khớp. Đã chạy thử import (dry-run) cả 4 file trên DB `baohan`: không lỗi.
Cách import trên giao diện: vào danh sách tương ứng > biểu tượng bánh răng > Nhập bản ghi > tải file > Kiểm tra > Nhập.
Lưu ý: DB `baohan` đã có sẵn dữ liệu này, import lần nữa sẽ tạo bản trùng. Để demo import, xóa bớt vài dòng trong Odoo trước hoặc dùng DB mới.

## Nạp lại toàn bộ dữ liệu nền

```bash
cd odoo_local
cat ../scripts/seed_data.py ../scripts/seed_odoo.py | MSYS_NO_PATHCONV=1 docker compose run --rm -T odoo -- shell -d baohan --no-http --addons-path=/usr/lib/python3/dist-packages/odoo/addons,/mnt/extra-addons,/mnt/oca/manufacture,/mnt/oca/account-financial-reporting,/mnt/oca/server-ux,/mnt/oca/reporting-engine,/mnt/oca/stock-logistics-barcode
```

Chạy lại nhiều lần không tạo trùng.

## Tài khoản thử nghiệm (CHỈ dùng cho Odoo local)

- Quản trị: `admin` / `admin` (mặc định khi tạo DB bằng dòng lệnh). Đổi ngay nếu đưa lên máy chủ thật.
- 8 người dùng nghiệp vụ, mật khẩu chung `BaoHan#2026`:

| Login | Vai trò | Quyền chính |
|---|---|---|
| giamdoc@baohan.local | Giám đốc | Quản lý Bán, Mua, Kho, Sản xuất, Kế toán, QC |
| kinhdoanh1@baohan.local | NV kinh doanh | Bán hàng: chỉ chứng từ của mình |
| kinhdoanh2@baohan.local | Trưởng nhóm KD | Bán hàng: tất cả chứng từ |
| muahang@baohan.local | NV mua hàng | Mua hàng, Kho (người dùng) |
| quandoc@baohan.local | Quản đốc | Sản xuất (quản lý), Kho (người dùng) |
| qc@baohan.local | QC | Kiểm soát chất lượng (người dùng), Kho |
| thukho@baohan.local | Thủ kho | Kho (người dùng) |
| ketoan@baohan.local | Kế toán | Kế toán (quản lý), xem Bán và Mua |

## Đã cấu hình bởi script

Công ty (MST, địa chỉ, logo chữ tự tạo), hệ thống tài khoản Việt Nam, tiền VND, tiếng Việt + tiếng Anh, mẫu chứng từ khung "Boxed" màu caramel, máy chủ mail Gmail (đang tắt, chờ điền App Password), avatar admin, kho "Xưởng Hiệp Bình Chánh" nhận hàng 2 bước và giao hàng 2 bước, 7 vị trí kho con, quy tắc cất hàng theo nhóm sản phẩm, xuất FEFO, 5 công đoạn sản xuất (work center), 12 BoM có công đoạn và phụ phẩm, quy tắc tái đặt hàng cho NVL và thành phẩm, 3 bảng giá, 3 phiếu kiểm tra chất lượng (OCA), website "Bảo Hân Bakery".
