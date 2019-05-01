# ofp-parser
Парсер таблицы с посещениями ОФП

## В проекте используются библиотеки:
 * <a href="https://github.com/burnash/gspread">Google Spreadsheets Python API</a>
 * sqlite3
 * oauth2client
 
## Запуск
После установки всех необходимых библиотек нужно создать файл авторизации
в Google API. Для этого следуйте иструкциям <a href='https://gspread.readthedocs.io/en/latest/oauth2.html'>здесь</a>.
<br>
После создания файла авторизации необходимо прописать его в файле main.py:
```python
parser = Parser('PATH_TO_AUTH_FILE.json')
``` 
После этого можно запускать парсер. Процесс сбора данных занимает около 10 секунд.