from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # 데이터 처리 로직 (예: 저장, 전송 등)
        pass
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)