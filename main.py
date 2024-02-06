import math
import uuid

from flask import Flask, render_template, request, make_response
from flask_cors import CORS
import json
from anthroscore import get_text_score
from datetime import datetime

MAX_LENGTH = 1024 * 5

app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', )


@app.route('/predict', methods=['POST'])
def predict():
    text = request.form.get('text')
    text = text[:MAX_LENGTH]
    entities = request.form.get('entities')
    entities = entities[:MAX_LENGTH]

    entities = [e.strip() for e in entities.split(",")]

    score = get_text_score(text, entities)
    if not math.isnan(score):
        score = str(score)
    else:
        score = "No words found."

    user_id = request.cookies.get('user_id')

    response = make_response(score)
    if user_id is None:
        user_id = uuid.uuid4().hex
        response.set_cookie('user_id', user_id)

    log_entry = json.dumps({"text": text,
                            "entities": entities,
                            "timestamp": datetime.now().isoformat(),
                            "user_id": user_id})

    with open("requests.log", "a") as log:
        log.write(log_entry + "\n")

    return response


if __name__ == '__main__':
    app.run(
        "0.0.0.0",
        port=5000,
        debug=True,
    )
