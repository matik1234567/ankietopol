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
                                  'questions': question['questions'],
                                  'measures': StatisticsCalculator.__get_measures_categorical(responses[question['name']]),
                                  'type': question['type']})
                case 'c':
                    df = pd.DataFrame(StatisticsCalculator.__merge_lists(responses[question['name']].dropna()))
                    #print(responses[question['name']].values.tolist())
                    stats.append(
                        {'data': StatisticsCalculator.__get_response_hist(df[0]),
                         'title': question['title'],
                         'questions': question['questions'],
                         'measures': StatisticsCalculator.__get_measures_categorical(StatisticsCalculator.__merge_lists(
                             responses[question['name']])),
                         'type': question['type']})
                case 'n':
                    a = 1
                    #stats[question.id] = StatisticsCalculator.__get_measures_continuous(responses[question.id])
                case 's':
                    a=2
                    #stats[question.id] = StatisticsCalculator.__get_measures_continuous(responses[question.id])
                case 't':

                    nothing = 0 # TODO: string length distribution??
        return stats

    ''''@staticmethod
    def __get_response_distribution(values, list):
        freq = [0] * len(values)
        for item in list:
            freq[item - 1] += 1  # +1 to the number of occurences of this answer
        return [values, freq]'''

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
        print(list)
        result = {}
        result['Total poll answers'] = len(list)
        list = list.dropna()
        result['Empty poll answers'] = result['Total poll answers'] - len(list)
        result["Average"] = statistics.mean(list)
        result["Mode"] = mode(list)
        result["StdDev"] = statistics.stdev(list)
        result["Q1"] = list.quantile(0.25)
        result["Q3"] = list.quantile(0.75)
        return result

    @staticmethod
    def __get_measures_categorical(list):  # get measures for continuous variables
        result = {}
        result['Total poll answers'] = len(list)
        list = list.dropna()
        result['Empty poll answers'] = result['Total poll answers'] - len(list)
        result["Mode"] = mode(list)
        result["Q1"] = list.quantile(0.25)
        result["Q3"] = list.quantile(0.75)
        return result

    '''@staticmethod
    def __count_empty(list):
        count = 0
        for item in list:
            if not item:
                count += 1
        return count'''

    ''''@staticmethod
    def __merge_lists(lists):
        result = []
        for list in lists:
<<<<<<< Updated upstream
            if list is list:
                result.extend(list)
            else:
                result.append(list)
=======
            result.extend(list)
        return result'''

    @staticmethod
    def __expand_lists_in_df(df):
        result = []
        for list in lists:
            result.extend(list)
>>>>>>> Stashed changes
        return result

    @staticmethod
    def get_correlation(poll, responses, var1_id, var2_id):
        var1_vals = responses[var1_id]
        var2_vals = responses[var2_id]

        # TODO - check what kind of variables, calculate correlation
        if StatisticsCalculator.__get_variable_type(poll["type"][var1_id]) == StatisticsCalculator.__get_variable_type(poll["type"][var2_id]):
            nothing = 0
            # variable types are the same
            description = "method used: ..., if index>1 corelation exists ..."
            index = 0.5
        else:
            nothing = 0
            # there is one categorical and one continuous variable
            description = "method used: ..., if index>1 corelation exists ..."
            index = 0.5
        return description, index

    @staticmethod
    def __get_variable_type(field_type):
        match field_type:
            case 'r':
                return "categorical"
            case 'c':
                return "categorical"
            case 'n':
                return "continuous"
            case 's':
                return "continuous"

"""
df_r = pd.read_json("C:\\Users\\aneta\\Documents\\GitHub\\ankietopol\\ankietopol\\ankiety\\static\\examples\\responses2.json")
print(df_r)
df_p = pd.read_json("C:\\Users\\aneta\\Documents\\GitHub\\ankietopol\\ankietopol\\ankiety\\static\\examples\\items2.json")
print(df_p)
print(StatisticsCalculator.get_basic_measurements(df_p, df_r))
print(get_correlation(df_p, df_r, 0, 2))
"""