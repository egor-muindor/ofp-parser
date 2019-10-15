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
        self.sht = self.gs.open_by_url('https://docs.google.com/spreadsheets'
                                       '/d/1Hx90XZAl1wluJ7loDmMm_a3P8BpPtAKBM1oqnRygtAc').sheet1  # google table url

        self.sht2 = self.gs.open_by_url('https://docs.google.com/spreadsheets'
                                        '/d/1Hx90XZAl1wluJ7loDmMm_a3P8BpPtAKBM1oqnRygtAc').get_worksheet(1)
        # google table url

    def fetch_all_values(self):
        """Возвращает все значения таблицы
        :returns result: list
        """
        rows = self.sht.row_count
        columns = self.sht.col_count
        result = []
        data = self.sht.range(1, 1, rows, columns)
        first_row = [i.value for i in data[0:columns]]
        for each in range(columns, len(data), columns):
            pairs = []
            for key in range(9, columns):
                if data[key + each].value != '':
                    pairs.append([first_row[key], data[key + each].value])

            result.append(
                [i.value for i in data[each:each + 9]] + [pairs])

        return result

    def fetch_all_standards(self):
        """Возвращает все значения 2ого листа
        :returns result: list
        """
        sht2_rows = self.sht2.row_count
        sht2_columns = self.sht2.col_count
        sht2_result = []
        data = self.sht2.range(2, 1, sht2_rows, sht2_columns)
        for each in range(0, len(data), sht2_columns):
            if data[each] == '':
                break
            standards = []
            for key in range(6, sht2_columns, 4):
                if data[key + each].value != '':
                    standards.append([data[key + each + i].value for i in range(4)])
                else:
                    break

            sht2_result.append(
                [i.value for i in data[each:each + 6]] + [standards])

        return sht2_result
