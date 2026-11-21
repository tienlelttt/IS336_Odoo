#!/usr/bin/env bash
# Dựng lại toàn bộ DB baohan từ đầu: module → theme → dữ liệu nền → tự động hóa → tuần go-live.
# Chạy trong Git Bash tại thư mục odoo_local:  bash ../scripts/rebuild_all.sh
# CẢNH BÁO: xóa DB baohan hiện tại (sao lưu trước nếu cần: docker compose exec -T db pg_dump -U odoo -Fc baohan > file.dump)
set -e
export MSYS_NO_PATHCONV=1
AP=/usr/lib/python3/dist-packages/odoo/addons,/mnt/extra-addons,/mnt/oca/manufacture,/mnt/oca/account-financial-reporting,/mnt/oca/server-ux,/mnt/oca/reporting-engine,/mnt/oca/stock-logistics-barcode
SHELL_RUN="docker compose run --rm -T odoo -- shell -d baohan --no-http --addons-path=$AP"
docker compose stop odoo
docker compose exec -T db dropdb -U odoo --if-exists baohan
docker compose run --rm -T odoo -- --addons-path=$AP -d baohan --load-language=vi_VN --without-demo=all --stop-after-init \
  -i sale_management,purchase,purchase_requisition,stock,stock_picking_batch,mrp,account,l10n_vn,l10n_vn_edi_viettel,crm,website_sale,base_automation,product_expiry,quality_control_oca,account_financial_report,partner_statement,bh_near_expiry,bh_api,theme_custom_website
printf '%s\n' "w = env['website'].search([], limit=1)" "m = env['ir.module.module'].search([('name','=','theme_custom_website')])" \
  "m.with_context(website_id=w.id)._theme_load(w)" "w.theme_id = m" "env.cr.commit()" | $SHELL_RUN
cat ../scripts/seed_data.py ../scripts/seed_odoo.py | $SHELL_RUN
$SHELL_RUN < ../scripts/automation_rules.py
cat ../scripts/seed_data.py ../scripts/demo_week.py | $SHELL_RUN
docker compose up -d odoo

# App đặt hàng gọi bh_api và ngân hàng gửi webhook qua HTTP thật (cần Python + requests trên máy)
for _ in $(seq 1 60); do curl -sf -o /dev/null http://localhost:8069/web/login && break; sleep 2; done
SQL="docker compose exec -T db psql -U odoo -d baohan -tAc"
TOKEN=$($SQL "select value from ir_config_parameter where key='bh_demo.api_token_kh02'")
# Hóa đơn khách trả sau đầu tiên chưa thu: khách chuyển khoản, nội dung ghi số hóa đơn
read -r INV AMT <<< "$($SQL "select name, amount_residual from account_move where move_type='out_invoice' \
  and state='posted' and payment_state='not_paid' and coalesce(ref,'') not like 'Số dư đầu kỳ%' order by id limit 1" | tr '|' ' ')"
if command -v python >/dev/null && [ -n "$TOKEN" ] && [ -n "$INV" ]; then
  PYTHONUTF8=1 BH_API_TOKEN="$TOKEN" python ../scripts/api_demo_calls.py "$INV" "$AMT"
else
  echo "Bỏ qua gọi API/webhook: thiếu Python, token hoặc hóa đơn chưa thu"
fi
