try:
    import datetime
    import sqlite3
    from parse import Parser
except ImportError as e:
    print('Не найдены необходимые библиотеки (%s)' % e.name)
    exit(500)


class DatabaseController:

    def __init__(self, db_name):
        self.db_name = db_name
        self.connect = sqlite3.connect(db_name)
        self.__setup_db__()

    def __setup_db__(self):
        """ Делает сброс БД, кроме таблицы info """
        c = self.connect.cursor()
        c.execute('PRAGMA foreign_keys = ON;')
        c.execute('DROP TABLE IF EXISTS students;')
        c.execute('DROP TABLE IF EXISTS teachers;')
        c.execute('DROP TABLE IF EXISTS faculties;')
        c.execute('DROP TABLE IF EXISTS groups;')
        c.execute('DROP TABLE IF EXISTS pairs;')
        c.execute('DROP INDEX IF EXISTS students_index;')
        c.execute('DROP INDEX IF EXISTS pairs_index;')
        self.connect.commit()
        c.execute(
            '''
            CREATE TABLE IF NOT EXISTS info (
                name STRING (30)   NOT NULL UNIQUE,
                status STRING (45) NOT NULL
            );'''
        )
        c.execute(
            '''
            CREATE TABLE IF NOT EXISTS groups (
                id   INTEGER      PRIMARY KEY AUTOINCREMENT NOT NULL 
                                  NOT NULL,
                name STRING (15)  NOT NULL
            );'''
        )
        c.execute('''
            CREATE TABLE IF NOT EXISTS teachers (
                id   INTEGER      PRIMARY KEY AUTOINCREMENT NOT NULL 
                                  NOT NULL,
                name STRING (175) NOT NULL
            );''')
        c.execute('''
                CREATE TABLE IF NOT EXISTS faculties (
                    id   INTEGER      PRIMARY KEY AUTOINCREMENT NOT NULL 
                                      NOT NULL,
                    name STRING (100) NOT NULL
                    );''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id          INTEGER      PRIMARY KEY AUTOINCREMENT NOT NULL 
                                         NOT NULL,
                name        STRING (175) NOT NULL,
                mark        STRING (45)  NOT NULL,
                course      INTEGER      NOT NULL,
                group_type  STRING (15)  NOT NULL,
                number_cls  INTEGER      NOT NULL,
                
                group_id    INTEGER      REFERENCES groups (id) ON DELETE CASCADE
                                         NOT NULL,
                teacher_id  INTEGER      REFERENCES teachers (id) ON DELETE CASCADE
                                         NOT NULL,
                faculty_id  INTEGER      REFERENCES faculties (id) ON DELETE CASCADE
                                         NOT NULL
            );''')
        c.execute('''
                    CREATE TABLE IF NOT EXISTS pairs (
                        id          INTEGER      PRIMARY KEY AUTOINCREMENT NOT NULL 
                                                 NOT NULL,
                        name        STRING (175) NOT NULL,
                        date        STRING (45)  ,
                        student_id  INTEGER      REFERENCES students (id) ON DELETE CASCADE
                                                 NOT NULL
                    );''')
        c.execute('''
        CREATE INDEX IF NOT EXISTS students_index ON students (
            name ASC,
            id ASC,
            course ASC,
            group_id ASC
        );''')
        c.execute('''
            CREATE INDEX IF NOT EXISTS pairs_index ON pairs (
                student_id ASC,
                id ASC
        );''')
        self.insert_teacher('Отсутствует')
        self.insert_faculty('Отсутствует')
        self.connect.commit()
        c.close()

    def insert_group(self, group):
        """ Вносит данные в таблицу groups
        :param group: Название группы.
        :type group: str

        :returns id: int внесенной записи"""
        c = self.connect.cursor()
        c.execute('''
            INSERT INTO groups (name) VALUES (?);
        ''', (group,))
        c.execute('SELECT id, name FROM groups where name=?', (group,))
        return c.fetchone()[0]

    def find_or_new_group(self, group):
        """ Возвращает id преподавателя, если не находит - создает нового
        :param group: Название группы.
        :type group: str

        :returns id: int внесенной записи
        """
        c = self.connect.cursor()
        c.execute("SELECT id, name from groups where name=?", (group,))
        result = c.fetchone()
        if not result:
            return self.insert_group(group)
        else:
            return result[0]

    def insert_teacher(self, teacher):
        """ Вносит данные в таблицу teachers
        :param teacher: ФИО преподавателя.
        :type teacher: str

        :returns id: int внесенной записи"""
        c = self.connect.cursor()
        c.execute('''
                    INSERT INTO teachers (name) VALUES (?);
                ''', (teacher,))
        c.execute('SELECT id, name FROM teachers WHERE name=?', (teacher,))
        return c.fetchone()[0]

    def find_or_new_teacher(self, name):
        """ Возвращает id преподавателя, если не находит - создает нового
        :param name: ФИО преподавателя.
        :type name: str

        :returns id: int внесенной записи
        """
        c = self.connect.cursor()
        c.execute("SELECT id, name from teachers where name=?", (name,))
        result = c.fetchone()
        if not result:
            return self.insert_teacher(name)
        else:
            return result[0]

    def insert_faculty(self, faculty):
        """ Вносит данные в таблицу faculties
        :param faculty: Название факультета.
        :type faculty: str

        :returns id: int внесенной записи"""
        c = self.connect.cursor()
        c.execute('''
                    INSERT INTO faculties (name) VALUES (?);
                ''', (faculty,))
        c.execute('SELECT id, name FROM faculties WHERE name=?', (faculty,))
        return c.fetchone()[0]

    def find_or_new_faculty(self, faculty):
        """ Возвращает id преподавателя, если не находит - создает нового
        Вносит данные в таблицу faculties
        :param faculty: Название факультета.
        :type faculty: str

        :returns id: int внесенной записи
        """
        c = self.connect.cursor()
        c.execute("SELECT id, name from faculties where name=?", (faculty,))
        result = c.fetchone()
        if not result:
            return self.insert_faculty(faculty)
        else:
            return result[0]

    def insert_student(self, student):
        """ Вносит данные в таблицу students
        :param student: Кортеж для таблицы students.
        :type student: tuple"""
        c = self.connect.cursor()
        c.execute('''
                    INSERT INTO students (
                      name,
                      group_id,
                      course,
                      faculty_id,
                      teacher_id,
                      mark,
                      group_type,
                      number_cls
                  )
                  VALUES (?,?,?,?,?,?,?,?);
                ''', student)
        c.execute('SELECT id, name, group_id FROM students WHERE name=? and group_id=?', (student[0], student[1],))
        return c.fetchone()[0]

    def insert_pairs(self, pairs):
        """ Вносит данные в таблицу students
        :param pairs: Массив с кортежами для таблицы pairs.
        :type pairs: list"""
        c = self.connect.cursor()
        c.executemany('''
                    INSERT INTO pairs (
                      date,
                      name,
                      student_id
                  )
                  VALUES (?,?,?);
                ''', pairs)

    def update_info(self, name, status):
        """ Вносит или обновляет информацию в системной таблице info """
        c = self.connect.cursor()
        c.execute('''
            INSERT OR REPLACE INTO info VALUES (?, ?) ;
        ''', (name, status,))

    def find_teacher(self, name):
        """ Возвращает id преподавателя, если не найден - вернет False """
        c = self.connect.cursor()
        c.execute("SELECT id, name from teachers where name LIKE ? LIMIT 30", ("%{}%".format(name.title()),))
        result = c.fetchall()
        if not result:
            return False
        else:
            return result

    def exit(self):
        """ Необходимо выполнить после завершения действий с БД """
        try:
            self.update_info('update_date', '%s' % datetime.date.today())
            self.connect.commit()
            self.connect.close()
            print('Finish')
            return True
        except():
            return False

    def insert_from_data(self, data):
        """Вносит значения в БД из парсера"""

        for each in data:
            if each[0] == '' or each[1] == '':
                continue
            try:
                each[1] = self.find_or_new_group(each[1])
                each[2] = -1 if each[2] == '' else int(each[2])
                each[3] = 1 if each[3] == '' else self.find_or_new_faculty(each[3])
                each[4] = 1 if each[4] == '' else self.find_or_new_teacher(each[4])
                each[5] = 'Отсутствует' if each[5] == '' else each[5]
                each[6] = 'Отсутствует' if each[6] == '' else each[6]
                each[7] = -1 if each[7] == '' else int(each[7])
                id = self.insert_student(tuple(each[:8]))
                if each[7] > 0:
                    pairs = [tuple(i + [id]) for i in each[8]]
                    self.insert_pairs(pairs)

            except Exception as e:
                print(e, each[0])
