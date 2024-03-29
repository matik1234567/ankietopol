import pandas as pd
import statistics
from statistics import mode
import json
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats
from sklearn.feature_selection import chi2
from scipy.stats import pointbiserialr

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
                    stats.append({'data': StatisticsCalculator.__get_response_hist(responses[question['name']]),
                                  'title': question['title'],
                                  'questions': question['questions'],
                                  'measures': StatisticsCalculator.__get_measures_categorical(responses[question['name']]),
                                  'type': question['type'],
                                  'name':question['name']})
                case 'c':
                    stats.append(
                        {'data': StatisticsCalculator.__get_response_hist(responses[question['name']]),
                         'title': question['title'],
                         'questions': question['questions'],
                         'measures': StatisticsCalculator.__get_measures_categorical(responses[question['name']]),
                         'type': question['type'],
                         'name': question['name']})
                case 'n':
                    stats.append(
                        {'data': StatisticsCalculator.__get_responses_hist_numeric(responses[question['name']]),
                         'title': question['title'],
                         'questions': question['questions'],
                         'measures': StatisticsCalculator.__get_measures_continuous(responses[question['name']]),
                         'type': question['type'],
                         'name': question['name']})
                case 's':
                    stats.append(
                        {'data': StatisticsCalculator.__get_responses_hist_numeric(responses[question['name']]),
                         'title': question['title'],
                         'questions': question['questions'],
                         'measures': StatisticsCalculator.__get_measures_continuous(responses[question['name']]),
                         'type': question['type'],
                         'name': question['name']})
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

        data = data.dropna()
        data = data.explode()

        dict_of_freq = {}
        for v in data.unique():
            dict_of_freq[str(v)] = 0
        for item in data.tolist():
            dict_of_freq[str(item)] += 1  # +1 to the number of occurences of this question

        return [[str(int(float(key))), value] for key, value in dict_of_freq.items()]

    @staticmethod
    def __get_responses_hist_numeric(data):
        data = data.dropna()
        data = data.explode()
        d = []
        for dd in data:
            if dd == '':
                continue
            d.append(int(dd))
        n, bins, patches = plt.hist(d)
        print(n)
        print(bins)
        #print(patches)

        res = [[str(round(bins[i], 1)), n[i]] for i in range(len(n))]
        for r in range(len(res)):
            if r<len(res)-1:
                res[r][0]+=(" - "+res[r+1][0])
        res[-1][0]+=(" - "+str(bins[-1]))

        return res

    @staticmethod
    def __get_measures_continuous(list): # get measures for continuous variables

        list_temp = []
        for l in list:
            if l != '':
                list_temp.append(float(l))

        list = pd.Series(list_temp)
        result = {}
        result['Total question answers'] = len(list)
        list = list.dropna()
        result['Empty question answers'] = result['Total question answers'] - len(list)
        list = list.explode()
        list = list.astype(float)
        result["Mean"] = round(statistics.mean(list),2)
        result["Mode"] = mode(list)
        result["Std Dev"] = round(np.std(list),2)
        result["Q1"] = list.quantile(0.25)
        result["Q3"] = list.quantile(0.75)

        return result

    @staticmethod
    def __get_measures_categorical(list):  # get measures for continuous variables

        result = {}
        result['Total question answers'] = len(list)
        list = list.dropna()
        result['Empty question answers'] = result['Total question answers'] - len(list)
        list = list.explode()
        list = list.astype(float)
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

    @staticmethod
    def __merge_lists(lists):
        result = []
        for list in lists:
            result.append(list)
        return result

    @staticmethod
    def get_correlation(poll, responses, var1_id, var2_id):
        var1_vals = responses[poll["name"][var1_id]]
        var2_vals = responses[poll["name"][var2_id]]

        var1_vals = var1_vals.astype(int)
        var2_vals = var2_vals.astype(int)

        description = ["Correlation"]

        if StatisticsCalculator.__get_variable_type(poll["type"][var1_id]) == StatisticsCalculator.__get_variable_type(poll["type"][var2_id]):
            # variable types are the same

            if StatisticsCalculator.__get_variable_type(poll["type"][var1_id]) == "continuous":
                corr_coe, p_value = scipy.stats.pearsonr(var1_vals, var2_vals)
                description.append("Method used: Pearson Correlation")
                description.append("Correlation coefficient = " +str(round(corr_coe, 2)))
                description.append("The Pearson's correlation coefficient varies between -1 and +1 with 0 implying no correlation. Correlations of -1 or +1 imply an exact linear relationship.")
            else:
                description.append("Method used: Chi Square")
                vals = [var1_vals, var2_vals]
                chi2_val, p_val, dof, other = scipy.stats.chi2_contingency(vals) # dof = degree of freedom
                description.append("Chi2 = "+str(round(chi2_val,2)))
                alpha = 0.05
                critical_value = scipy.stats.chi2.ppf(q = 1-alpha, df = dof)
                description.append("Chi2 critical value for p=0.05 is "+str(round(critical_value,2)))
                if chi2_val<critical_value:
                    description.append(" - the variables are not correlated.")
                else:
                    description.append(" - the variables are correlated.")
        else:
            # there is one categorical and one continuous variable

            description.append("method used: Point Biserial Correlation")
            corr, p_val = pointbiserialr(var1_vals, var2_vals)
            description.append("correlation = "+str(round(corr, 2))+"; p = "+str(round(p_val, 2)))
        return description

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

'''
df_r = pd.read_json("C:\\Users\\aneta\\Documents\\GitHub\\ankietopol\\ankietopol\\ankiety\\static\\examples\\responses3.json")
print(df_r)
df_p = pd.read_json("C:\\Users\\aneta\\Documents\\GitHub\\ankietopol\\ankietopol\\ankiety\\static\\examples\\items3.json")
print(df_p)
#print(StatisticsCalculator.get_basic_measurements(df_p, df_r))
print(StatisticsCalculator.get_correlation(df_p, df_r, 0, 0))
'''

