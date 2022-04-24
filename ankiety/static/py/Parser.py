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
    def get_poll_model(poll_id):
        poll = DBManager.get_poll_model(poll_id)
        return pd.read_json(poll)

    @staticmethod
    def get_response_hist(data, attribute):
        dict_of_freq = {}
        for v in data.unique():
            dict_of_freq[str(v)] = 0
        for item in data.tolist():
            dict_of_freq[str(item)] += 1  # +1 to the number of occurences of this question

        return [[str(int(float(key))), value] for key, value in dict_of_freq.items()]

    @staticmethod
    def parse_to_chart(poll_id):

        responses_df = Parser.responses_to_dataframe(poll_id)
        names_types = DBManager.get_names_types(poll_id)

        for nt in names_types:
            if nt['type'] == 'r':
                data = responses_df[nt['name']]
                data = data.dropna()
                title = nt['description']
                return Parser.get_response_hist(data, nt['name']), title

            elif nt['type'] == 'c':
                data = responses_df[nt['name']]
                print(data)
            elif nt['type'] == 'n':
                data = responses_df[nt['name']]
                print(data)
            elif nt['type'] == 's':
                data = responses_df[nt['name']]
                print(data)


