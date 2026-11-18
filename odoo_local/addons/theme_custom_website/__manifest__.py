{
    "name": "Bảo Hân Bakery Theme",
    "summary": "Theme website cho xưởng bánh: bảng màu kem - socola - caramel, font Be Vietnam Pro và Lora",
    "description": "Theme Odoo 19 cho website bán sỉ và gia công OEM bánh. Chỉ gồm SCSS và QWeb nên import được lên Odoo Online.",
    "version": "19.0.1.0.0",
    "category": "Theme/Retail",
    "author": "Nhóm 06 - IS336.R12 - UIT",
    "license": "LGPL-3",
    "depends": ["website"],
    "data": [
        "views/homepage.xml",
        "views/layout.xml",
    ],
    "assets": {
        "web._assets_primary_variables": [
            "theme_custom_website/static/src/scss/primary_variables.scss",
        ],
        "web.assets_frontend": [
            "theme_custom_website/static/src/scss/custom.scss",
        ],
    },
    "installable": True,
}
