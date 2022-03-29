from ankiety.models import Form
from django.test import TestCase
from django.contrib.auth.models import User
from essential_generators import DocumentGenerator
import random
from ankiety.static.py import DataCleaner

"""class FactoryDatabase(TestCase):
    def setUp(self):
        self.rows_count = 4
        # User.objects.create(id_user="1",name="admin", email="example@example.com", password="fdsfsfd", created_at="22-05-2022")

    def test_factory(self):
        user = User.objects.get(pk=1)
        for c in range(0, self.rows_count):
            Form.objects.create(id_form=c+1, owner=user,close_condition='C',close_value='200',is_closed=False, title="sdasdsa",description="fff", items="{item:[{'id':0}]}")


class TestMainDB:

    @staticmethod
    def clear():
        Form.objects.all().delete()


    @staticmethod
    def run():
        user = User.objects.get(pk=1)  # admin user
        for i in range(0, 5):
            s = DocumentGenerator()
            Form.objects.create(owner=user,
                                close_condition='C',
                                close_value='200',
                                is_closed=False,
                                title=s.word(),
                                description=s.sentence() + s.sentence() + s.sentence(),
                                items=TestMainDB.form_gen()
                                )

    @staticmethod
    def form_gen():
        num_of_items = random.randint(1, 16)
        s = DocumentGenerator()
        types = ['C', 'T', 'R', 'S', 'N']
        req = ['T', 'F']
        j = "["
        for i in range(0, num_of_items):
            type = types[random.randint(0, len(types)-1)]
            j += "{" + f'"id":"{i}", "type":"{type}", "description":"{s.sentence()}", "value":"{TestMainDB.value_gen(type)}", "name": "{s.word()}", "is_req":"{req[random.randint(0, 1)]}"' + "}"
            if i != num_of_items-1:
                j += ","
        j += ']'
        return j


    @staticmethod
    def value_gen(type):
        s = DocumentGenerator()
        if type != 'T' and not type == 'N':
            num_of_items = random.randint(2, 8)
            arr = []
            for n in range(0, num_of_items):
                arr.append(s.sentence())
            return arr
        elif type == 'N':
            down = random.randint(0, 8)
            up = random.randint(50, 100)
            return [down, up]
        else:
            return s.sentence()"""

class DataCleanerTests(TestCase):

    dataCleaner = DataCleaner.DataCleaner()

    def remove_spaces_test(self):
        in_text = "he    ll    o!!"
        ou_text = self.dataCleaner.removeMultipleSpaces(in_text)
        self.assertEqual(ou_text, "he ll o!!")

    def remove_newlines_test(self):
        in_text = """hey
        hi
        hello"""
        ou_text = self.dataCleaner.removeNewLines(in_text)
        self.assertEqual(ou_text, "heyhihello")