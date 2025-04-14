
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
    data = request.form.to_dict(flat=False)
    df = pd.DataFrame({k: v for k, v in data.items() if k in FIELDS})
    memo = data.get("업로드메모", [""])[0]

    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name="마스터시트")
        if memo:
            pd.DataFrame([{"업로드 메모": memo}]).to_excel(writer, index=False, sheet_name="업로드메모")
    output.seek(0)
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    return send_file(output, as_attachment=True, download_name=f"마스터시트_{now}.xlsx")

if __name__ == "__main__":
    app.run(debug=True)
