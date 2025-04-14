
import { saveAs } from "file-saver";
import { generateExcelFile } from "../utils/excelUtils";

export function UploadForm({ products, memo }) {
  const handleDownload = () => {
    const file = generateExcelFile(products, memo);
    saveAs(file, "업로드_데이터.xlsx");
  };

  return (
    <div>
      <button
        onClick={handleDownload}
        className="bg-blue-500 text-white px-4 py-2 rounded"
      >
        엑셀 다운로드
      </button>
    </div>
  );
}
