
from flask import Flask, render_template, request, send_file
import pandas as pd
import io
from datetime import datetime

app = Flask(__name__)

FIELDS = ["구분", "계약여부", "식별번호", "계약금액", "제품모델명", "품명", "모델명", "규격", "수량",
          "원산지", "구성종류", "제품원가", "원천제조사", "수익률", "비고", "메모"]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # 입력 필드 리스트화
        inputs = {field: request.form.getlist(field) for field in FIELDS}
        df = pd.DataFrame(inputs)
        df = df[[col for col in FIELDS if col in df.columns]]
        memo = request.form.get('memo')
        category = request.form.get('category', '기타')

        # 엑셀 생성
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name="업로드데이터")
            pd.DataFrame([{"업로드 메모": memo, "제품군": category}]).to_excel(writer, sheet_name="메모", index=False)

        output.seek(0)
        filename = f"업로드_{category}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        return send_file(output, download_name=filename, as_attachment=True)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
