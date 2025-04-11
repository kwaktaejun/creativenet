
from flask import Flask, render_template, request, send_file
import pandas as pd

app = Flask(__name__)
FIELDS = ["구분", "계약여부", "식별번호", "계약금액", "제품모델명", "품명",
          "모델명", "규격", "수량", "원산지", "제품원가", "원천제조사", "비고"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = {field: request.form.getlist(f"{field}[]") for field in FIELDS}
    df = pd.DataFrame(data)
    output_path = "/mnt/data/마스터시트_엑셀형입력결과.xlsx"
    df.to_excel(output_path, index=False)
    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
