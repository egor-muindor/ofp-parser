try:
    from parse import Parser
    from db_controller import DatabaseController
    import os
except ImportError as e:
    print('Не найдены необходимые библиотеки (%s)' % e.name)
    exit(500)
except Exception as e:
    print('Неизвестная ошибка. \n', e)

if __name__ == '__main__':
    path_to_db = '/home/muindor/projects/ofp-parser/'  # Полный путь к файлу БД
    temp_name = os.path.join(path_to_db, 'temp.db')  # Временный файл БД (создается при заполнении БД)
    name_db = os.path.join(path_to_db, 'my.db')  # Финальный файл БД
    parser = Parser('PATH_TO_AUTH_FILE.json')  # Путь к вашему файлу авторизации
    data = parser.fetch_all_values()
    db = DatabaseController(temp_name)
    db.insert_from_data(data)
    if db.exit():
        try:
            os.remove(name_db)
            os.rename(temp_name, name_db)
        except FileNotFoundError as e:
            os.rename(temp_name, name_db)
