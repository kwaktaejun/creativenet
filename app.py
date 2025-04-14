from flask import Flask, render_template, request, send_file
import pandas as pd
from io import BytesIO
from datetime import datetime

app = Flask(__name__)

FIELDS = [
    "구분", "계약여부", "식별번호", "계약금액", "제품모델명", "품명", "모델명",
    "규격", "수량", "원산지", "구성종류", "제품원가", "원천제조사", "수익률", "비고"
]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/download_excel", methods=["POST"])
def download_excel():
    # 1. form 입력 처리
    data = request.form.to_dict(flat=False)
    df_form = pd.DataFrame({k: v for k, v in data.items() if k in FIELDS})

    # 2. 엑셀 파일 업로드 처리
    uploaded_file = request.files.get("excel_file")
    df_excel = pd.DataFrame()
    if uploaded_file and uploaded_file.filename.endswith(".xlsx"):
        try:
            df_excel = pd.read_excel(uploaded_file)
        except Exception as e:
            print("엑셀 업로드 오류:", e)

    # 3. 병합
    df_all = pd.concat([df_form, df_excel], ignore_index=True)
    df_all = df_all[[col for col in FIELDS if col in df_all.columns]]

    # 4. 메모 처리
    memo = data.get("업로드메모", [""])[0]

    # 5. 엑셀로 출력
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df_all.to_excel(writer, index=False, sheet_name="마스터시트")
        if memo:
            memo_df = pd.DataFrame([{"업로드 메모": memo}])
            memo_df.to_excel(writer, index=False, sheet_name="업로드메모")
    output.seek(0)

    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    return send_file(output, as_attachment=True,
                     download_name=f"마스터시트_{now}.xlsx",
                     mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

if __name__ == "__main__":
    app.run(debug=True)