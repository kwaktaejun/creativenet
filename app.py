from flask import Flask, render_template, request, send_file
import pandas as pd
from openpyxl import load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows
import io
from datetime import datetime

app = Flask(__name__)

FIELDS = ["구분", "계약여부", "식별번호", "계약금액", "제품모델명", "품명", "모델명", "규격", "수량",
          "원산지", "구성종류", "제품원가", "원천제조사", "수익률", "비고", "메모"]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        input_data = {field: request.form.getlist(field) for field in FIELDS}
        df_form = pd.DataFrame(input_data)

        uploaded_file = request.files.get("excel_file")
        df_upload = pd.read_excel(uploaded_file) if uploaded_file and uploaded_file.filename.endswith(".xlsx") else pd.DataFrame()

        df_all = pd.concat([df_form, df_upload], ignore_index=True)
        df_all = df_all[[col for col in FIELDS if col in df_all.columns]]

        category = request.form.get('category', '기타')
        memo = request.form.get('memo', '')

        template_path = 'master_template_copy.xlsx'
        sheet_name = '영상감시 마스터시트' if category == '영상감시' else '출입통제 마스터시트'
        wb = load_workbook(template_path)
        ws = wb[sheet_name]

        start_row = ws.max_row + 1
        for r_idx, row in enumerate(dataframe_to_rows(df_all, index=False, header=False), start=start_row):
            for c_idx, value in enumerate(row, start=1):
                ws.cell(row=r_idx, column=c_idx, value=value)

        memo_sheet = wb.create_sheet("업로드메모")
        memo_sheet["A1"] = "업로드 메모"
        memo_sheet["B1"] = memo
        memo_sheet["A2"] = "제품군"
        memo_sheet["B2"] = category

        output = io.BytesIO()
        wb.save(output)
        output.seek(0)
        filename = f"마스터시트_{category}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        return send_file(output, download_name=filename, as_attachment=True)

    return render_template("index.html")