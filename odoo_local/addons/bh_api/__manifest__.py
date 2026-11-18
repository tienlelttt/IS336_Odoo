{
    "name": "Bảo Hân - API cho đối tác",
    "summary": "REST API có token, phạm vi quyền, giới hạn tần suất, nhật ký; webhook nhận biến động số dư ngân hàng",
    "version": "19.0.1.0.0",
    "category": "Sales/Sales",
    "author": "Nhóm 06 - IS336.R12 - UIT",
    "license": "LGPL-3",
    "depends": ["sale_stock", "account"],
    "data": [
        "security/ir.model.access.csv",
        "views/bh_api_views.xml",
        "wizard/token_wizard_views.xml",
        "views/menus.xml",
    ],
    "installable": True,
}
