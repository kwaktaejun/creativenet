from flask import Flask, render_template, request, send_file
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        excel_file = request.files.get('excel_file')
        memo = request.form.get('memo')
        category = request.form.get('category')

        if excel_file:
            df = pd.read_excel(excel_file, sheet_name=None)
            writer_path = f"upload_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            with pd.ExcelWriter(writer_path, engine='openpyxl') as writer:
                for name, sheet in df.items():
                    sheet.to_excel(writer, index=False, sheet_name=name)
                pd.DataFrame([{"업로드 메모": memo, "제품군": category}]).to_excel(writer, sheet_name="업로드 메모", index=False)
            return send_file(writer_path, as_attachment=True)
    return render_template('index.html')
    
if __name__ == '__main__':
    app.run(debug=True)