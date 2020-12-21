# -*- coding: utf-8 -*-

import json
import flask
from flask import Response

from category_predictor import CategoryPredictor

app = flask.Flask(__name__)

category_predictor = CategoryPredictor()


@app.route("/api/inference", methods=["POST"])
def predict_category():
    """
    Entry point
    """

    if flask.request.method == 'POST':
        request_json = flask.request.json

        name_text: str = request_json.get("name")
        short_description_text: str = request_json.get("short_description")
        short_description_mm_text: str = request_json.get("short_description_mm")
        long_description_text: str = request_json.get("long_description")
        long_description_mn_text: str = request_json.get("long_description_mm")
        marketing_text_mm_text: str = request_json.get("marketing_text_mm")

        result = category_predictor.run(name=name_text, short_description_text=short_description_text,
                                        short_description_mm_text=short_description_mm_text,
                                        long_description_text=long_description_text,
                                        long_description_mn_text=long_description_mn_text,
                                        marketing_text_mm_text=marketing_text_mm_text)

        response = Response(
            response=json.dumps({'results': result}),
            status=200,
            mimetype='application/json'
                            )
        return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, threaded=True)
