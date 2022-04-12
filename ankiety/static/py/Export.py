from DBManager import DBManager
import xlsxwriter

class Export:
    @staticmethod
    def write_xlsx(poll_id):
        responses = DBManager.get_responses(poll_id).responses
        print(responses)

    @staticmethod
    def write_csv(poll_id):
        responses = DBManager.get_responses(poll_id).responses


    @staticmethod
    def write_pdf(poll_id):
        responses = DBManager.get_responses(poll_id).responses



