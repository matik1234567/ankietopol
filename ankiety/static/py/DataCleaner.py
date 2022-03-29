import re

class DataCleaner:
    def removeMultipleSpaces(self, input):
        output = re.sub(r'\s{2,}', ' ', input)
        return output
    def removeNewLines(self, input):
        output = re.sub(r'\n', '', input)
        return output