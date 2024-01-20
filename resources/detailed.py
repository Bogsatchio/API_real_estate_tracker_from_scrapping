import os
import traceback
import pandas as pd
from collections import OrderedDict
from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from data_prep_and_insert import refresh_database

from data_prep_and_insert import process_file, file_processing
from utils.sqls import get_latest_search, get_prices_over_time
from db import db

blp = Blueprint("detailed", __name__, description="Utilities and queries concering just the data for selected city and size of apartment")

@blp.route("/detailed/latest/<city>/<min_s>/<max_s>")
class LatestSearch(MethodView):
    def get(self, city, min_s, max_s):
        try:
            df = pd.read_sql(get_latest_search(city, min_s, max_s), db.engine)
            json_data = df.to_dict(orient="index", into=OrderedDict)
            return jsonify(json_data), 200
        except Exception as e:
            error_traceback = traceback.format_exc()
            error_message = {
                'error_type': type(e).__name__,
                'error_message': str(e),
                'error_traceback': error_traceback
            }
            return jsonify(error_message), 404


@blp.route("/detailed/prices_over_time/<city>/<min_s>/<max_s>")
class PricesOverTime(MethodView):
    def get(self, city, min_s, max_s):
        try:
            df = pd.read_sql(get_prices_over_time(city, min_s, max_s), db.engine)
            df.set_index("scrapped_time", inplace=True)
            json_data = df.to_dict(orient="index")
            json_data = {key: value["average_price_sqm"] for key, value in json_data.items()}
            return jsonify(json_data), 200
        except Exception as e:
            error_traceback = traceback.format_exc()
            error_message = {
                'error_type': type(e).__name__,
                'error_message': str(e),
                'error_traceback': error_traceback
            }
            return jsonify(error_message), 404




