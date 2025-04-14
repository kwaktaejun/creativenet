
import ExcelJS from "exceljs";
import { saveAs } from "file-saver";

export function generateExcelFile(products, memo) {
  const wb = new ExcelJS.Workbook();
  const ws = wb.addWorksheet("업로드 데이터");
  const memoSheet = wb.addWorksheet("업로드 메모");

  const columns = ["계약여부", "식별번호", "계약금액", "제품모델명", "품명", "모델명", "규격", "수량", "원산지", "비고"];
  ws.addRow(columns);
  products.forEach(p => {
    ws.addRow(columns.map(c => p[c] || ""));
  });

  memoSheet.addRow(["업로드 메모"]);
  memoSheet.addRow([memo]);

  return wb.xlsx.writeBuffer().then((buffer) => new Blob([buffer]));
}
