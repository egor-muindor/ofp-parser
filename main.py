try:
    from parse import Parser
    from db_controller import DatabaseController
except ImportError as e:
    print('Не найдены необходимые библиотеки (%s)' % e.name)
    exit(500)
except Exception as e:
    print('Неизвестная ошибка. \n', e)

if __name__ == '__main__':
    db = DatabaseController('my.db')  # Название файла sqlite базы данных
    parser = Parser('PATH_TO_AUTH_FILE.json')  # Путь к вашему файлу авторизации
    data = parser.fetch_all_values()
    db.insert_from_data(data)
    db.exit()
