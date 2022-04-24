import pandas as pd
import statistics
from statistics import mode
import json
import numpy as np

# radio, checkbox: answers_distribution []
# number, slider: ['Average', 'Mode', 'StdDev', 'Q1', 'Q3', 'Empty answers']
# text: empty_answers

class StatisticsCalculator:

    @staticmethod
    def get_basic_measurements(poll, responses):
        stats = []
        for question in poll:
            match question['type']:
                case 'r':
                    stats.append({'data': StatisticsCalculator.__get_response_hist(responses[question['name']].dropna()),
                                  'title': question['title'],
                                  'questions':question['questions'],
                                  'measures': 3})
                    return StatisticsCalculator.__get_response_hist(responses[question['name']].dropna()), question['title'], question['questions'], StatisticsCalculator.__get_measures_continuous(responses[question['name']])
                case 'c':
                    stats[question.id] = StatisticsCalculator.__get_response_hist(question.value, StatisticsCalculator.__merge_lists(responses[question.id]))
                case 'n':
                    stats[question.id] = StatisticsCalculator.__get_measures_continuous(responses[question.id])
                case 's':
                    stats[question.id] = StatisticsCalculator.__get_measures_continuous(responses[question.id])
                case 't':
                    nothing = 0 # TODO: string length distribution??
        return stats

    @staticmethod
    def __get_response_distribution(values, list):
        freq = [0] * len(values)
        for item in list:
            freq[item - 1] += 1  # +1 to the number of occurences of this answer
        return [values, freq]

    @staticmethod
    def __get_response_hist(data):
        dict_of_freq = {}
        for v in data.unique():
            dict_of_freq[str(v)] = 0
        for item in data.tolist():
            dict_of_freq[str(item)] += 1  # +1 to the number of occurences of this question

        return [[str(int(float(key))), value] for key, value in dict_of_freq.items()]

    @staticmethod
    def __get_measures_continuous(list): # get measures for continuous variables
        result = {}
        result['Total poll answers'] = len(list)
        list = list.dropna()
        result['Empty poll answers'] = result['Total poll answers'] - len(list)
        result["Average"] = statistics.mean(list)
        result["Mode"] = mode(list)
        result["StdDev"] = statistics.stdev(list)
        result["Q1"] = list.quantile(0.25)
        result["Q3"] = list.quantile(0.75)
        result["Empty answers"] = StatisticsCalculator.__count_empty(list)
        return result

    @staticmethod
    def __get_measures_discrete(list):  # get measures for continuous variables
        result = {}
        return result

    @staticmethod
    def __count_empty(list):
        count = 0
        for item in list:
            if not item:
                count += 1
        return count

    @staticmethod
    def __merge_lists(lists):
        result = []
        for list in lists:
            result.extend(list)
        return result

"""
df_r = pd.read_json("C:\\Users\\aneta\\Documents\\GitHub\\ankietopol\\ankietopol\\ankiety\\static\\examples\\responses2.json")
print(df_r)
df_p = pd.read_json("C:\\Users\\aneta\\Documents\\GitHub\\ankietopol\\ankietopol\\ankiety\\static\\examples\\items2.json")
print(df_p)
print(StatisticsCalculator.get_basic_measurements(df_p, df_r))
"""