from .DBManager import DBManager
from .Parser import Parser
import xlsxwriter
import time
from django.http import HttpResponse
import json
import pandas as pd

class Export:

    @staticmethod
    def __generate_filename():
        return 'AnkietoPoll'+time.strftime("%Y%m%d%H%M%S")

    @staticmethod
    def __collect_data(poll_id):
        return []

    @staticmethod
    def write_xlsx(poll_id):
        dataframe = Parser.responses_to_dataframe(poll_id)

        response = HttpResponse(content_type='pplication/ms-excel')
        response['Content-Disposition'] = f'attachment; filename="{Export.__generate_filename()}.xlsx"'
        workbook = xlsxwriter.Workbook(response)
        worksheet = workbook.add_worksheet()
        col = 0
        for name, values in dataframe.iteritems():
            worksheet.write(0, col, name)
            col += 1

        for d in range(0, len(dataframe)):
            col = 0
            for column in dataframe:
                if type(dataframe[column][d]) is list:
                    st = ""
                    for e in dataframe[column][d]:
                        st += str(e)+";"
                    st = st[:-1]
                    worksheet.write(d + 1, col, st)
                else:
                    worksheet.write(d+1, col, str(dataframe[column][d]))
                col += 1

        workbook.close()
        return response

    @staticmethod
    def write_csv(poll_id):
        response = HttpResponse(content_type='pplication/ms-excel')
        response['Content-Disposition'] = f'attachment; filename="{Export.__generate_filename()}.csv"'
        dataframe = Parser.responses_to_dataframe(poll_id)
        dataframe.to_csv(response)
        return response


    @staticmethod
    def write_pdf(poll_id):
        responses = DBManager.get_responses(poll_id).responses



