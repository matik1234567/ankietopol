import json
import pandas as pd
from .DBManager import DBManager

class Parser:
    @staticmethod
    def responses_to_dataframe(poll_id):
        responses = DBManager.get_responses(poll_id)

        js = str(responses)
        js = js.replace('\"', '')
        js = js.replace('\'', '\"')

        dataframe = pd.read_json(js)
        dataframe.columns = DBManager.get_names(poll_id)
        return dataframe

    @staticmethod
    def parse_to_chart(response, poll_id, name):
        responses = DBManager.get_responses(poll_id)
