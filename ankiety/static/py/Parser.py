import json
import pandas as pd
from .DBManager import DBManager
import gviz_api

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
    def parse_to_chart(poll_id):

        responses_df = Parser.responses_to_dataframe(poll_id)
        names_types = DBManager.get_names_types(poll_id)

        for nt in names_types:
            if nt['type'] == 'r':
                data = responses_df[nt['name']]
                description = {
                    'index': ("number", "index"),
                    'name': ("number", "name")}
                data = data.to_dict('records')
                print(data)



            elif nt['type'] == 'c':
                data = responses_df[nt['name']]
                print(data)
            elif nt['type'] == 'n':
                data = responses_df[nt['name']]
                print(data)
            elif nt['type'] == 's':
                data = responses_df[nt['name']]
                print(data)


