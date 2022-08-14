from datetime import datetime

from flask import jsonify, request

from sm_api.api.app import app
from sm_api.models.likes import LikesModel as lm


@app.route('/api/analytics', methods=["GET"])
def get_analytics():
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')

    if not (date_from and date_to):
        return jsonify(message=f"Input a period"), 400

    date_from_datetime = datetime.strptime(date_from, '%m/%d/%y')
    date_to_datetime = datetime.strptime(date_to, '%m/%d/%y')

    res_data = lm.get_likes_for_period(date_from_datetime, date_to_datetime)
    return jsonify(res_data), 200
