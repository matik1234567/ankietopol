from .DBManager import DBManager
import xlsxwriter
import time
from django.http import HttpResponse
import json

class Export:
    @staticmethod
    def write_xlsx(poll_id):
        responses = DBManager.get_responses(poll_id)
        print(responses.responses)
        #print(json.loads(responses))
        response = HttpResponse(content_type='pplication/ms-excel')
        timestr = time.strftime("%Y%m%d%H%M%S")
        response['Content-Disposition'] = f'attachment; filename="{timestr}.xlsx"'
        workbook = xlsxwriter.Workbook(response)
        worksheet = workbook.add_worksheet()
        worksheet.write(0, 0, 'bbb')
        workbook.close()
        return response

    @staticmethod
    def write_csv(poll_id):
        responses = DBManager.get_responses(poll_id).responses


    @staticmethod
    def write_pdf(poll_id):
        responses = DBManager.get_responses(poll_id).responses



