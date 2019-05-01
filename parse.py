try:
    import gspread
    from oauth2client.service_account import ServiceAccountCredentials
except ImportError as e:
    print('Не найдены необходимые библиотеки (%s)' % e.name)
    exit(500)


class Parser:

    def __init__(self, json_name):
        # init Google API key
        credentials = ServiceAccountCredentials.from_json_keyfile_name(json_name,
                                                                       'https://spreadsheets.google.com/feeds')
        self.gs = gspread.authorize(credentials)
        self.sht = self.gs.open_by_url('https://docs.google.com/spreadsheets/d'
                                       '/1VElk298_tbpeYPsTvHLcFB2Crk6jUWGcCG4vGNvM-Xw').sheet1  # google table url

    def fetch_all_values(self):
        """Возвращает все значения таблицы в столбцах [A-H]
        :returns result: array
        """
        rows = self.sht.row_count
        columns = self.sht.col_count
        result = []
        first_row = [i.value for i in self.sht.range(1, 1, 1, columns)]
        data = self.sht.range(2, 1, rows, columns)
        for each in range(0, len(data), columns):
            pairs = []
            for key in range(8, columns):
                if data[key + each].value != '':
                    pairs.append([first_row[key], data[key + each].value])

            result.append(
                [i.value for i in data[each:each + 8]] + [pairs])

        return result
