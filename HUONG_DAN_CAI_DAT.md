# Hướng dẫn cài đặt và làm lại toàn bộ đồ án (Nhóm 06 – Bảo Hân)

Tài liệu này giúp một thành viên bất kỳ, trên máy Windows mới, dựng lại hệ thống y hệt và hiểu từng bước đã làm gì. Đọc theo thứ tự.

## Phần 1. Cài đặt nhanh (khoảng 30 phút)

### 1.1. Cài phần mềm

| Phần mềm | Dùng để | Tải |
|---|---|---|
| Docker Desktop | Chạy Odoo và PostgreSQL trong container | docker.com |
| Git for Windows (kèm Git Bash) | Chạy lệnh, tải module OCA | git-scm.com |
| Python 3.12+ | Chạy script xuất file, gọi API, dựng báo cáo | python.org |
| Camunda Modeler (desktop) | Mở, sửa, xuất ảnh BPMN | camunda.com/download/modeler |

Sau khi cài Python: `pip install python-docx openpyxl requests pillow playwright`.

### 1.2. Lấy thư mục đồ án

Chép nguyên thư mục `DoAn_HoanChinh` (kèm file `GIới-thiệu-đề-tài.docx` ở thư mục cha – mẫu định dạng báo cáo). Cấu trúc chính:

| Thư mục | Nội dung |
|---|---|
| odoo_local/ | docker-compose.yml, addons/ (3 module tự viết), oca/ (module cộng đồng) |
| scripts/ | Dữ liệu nền, cấu hình, kịch bản tuần go-live, gọi API, dựng lại |
| bpmn/ | 5 quy trình (.bpmn, .png) |
| baocao/ | Nội dung báo cáo (.md) và ảnh chụp màn hình |
| data/ | File import CSV/XLSX |
| integrations/ | Apps Script Google Sheets, hướng dẫn Telegram |
| tools/ | Dựng báo cáo, sinh BPMN, chụp ảnh |

### 1.3. Tải module OCA (nếu thư mục oca/ trống)

Trong Git Bash tại `odoo_local/oca`:

```
for r in manufacture account-financial-reporting server-ux reporting-engine stock-logistics-barcode; do git clone --depth 1 -b 19.0 https://github.com/OCA/$r.git $r; done
```

### 1.4. Dựng toàn bộ hệ thống bằng một lệnh

Mở Docker Desktop, chờ xanh. Trong Git Bash tại `odoo_local`:

```
docker compose up -d db
bash ../scripts/rebuild_all.sh
```

Lần đầu tải image khoảng 1 GB. Script xóa DB `baohan` nếu có, rồi: cài 19 module → áp theme → dữ liệu nền → quy tắc tự động → tuần go-live → bật Odoo. Khoảng 5 phút.

### 1.5. Đăng nhập

http://localhost:8069 – `admin` / `admin` (chỉ máy local). Các tài khoản vai trò (mật khẩu `BaoHan#2026`): xem `data/README.md`.

### 1.6. Lệnh hằng ngày

| Việc | Lệnh (Git Bash, thư mục odoo_local) |
|---|---|
| Bật | `docker compose up -d` |
| Tắt | `docker compose stop` |
| Xem log lỗi | `docker compose logs odoo --tail 100` |
| Sao lưu | `docker compose exec -T db pg_dump -U odoo -Fc baohan > ../backups/baohan_$(date +%Y%m%d).dump` |
| Khôi phục | `docker compose exec -T db createdb -U odoo baohan2` rồi `docker compose exec -T db pg_restore -U odoo -d baohan2 < file.dump` |
| Gọi API demo | `BH_API_TOKEN=<token> python ../scripts/api_demo_calls.py` (token: Thông số hệ thống `bh_demo.api_token_kh02`) |
| Dựng lại báo cáo | `python ../tools/md2docx.py "../Report - Nhóm 06.docx" ../baocao/00_bia.md ../baocao/00_mo_dau.md ../baocao/chuong1.md ... ` (xem mục 4.3) |

Lỗi thường gặp: Docker chưa bật (`failed to connect to the docker API`) → mở Docker Desktop; cổng 8069 bận → tắt Odoo khác đang chạy; chạy lệnh từ Git Bash phải có `MSYS_NO_PATHCONV=1` trước `docker compose run` (script đã có sẵn).

## Phần 2. Hiểu từng bước đã làm (để tự làm lại bằng tay khi quay video)

### 2.1. Cấu hình chung (Thiết lập)

1. Thiết lập > Công ty: tên, MST, địa chỉ, logo; Kế toán > Cấu hình > Cài đặt: gói hệ thống tài khoản Việt Nam, tiền VND.
2. Thiết lập > Ngôn ngữ: kích hoạt Tiếng Việt; avatar > Tùy chọn: chọn ngôn ngữ.
3. Thiết lập > Người dùng: tạo 8 người dùng; tab Quyền truy cập chọn mức cho từng app (mục 3.4 báo cáo).
4. Avatar tài khoản admin: mở hồ sơ, đổi ảnh.
5. Thiết lập > Kỹ thuật > Máy chủ gửi thư: smtp.gmail.com, 587, STARTTLS, email, mật khẩu ứng dụng Gmail → Kiểm tra kết nối.
6. Thiết lập > Công ty > Cấu hình bố cục chứng từ: Boxed, màu, logo, chân trang.
7. Tồn kho > Cấu hình > Cài đặt: bật Vị trí lưu trữ, Lô & số sê-ri, Ngày hết hạn, Tuyến nhiều bước; Sản xuất: bật Công đoạn, Phụ phẩm; Bán hàng: Bảng giá; Kế toán: Hạn mức nợ; Mua hàng: Duyệt đơn mua 2 cấp (20.000.000).

### 2.2. Kho

1. Tồn kho > Cấu hình > Kho: nhận hàng 1 bước, giao hàng 1 bước, sản xuất 2 bước.
2. Vị trí: tạo Kho khô, Kho mát, Kho bao bì, TP nhiệt độ thường/lạnh/đông dưới BH/Tồn kho; Khu cách ly dưới BH (ngoài Tồn kho).
3. Nhóm sản phẩm: chiến lược xuất FEFO; phương pháp giá vốn bình quân; định giá tự động; TK tồn kho thành phẩm 155.
4. Quy tắc cất hàng: nhóm → vị trí.

### 2.3. Dữ liệu nền

Cách nhanh: import file trong `data/` (danh sách → bánh răng → Nhập bản ghi). Cách tay để quay video: tạo 1 sản phẩm theo lô có hạn dùng, 1 BoM có công đoạn và phụ phẩm, 1 khách có bảng giá và hạn mức nợ, 1 hợp đồng giá NCC.

### 2.4. Quy trình mẫu để quay video (mỗi bạn 1 quy trình)

| Quy trình | Các bước thao tác trên Odoo |
|---|---|
| QT1 Bán hàng | Tạo đơn cho KH01 → xác nhận → tạo đợt soạn hàng tuyến 1 → xác nhận phiếu giao (sửa số giao thiếu 1) → tạo hóa đơn → đăng ký thanh toán tiền mặt. Thử KH03: xác nhận bị chặn → đăng nhập giamdoc gắn nhãn duyệt → xác nhận được |
| QT2 Mua hàng | Tồn kho > Bổ sung hàng → Đặt hàng NVL → mở đơn mua → xác nhận (đơn trên 20 triệu: đăng nhập giamdoc phê duyệt) → mở phiếu QC → nhập kết quả → phiếu nhập: nhập lô, hạn dùng, số nhận → xác nhận → tạo hóa đơn NCC → xác nhận → thanh toán |
| QT3 Sản xuất | Đăng nhập quandoc → Bổ sung hàng → Đặt hàng thành phẩm → mở lệnh → xác nhận, in phiếu → thủ kho xác nhận phiếu cấp NVL → QC nhập phiếu kiểm mẫu → nhập số lượng thực tế, lô → Hoàn tất (làm thiếu: đóng lệnh) → Loại bỏ 1 sản phẩm lỗi |
| QT4 Kho | Tồn kho > Cận hạn > Việc cần xử lý → lọc "Đang ở điểm bán" → nhóm theo điểm bán; lô hết hạn ở kho → chuyển Khu cách ly → nút Hủy lô; Điều chỉnh tồn: đếm kho mát, nhập số đếm → áp dụng |
| QT5 Kế toán | Hóa đơn → lọc quá hạn → xem việc nhắc nợ; chạy `api_demo_calls.py` cho một hóa đơn → xem Giao dịch ngân hàng; Báo cáo tuổi nợ (OCA) |

### 2.5. Quy tắc tự động

Bật chế độ nhà phát triển (Thiết lập > Kích hoạt chế độ nhà phát triển) → Thiết lập > Kỹ thuật > Tự động hóa > Quy tắc tự động hóa. Mở BH2b để giải thích: mô hình Đơn bán, kích hoạt "Trạng thái được đặt thành Đơn bán", hành động "Thực thi code".

### 2.6. Module tự viết

Mã nguồn ở `odoo_local/addons`. Cài/cập nhật một module: `MSYS_NO_PATHCONV=1 docker compose run --rm -T odoo -- -d baohan -u bh_near_expiry --stop-after-init`. Chạy test: thêm `--test-tags /bh_near_expiry` (DB thử, không phải baohan).

### 2.7. Website

Website > Chỉnh sửa: sửa chữ, thay ảnh trong từng khối. Mã theme: `odoo_local/addons/theme_custom_website` (SCSS, QWeb). Sửa SCSS xong mà chưa thấy đổi: `docker compose restart odoo` rồi tải lại trang.

### 2.8. BPMN

Mở `bpmn/*.bpmn` bằng Camunda Modeler → kéo gọn nếu muốn → File > Export as image (PNG) → thay ảnh trong `bpmn/`. Muốn sửa nội dung quy trình và sinh lại cả 5 file: sửa `tools/bpmn_specs.py` → `python tools/bpmn_gen.py`.

## Phần 3. Quay video cá nhân (theo tiêu chí)

Đặt tên: `Thao tác ERP - MSSV - [Họ và tên].mp4`. Có mặt và giọng nói (OBS Studio: nguồn màn hình + webcam góc phải). Nội dung 8–12 phút:

1. Chứng minh tự cài: mở Docker Desktop thấy 2 container; chạy `docker compose ps`; mở Thiết lập > Người dùng của tài khoản admin trên máy mình.
2. Thiết lập và nhập liệu căn bản: đổi một cấu hình, tạo một sản phẩm / khách / người dùng.
3. Thực hiện trọn quy trình mình phụ trách (mục 2.4), nói rõ mỗi bước thay giấy tờ nào và kiểm soát gì.
4. Bộ lọc, nhóm, lưu tìm kiếm; một báo cáo Pivot.
5. Gọi API cá nhân (script trong `scripts/`).

Mỗi bạn nên dựng hệ thống trên máy mình bằng mục 1.4 để video đúng là "Odoo do chính người quay cài đặt".

## Phần 4. Dựng báo cáo Word

### 4.1. Sửa nội dung

Sửa các file `baocao/*.md` (tiêu đề `#` là chương, `##` mục, `###` tiểu mục; bảng bằng `|`; hình `![chú thích](hinh/x.png)`).

### 4.2. Chụp lại ảnh (khi dữ liệu thay đổi)

`PYTHONIOENCODING=utf-8 python tools/chup_man_hinh.py` (Odoo phải đang chạy). Chụp riêng vài ảnh: thêm tên ảnh sau lệnh.

### 4.3. Dựng file

```
python tools/md2docx.py "Report - Nhóm 06.docx" baocao/00_bia.md baocao/00_mo_dau.md baocao/chuong1.md baocao/chuong2.md baocao/chuong3.md baocao/chuong4.md baocao/chuong5.md baocao/chuong6.md baocao/chuong7.md baocao/chuong8.md baocao/chuong9.md baocao/99_tham_khao_phu_luc.md baocao/phuluc_A_phong_van.md
```

Mở file trong Word, đồng ý "cập nhật trường" để mục lục tự sinh (hoặc nhấn chuột phải vào mục lục → Update Field → Update entire table). Điền họ tên 2 bạn, bảng phân công, tỷ lệ đóng góp ở chương 9 trước khi nộp. Nếu Khoa có template riêng: chép nội dung sang template, dùng Heading 1–3 để mục lục vẫn tự động.
