from flask import Flask, render_template, request, send_file
import pandas as pd
from openpyxl import load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from io import BytesIO
from datetime import datetime

app = Flask(__name__)

FIELDS = [
    "구분", "계약여부", "식별번호", "계약금액", "제품모델명", "품명", "모델명",
    "규격", "수량", "원산지 / 제조사", "구성종류", "제품원가", "원천제조사", "수익률"
]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/download_excel", methods=["POST"])
def download_excel():
    data = request.form.to_dict(flat=False)
    df = pd.DataFrame({k: v for k, v in data.items() if k in FIELDS})
    memo = data.get("업로드메모", [""])[0]

    # 템플릿 로드
    template_path = "download_template_copy.xlsx"
    wb = load_workbook(template_path)
    ws = wb.active  # 첫 시트 사용

    # 삽입 시작 위치
    start_row = ws.max_row + 1

    # 삽입 (양식은 이미 시트에 정의되어 있음)
    for r_idx, row in enumerate(dataframe_to_rows(df, index=False, header=False), start=start_row):
        for c_idx, val in enumerate(row, start=1):
            ws.cell(row=r_idx, column=c_idx, value=val)

    # 메모 시트 추가
    memo_ws = wb.create_sheet("업로드메모")
    memo_ws["A1"] = "업로드 메모"
    memo_ws["B1"] = memo

    # 저장
    output = BytesIO()
    wb.save(output)
    output.seek(0)

    filename = f"다운로드_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    return send_file(output, download_name=filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)