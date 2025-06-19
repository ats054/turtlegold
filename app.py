from flask import Flask
from logic import check_signals

app = Flask(__name__)

@app.route('/ping')
def ping():
    result = check_signals()
    return result if result else "✅ נבדק - אין איתות כרגע"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)