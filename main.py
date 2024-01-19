import math

from flask import Flask, render_template, request
from flask_cors import CORS

from anthroscore import get_text_score

# from anthroscore import get_text_score

app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html',)


@app.route('/predict', methods=['POST'])
def predict():
    text = request.form.get('text')
    text = text[:1024]
    entities = request.form.get('entities')
    entities = entities[:1024]

    entities = [e.strip()for e in entities.split(",")]
    score = get_text_score(text, entities)
    if not math.isnan(score):
        score = str(score)
    else:
        score = "No words found."
    return score

if __name__ == '__main__':
    app.run(
        "0.0.0.0",
        port=5000,
        debug=True,
    )
