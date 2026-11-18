# Master data của case Bảo Hân. Thông tin công ty là thông tin công khai; còn lại là GIẢ ĐỊNH phục vụ học tập.
# Khách hàng và nhà cung cấp đều là tên mẫu (KH/NCC mẫu), không phải doanh nghiệp thật, để không bịa giao dịch với công ty thật.
# File được dùng bởi seed_odoo.py (nạp vào Odoo) và export_import_files.py (xuất CSV/XLSX cho phần Import).

COMPANY = {
    "name": "Công ty TNHH Bánh Bảo Hân",
    "vat": "0314345823",
    "street": "86 Đường 11, KP.5, P. Linh Xuân",
    "street2": "Xưởng: 71 Đường 20, KP.4, P. Hiệp Bình Chánh",
    "city": "TP. Thủ Đức, TP. Hồ Chí Minh",
    "phone": "(028) 6274 7929",
    "email": "kinhdoanh@baohan.local",
    "website": "http://localhost:8069",
}

# Mật khẩu thử nghiệm cho môi trường local (không dùng khi triển khai thật).
TEST_PASSWORD = "BaoHan#2026"

# login, tên, chức danh, danh sách xmlid nhóm quyền
USERS = [
    ("giamdoc@baohan.local", "Nguyễn Văn Giám Đốc (mẫu)", "Giám đốc", [
        "sales_team.group_sale_manager", "purchase.group_purchase_manager", "stock.group_stock_manager",
        "mrp.group_mrp_manager", "account.group_account_manager", "quality_control_oca.group_quality_control_manager"]),
    ("kinhdoanh1@baohan.local", "Trần Thị Kinh Doanh 1 (mẫu)", "Nhân viên kinh doanh", ["sales_team.group_sale_salesman"]),
    ("kinhdoanh2@baohan.local", "Lê Văn Kinh Doanh 2 (mẫu)", "Trưởng nhóm kinh doanh", ["sales_team.group_sale_salesman_all_leads"]),
    ("muahang@baohan.local", "Phạm Thị Mua Hàng (mẫu)", "Nhân viên mua hàng", ["purchase.group_purchase_user", "stock.group_stock_user"]),
    ("quandoc@baohan.local", "Hoàng Văn Quản Đốc (mẫu)", "Quản đốc sản xuất", ["mrp.group_mrp_manager", "stock.group_stock_user"]),
    ("qc@baohan.local", "Võ Thị Kiểm Soát (mẫu)", "Nhân viên QC", ["quality_control_oca.group_quality_control_user", "stock.group_stock_user"]),
    ("thukho@baohan.local", "Đặng Văn Thủ Kho (mẫu)", "Thủ kho", ["stock.group_stock_user"]),
    ("ketoan@baohan.local", "Bùi Thị Kế Toán (mẫu)", "Kế toán", ["account.group_account_manager", "sales_team.group_sale_salesman_all_leads",
                                                               "purchase.group_purchase_user"]),
]

# Vị trí kho con dưới WH/Stock
LOCATIONS = ["Kho khô", "Kho mát", "Kho bao bì", "TP nhiệt độ thường", "TP lạnh", "TP đông", "Khu cách ly"]

# tên nhóm, nhóm cha, vị trí cất (putaway), FEFO?
CATEGORIES = [
    ("Thành phẩm", None, None, True),
    ("Bánh mì tươi", "Thành phẩm", "TP nhiệt độ thường", True),
    ("Bánh ngọt", "Thành phẩm", "TP nhiệt độ thường", True),
    ("Bánh lạnh", "Thành phẩm", "TP lạnh", True),
    ("Bánh khô", "Thành phẩm", "TP nhiệt độ thường", True),
    ("Cấp đông", "Thành phẩm", "TP đông", True),
    ("Nguyên vật liệu", None, None, True),
    ("NVL khô", "Nguyên vật liệu", "Kho khô", True),
    ("NVL mát", "Nguyên vật liệu", "Kho mát", True),
    ("Bao bì", None, "Kho bao bì", False),
    ("Phụ phẩm", None, "Kho khô", False),
]

# mã, tên, nhóm, giá bán sỉ (VND), hạn dùng (ngày), có bán web?
FINISHED = [
    ("FG01", "Bánh mì Hoppi (gói 6 cái)", "Bánh mì tươi", 22000, 5, True),
    ("FG02", "Bánh mì sandwich trắng 400g", "Bánh mì tươi", 25000, 5, True),
    ("FG03", "Bánh mì sandwich đen 400g", "Bánh mì tươi", 32000, 5, True),
    ("FG04", "Bánh mì nguyên cám 400g", "Bánh mì tươi", 35000, 5, True),
    ("FG05", "Bông lan cắt lát OEM (hộp 10 miếng)", "Bánh ngọt", 38000, 30, False),
    ("FG06", "Bánh tiệc trà (khay 20 cái)", "Bánh ngọt", 85000, 15, True),
    ("FG07", "Bánh lạnh mousse (hộp 6 cái)", "Bánh lạnh", 90000, 3, True),
    ("FG08", "Cookies bơ socola (túi 250g)", "Bánh khô", 45000, 180, True),
    ("FG09", "Đế pizza nhỏ 18cm (gói 5)", "Cấp đông", 20000, 180, True),
    ("FG10", "Đế pizza lớn 28cm (gói 3)", "Cấp đông", 28000, 180, True),
    ("FG11", "Pizza xúc xích 18cm", "Cấp đông", 39000, 180, True),
    ("FG12", "Vỏ bánh tart (khay 24)", "Cấp đông", 55000, 180, True),
]
FG_IMAGES = {"FG01": "hero_bakery.jpg", "FG03": "oven.jpg", "FG05": "cakes.jpg", "FG12": "cookies.jpg", "FG02": "bread_sliced.jpg", "FG04": "bread_sliced.jpg", "FG06": "cakes.jpg", "FG07": "cakes.jpg",
             "FG08": "cookies.jpg", "FG11": "pizza.jpg", "FG09": "pizza.jpg", "FG10": "pizza.jpg"}

# mã, tên, nhóm, đơn vị (kg/L/Đơn vị), giá mua, hạn dùng (0 = không theo lô), mã NCC, min, max
RAW = [
    ("RM01", "Bột mì số 11", "NVL khô", "kg", 18000, 180, "NCC01", 200, 600),
    ("RM02", "Bột mì số 8 (bánh ngọt)", "NVL khô", "kg", 20000, 180, "NCC01", 80, 250),
    ("RM03", "Đường cát trắng", "NVL khô", "kg", 22000, 0, "NCC01", 80, 250),
    ("RM04", "Muối tinh", "NVL khô", "kg", 8000, 0, "NCC01", 10, 40),
    ("RM05", "Men khô instant", "NVL khô", "kg", 120000, 365, "NCC02", 5, 20),
    ("RM06", "Bột nở", "NVL khô", "kg", 90000, 365, "NCC02", 3, 10),
    ("RM07", "Bơ lạt", "NVL mát", "kg", 210000, 120, "NCC03", 20, 60),
    ("RM08", "Trứng gà", "NVL mát", "Đơn vị", 3200, 21, "NCC04", 1000, 3000),
    ("RM09", "Sữa tươi không đường", "NVL mát", "L", 32000, 10, "NCC03", 30, 100),
    ("RM10", "Kem tươi whipping", "NVL mát", "L", 120000, 30, "NCC03", 10, 30),
    ("RM11", "Phô mai mozzarella", "NVL mát", "kg", 190000, 60, "NCC03", 10, 30),
    ("RM12", "Xúc xích", "NVL mát", "kg", 110000, 45, "NCC05", 10, 40),
    ("RM13", "Sốt cà chua pizza", "NVL khô", "kg", 60000, 180, "NCC05", 10, 30),
    ("RM14", "Dầu ăn", "NVL khô", "L", 45000, 0, "NCC01", 20, 60),
    ("RM15", "Socola chip", "NVL khô", "kg", 180000, 365, "NCC02", 5, 20),
    ("RM16", "Bột cacao", "NVL khô", "kg", 150000, 365, "NCC02", 5, 15),
    ("RM17", "Ngũ cốc nguyên cám", "NVL khô", "kg", 40000, 180, "NCC01", 20, 60),
    ("PK01", "Túi in nhãn bánh mì", "Bao bì", "Đơn vị", 600, 0, "NCC06", 2000, 8000),
    ("PK02", "Hộp nhựa bánh ngọt", "Bao bì", "Đơn vị", 2500, 0, "NCC06", 300, 1000),
    ("PK03", "Khay giấy", "Bao bì", "Đơn vị", 1500, 0, "NCC06", 300, 1000),
    ("PK04", "Túi zip cookies", "Bao bì", "Đơn vị", 1200, 0, "NCC06", 300, 1000),
    ("PK05", "Thùng carton", "Bao bì", "Đơn vị", 6000, 0, "NCC06", 100, 400),
    ("PK06", "Màng co đế pizza", "Bao bì", "Đơn vị", 400, 0, "NCC06", 500, 2000),
]
BYPRODUCT = ("BP01", "Vụn bánh (phụ phẩm)", "Phụ phẩm", "kg", 5000)

# mã, tên, chi phí/giờ, công suất song song
WORKCENTERS = [
    ("WC01", "Khu trộn và nhào", 180000, 1),
    ("WC02", "Phòng ủ bột", 60000, 2),
    ("WC03", "Lò nướng đối lưu", 250000, 1),
    ("WC04", "Khu làm nguội và đóng gói", 150000, 1),
    ("WC05", "Tủ cấp đông nhanh", 120000, 1),
]

# BoM cho 1 mẻ (bản 2: định mức theo khối lượng thực tế, tối đa 4 công đoạn):
# mã TP, SL mẻ, [(mã NVL, SL)], [(tên công đoạn, mã WC, phút/mẻ)], phụ phẩm kg
# Ví dụ FG02: ổ 400 g cần ~230 g bột → 100 ổ ~23 kg bột (đúng 1 cối trộn 25 kg).
BOMS = [
    ("FG01", 100, [("RM01", 18), ("RM03", 2.2), ("RM04", .3), ("RM05", .25), ("RM07", 1.6), ("RM08", 30), ("RM09", 4),
                   ("PK01", 100), ("PK05", 5)],
     [("Chuẩn bị và trộn", "WC01", 40), ("Ủ bột", "WC02", 90), ("Nướng", "WC03", 30), ("Làm nguội, đóng gói", "WC04", 60)], 0),
    ("FG02", 100, [("RM01", 23), ("RM03", 1.5), ("RM04", .45), ("RM05", .3), ("RM07", 1.5), ("RM09", 5), ("PK01", 100), ("PK05", 5)],
     [("Chuẩn bị và trộn", "WC01", 40), ("Ủ bột", "WC02", 90), ("Nướng", "WC03", 40), ("Làm nguội, cắt lát, đóng gói", "WC04", 60)], 1),
    ("FG03", 100, [("RM01", 16), ("RM17", 6), ("RM16", .8), ("RM03", 1.8), ("RM04", .45), ("RM05", .3), ("RM07", 1.2),
                   ("PK01", 100), ("PK05", 5)],
     [("Chuẩn bị và trộn", "WC01", 40), ("Ủ bột", "WC02", 90), ("Nướng", "WC03", 40), ("Làm nguội, cắt lát, đóng gói", "WC04", 60)], 1),
    ("FG04", 100, [("RM01", 12), ("RM17", 11), ("RM03", 1.2), ("RM04", .45), ("RM05", .3), ("RM14", 1), ("PK01", 100), ("PK05", 5)],
     [("Chuẩn bị và trộn", "WC01", 40), ("Ủ bột", "WC02", 100), ("Nướng", "WC03", 45), ("Làm nguội, cắt lát, đóng gói", "WC04", 60)], 1),
    ("FG05", 100, [("RM02", 7), ("RM03", 7), ("RM08", 280), ("RM09", 4), ("RM14", 3), ("RM06", .2), ("PK02", 100), ("PK05", 5)],
     [("Chuẩn bị và trộn", "WC01", 40), ("Nướng", "WC03", 40), ("Làm nguội, cắt, đóng hộp", "WC04", 60)], .8),
    ("FG06", 50, [("RM02", 6), ("RM03", 4), ("RM07", 3), ("RM08", 100), ("RM10", 2), ("PK03", 50), ("PK05", 3)],
     [("Chuẩn bị và trộn", "WC01", 40), ("Nướng", "WC03", 40), ("Trang trí, đóng khay", "WC04", 60)], 0),
    ("FG07", 50, [("RM02", 1.5), ("RM03", 3), ("RM08", 50), ("RM10", 6), ("RM09", 3), ("RM16", .5), ("PK02", 50)],
     [("Chuẩn bị đế và kem", "WC01", 40), ("Làm lạnh định hình", "WC05", 180), ("Đóng hộp", "WC04", 30)], 0),
    ("FG08", 100, [("RM02", 10), ("RM07", 6), ("RM03", 6), ("RM08", 50), ("RM15", 3), ("PK04", 100), ("PK05", 5)],
     [("Chuẩn bị và trộn", "WC01", 30), ("Nướng", "WC03", 60), ("Làm nguội, đóng túi", "WC04", 45)], .3),
    ("FG09", 100, [("RM01", 25), ("RM05", .3), ("RM04", .4), ("RM14", 1.5), ("PK06", 100), ("PK05", 4)],
     [("Chuẩn bị, cán đế", "WC01", 30), ("Nướng sơ", "WC03", 40), ("Cấp đông", "WC05", 120), ("Đóng gói", "WC04", 45)], 0),
    ("FG10", 100, [("RM01", 36), ("RM05", .45), ("RM04", .6), ("RM14", 2.2), ("PK06", 100), ("PK05", 6)],
     [("Chuẩn bị, cán đế", "WC01", 35), ("Nướng sơ", "WC03", 45), ("Cấp đông", "WC05", 120), ("Đóng gói", "WC04", 45)], 0),
    ("FG11", 100, [("RM01", 9), ("RM05", .12), ("RM13", 4), ("RM11", 5), ("RM12", 5), ("PK06", 100), ("PK05", 5)],
     [("Làm đế", "WC01", 40), ("Phủ nhân", "WC04", 50), ("Nướng", "WC03", 30), ("Cấp đông", "WC05", 120)], 0),
    ("FG12", 50, [("RM02", 9), ("RM07", 4.5), ("RM03", 2), ("RM08", 40), ("PK03", 50), ("PK05", 3)],
     [("Chuẩn bị và trộn", "WC01", 30), ("Ép khuôn", "WC04", 60), ("Nướng", "WC03", 40), ("Cấp đông", "WC05", 120)], .2),
]

# Kế hoạch sản xuất: bánh tươi làm theo nhu cầu đơn (min = max = 0, quản đốc chốt), hàng trữ theo min/max,
# OEM làm theo đơn (MTO). mã TP: (kiểu, min, max)
FG_PLANNING = {
    "FG01": ("tuoi", 0, 0), "FG02": ("tuoi", 0, 0), "FG03": ("tuoi", 0, 0), "FG04": ("tuoi", 0, 0),
    "FG07": ("tuoi", 0, 0), "FG06": ("tru", 10, 30), "FG05": ("oem", 0, 0),
    "FG08": ("tru", 100, 300), "FG09": ("tru", 100, 300), "FG10": ("tru", 100, 300),
    "FG11": ("tru", 100, 300), "FG12": ("tru", 50, 150),
}

# Tuyến giao (nhãn khách hàng)
ROUTES = ["Tuyến 1 - Linh Xuân - Linh Trung", "Tuyến 2 - Hiệp Bình - Tam Bình", "Tuyến 3 - Thủ Đức - Bình Thạnh"]

# Hợp đồng giá theo quý với NCC chính (thỏa thuận mua hàng): mã NCC, [(mã NVL, số lượng dự kiến quý, giá)]
BLANKET_ORDERS = [
    ("NCC01", [("RM01", 6000, 17500), ("RM02", 1500, 19500), ("RM03", 1500, 21500), ("RM14", 300, 44000), ("RM17", 800, 39000)]),
    ("NCC03", [("RM07", 500, 205000), ("RM09", 800, 31000), ("RM10", 200, 118000)]),
    ("NCC04", [("RM08", 40000, 3100)]),
]

# Quy tắc cận hạn riêng theo nhóm (bổ sung cho quy tắc chung 50/30/15 có sẵn trong module):
# nhóm, mức, ngưỡng % còn lại, % giảm giá, hướng dẫn
EXPIRY_RULES = [
    ("Bánh mì tươi", "recall", 40, 0, "Bánh mì còn ≤ 2 ngày: thu hồi ở chuyến giao sau, không bán tiếp."),
    ("Bánh lạnh", "recall", 34, 0, "Bánh lạnh còn ≤ 1 ngày: thu hồi, cách ly."),
    ("NVL mát", "watch", 50, 0, "Ưu tiên cấp lô này cho sản xuất trước."),
    ("NVL mát", "recall", 15, 0, "Không dùng cho sản xuất, chuyển Khu cách ly, báo NCC."),
]

# Bảng giá: tên, % giảm so với giá niêm yết
PRICELISTS = [("Giá sỉ quán", 0), ("Giá siêu thị - bếp ăn", 5), ("Giá OEM theo hợp đồng", 8)]

# Nhà cung cấp mẫu: mã, tên, nhóm hàng
VENDORS = [
    ("NCC01", "NCC mẫu 01 - Bột mì, đường, dầu"),
    ("NCC02", "NCC mẫu 02 - Men, phụ gia, socola"),
    ("NCC03", "NCC mẫu 03 - Bơ sữa"),
    ("NCC04", "NCC mẫu 04 - Trứng gà"),
    ("NCC05", "NCC mẫu 05 - Xúc xích, sốt"),
    ("NCC06", "NCC mẫu 06 - Bao bì"),
]
VENDOR_LEAD_DAYS = {"NCC01": 2, "NCC02": 3, "NCC03": 1, "NCC04": 1, "NCC05": 2, "NCC06": 5}

# Khách hàng mẫu: mã, tên, bảng giá, điều khoản (immediate/30), hạn mức nợ, tuyến (0-2), trả tiền mặt cho tài xế?
CUSTOMERS = [
    ("KH01", "Quán cà phê Mộc (KH mẫu)", "Giá sỉ quán", "immediate", 0, 0, True),
    ("KH02", "Chuỗi trà sữa Lá Xanh (KH mẫu)", "Giá sỉ quán", "immediate", 10000000, 0, False),
    ("KH03", "Siêu thị mini Hiệp Bình (KH mẫu)", "Giá siêu thị - bếp ăn", "30", 30000000, 1, False),
    ("KH04", "Bếp ăn công nghiệp KCN (KH mẫu)", "Giá siêu thị - bếp ăn", "30", 80000000, 1, False),
    ("KH05", "Trường THPT Linh Trung (KH mẫu)", "Giá siêu thị - bếp ăn", "30", 30000000, 2, False),
    ("KH06", "Thương hiệu bánh OEM Sao Mai (KH mẫu)", "Giá OEM theo hợp đồng", "30", 120000000, 2, False),
    ("KH07", "Tạp hóa Bà Sáu (KH mẫu)", "Giá sỉ quán", "immediate", 0, 0, True),
    ("KH08", "Quán cà phê Sân Thượng (KH mẫu)", "Giá sỉ quán", "immediate", 0, 2, True),
]

# Đơn cố định hằng ngày (thứ 2 = 0 … thứ 6 = 4): mã KH: {thứ: [(mã SP, SL)]}; None = mọi ngày làm việc
STANDING_ORDERS = {
    "KH01": {None: [("FG01", 10), ("FG02", 6)]},
    "KH02": {0: [("FG06", 2), ("FG08", 10)], 3: [("FG06", 2), ("FG08", 10)]},
    "KH03": {0: [("FG02", 30), ("FG03", 20), ("FG08", 20), ("FG11", 20)], 3: [("FG02", 30), ("FG03", 20), ("FG08", 20)]},
    "KH04": {None: [("FG01", 120), ("FG02", 60)]},
    "KH05": {None: [("FG01", 80)]},
    "KH07": {None: [("FG01", 10), ("FG04", 5)]},
    "KH08": {None: [("FG07", 2), ("FG02", 4)]},
}

# Phiếu kiểm tra chất lượng (OCA quality_control): tên, [(câu hỏi, loại, min, max, đơn vị)]
QC_TESTS = [
    ("Kiểm nguyên liệu mát đầu vào", [
        ("Nhiệt độ hàng khi nhận (°C)", "quantitative", 0, 5, None),
        ("Bao bì nguyên vẹn, không rò rỉ", "qualitative", None, None, None),
        ("Hạn dùng còn ít nhất 2/3", "qualitative", None, None, None)]),
    ("Kiểm nguyên liệu khô đầu vào", [
        ("Bao bì khô, không ẩm mốc, không côn trùng", "qualitative", None, None, None),
        ("Có số lô và hạn dùng trên bao", "qualitative", None, None, None)]),
    ("Kiểm mẫu thành phẩm theo lô", [
        ("Nhiệt độ lõi bánh sau nướng (°C, que đo)", "quantitative", 92, 99, None),
        ("Cảm quan: màu vỏ, mùi, ruột bánh đạt", "qualitative", None, None, None),
        ("Khối lượng mẫu trong dung sai ±3%", "qualitative", None, None, None),
        ("Nhãn đủ ngày sản xuất, hạn dùng, số lô", "qualitative", None, None, None)]),
]
