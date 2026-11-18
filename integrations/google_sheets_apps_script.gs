/**
 * Google Apps Script nhận webhook từ Odoo (Automation Rule "BH4 - Việc cận hạn mới: gửi sang Google Sheets")
 * và ghi mỗi việc cận hạn thành một dòng trong sheet "CanHan". Quản lý xem trên điện thoại, lọc theo mức.
 *
 * Cài đặt: xem integrations/HUONG_DAN_TICH_HOP.md, mục 2.
 */
const SHEET_NAME = 'CanHan';
const SECRET = 'doi-chuoi-bi-mat-nay'; // trùng với tham số ?key=... trong URL webhook khai báo ở Odoo
const STAGES = { watch: 'Theo dõi', markdown: 'Giảm giá', recall: 'Thu hồi / cách ly', expired: 'Hết hạn' };

function doPost(e) {
  if (!e || e.parameter.key !== SECRET) {
    return json({ ok: false, error: 'unauthorized' });
  }
  const d = JSON.parse(e.postData.contents);
  const sheet = getSheet();
  // Odoo gửi many2one dưới dạng id; tên hiển thị lấy từ trường display (nếu có) hoặc giữ id
  sheet.appendRow([
    new Date(),
    d.id,
    d.product_id,
    d.lot_id,
    STAGES[d.stage] || d.stage,
    d.remaining_pct,
    d.qty,
    d.value,
    d.partner_id || 'Kho công ty',
    d.expiration_date,
  ]);
  return json({ ok: true });
}

function getSheet() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sh = ss.getSheetByName(SHEET_NAME);
  if (!sh) {
    sh = ss.insertSheet(SHEET_NAME);
    sh.appendRow(['Thời điểm nhận', 'Mã việc', 'Sản phẩm (id)', 'Lô (id)', 'Mức', '% hạn còn lại',
                  'Số lượng', 'Giá trị (VND)', 'Đang ở', 'Hạn sử dụng']);
    sh.setFrozenRows(1);
  }
  return sh;
}

function json(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}
