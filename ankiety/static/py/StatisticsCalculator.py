import pandas as pd
import statistics
from statistics import mode
import json
import numpy as np

# radio, checkbox: answers_distribution []
# number, slider: ['Average', 'Mode', 'StdDev', 'Q1', 'Q3', 'Empty answers']
# text: empty_answers

class StatisticsCalculator:

    def get_basic_measurements(self, poll, responses):
        stats = {}
        for index, question in poll.iterrows():
            match question.type:
                case 'r':
                    stats[question.id] = get_response_distribution(question.value, responses[question.id])
                case 'c':
                    stats[question.id] = get_response_distribution(question.value, merge_lists(responses[question.id]))
                case 'n':
                    stats[question.id] = get_measures(responses[question.id])
                case 's':
                    stats[question.id] = get_measures(responses[question.id])
                case 't':
                    stats[question.id] = count_empty(responses[question.id])
                case _:
                    nothing = 0
        return stats


    def get_response_distribution(self, values, list):
        freq = [0] * len(values)
        for item in list:
            freq[item - 1] += 1  # +1 to the number of occurences of this question
        return [values, freq]


    def get_measures(self, list):
        result = {}
        result["Average"] = statistics.mean(list)
        result["Mode"] = mode(list)
        result["StdDev"] = statistics.stdev(list)
        result["Q1"] = list.quantile(0.25)
        result["Q3"] = list.quantile(0.75)
        result["Empty answers"] = count_empty(list)
        return result


    def count_empty(self, list):
        count = 0
        for item in list:
            if not item:
                count += 1
        return count


    def merge_lists(self, lists):
        result = []
        for list in lists:
            result.extend(list)
        return result


    '''
    df_r = pd.read_json("C:\\Users\\aneta\\Documents\\GitHub\\ankietopol\\ankietopol\\ankiety\\static\\examples\\responses2.json")
    print(df_r)
    df_p = pd.read_json("C:\\Users\\aneta\\Documents\\GitHub\\ankietopol\\ankietopol\\ankiety\\static\\examples\\items2.json")
    print(df_p)
    print(get_basic_measurements(df_p, df_r))
    '''
