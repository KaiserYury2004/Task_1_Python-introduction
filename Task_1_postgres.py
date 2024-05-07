import pyodbc
import json
import logging 
from lxml import etree
import os
import psycopg2
import configparser
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
class MyDatabase:
    #Здесь ищу сервер
    def __init__(self, port ,server, database, username, password):
            self.port=port
            self.server =server
            self.database = database
            self.username = username
            self.password = password
            try:
                self.cursor, self.connection = self.connect()
                print('cursor were created')
            except:
                logger.critical("Ошибка при подключении к серверу базы данных")
    #Здесь конекчусь
    def connect(self):
        try:
            #conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.server};DATABASE={self.database};PORT={self.port};UID={self.username};PWD={self.password};'
            #conn = pyodbc.connect(conn_str)
            connection = psycopg2.connect(
            host='postgres',
            database='test',
            user='sa',
            password=18011871,
            port=5432
            )
            logger.info("Успешное подключение к базе данных")
            cursor = connection.cursor()
            return cursor, connection
        except Exception as e:
            global connected
            connected=False
            logger.critical(f"Ошибка при подключении к базе данных: {e}")
        return None
    
    #Здесь создаю при необходимости таблицу
    def create_tables(self):
        cursor = self.cursor
        cursor.execute("SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'rooms'")
        if cursor.fetchone()[0] == 0:
             cursor.execute('''CREATE TABLE rooms
                        (id INT PRIMARY KEY,
                        name VARCHAR(255))''')
        else:
            logger.info('Таблица "rooms" уже существует!')
        cursor.execute("SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'students'")
        if cursor.fetchone()[0] == 0:
            cursor.execute('''CREATE TABLE students
                        (id INT PRIMARY KEY,
                        name VARCHAR(255),
                        birthday timestamp,
                        room INT,
                        sex CHAR(1),
                        FOREIGN KEY(room) REFERENCES rooms(id))''')
            logger.info('Таблица Students создана!')
        else:
            print('Таблицы "Students" already exists!')
        self.connection.commit()

    
    #Здесь выгружается инфа из файлов!     
    def load_data_from_json(self, rooms_file, students_file)->int:
        check_wrong_ways=0
        if not os.path.isfile(rooms_file):
            logger.error(f"Файл '{rooms_file}' не найден.")
            check_wrong_ways=1
        if not os.path.isfile(students_file):
            logger.error(f"Файл '{students_file}' не найден.")
            check_wrong_ways=1
        if check_wrong_ways == 1:
            return check_wrong_ways
        cursor = self.cursor
        try:
            with open(rooms_file, 'r') as file:
                rooms_data = json.load(file)
                for room in rooms_data:
                    query = "INSERT INTO rooms (id, name) VALUES (%s, '%s')" % (room['id'], room['name'])
                    cursor.execute(query)
                logger.info('Данные по комнатам занесены!')

            with open(students_file, 'r') as file:
                students_data = json.load(file)
                for student in students_data:
                    birthday = student['birthday'][:10]
                    cursor.execute("INSERT INTO Students (id, name, birthday, room, sex) VALUES (%s, '%s', '%s', '%s', '%s')" % (student['id'], student['name'], birthday, student['room'], student['sex']))
                logger.info('Данные по студентам занесены!')
        except pyodbc.Error as e:
            logger.critical(f"Ошибка при заносе данных в базу данных: {e}")
        self.connection.commit()
    

    def execute_sql_query_json(self,input_file,output_file):
        cursor = self.connect()
        with open(input_file, 'r') as f:
            queries = f.read()
        with open(output_file, 'w') as f:
                try:
                    cursor.execute(queries)
                    rows = cursor.fetchall()
                    f.write(f"Result of {input_file}: \n")
                    for row in rows:
                        f.write(str(row) + '\n')
                except pyodbc.Error as e:
                    logger.critical(f"Ошибка выполнения запроса: {output_file}\n{e}\n\n")

    def query_processing(self, input_file, output_file):
        try:
            with open(input_file, 'r') as f:
                sql_query = f.read()
            cursor = self.connect()
            cursor.execute(sql_query)
            columns = [column[0] for column in cursor.description]
            rows = cursor.fetchall()
            if columns and rows:
                xml_data = self.convert_result_to_xml(columns, rows)
                self.save_xml_to_file(xml_data, output_file)
                logger.info('Создан файл '+output_file)
            else:
                logger.critical("Не удалось выполнить запрос или получить результаты.")
        except pyodbc.Error as e:
            print(f"Ошибка при выполнении SQL запроса: {e}")

    def convert_result_to_xml(self, columns, rows):
        root = etree.Element('data')
        for row in rows:
            record = etree.Element('record')
            for column, value in zip(columns, row):
                if column:
                    field = etree.Element(column)
                    field.text = str(value)
                    record.append(field)
            root.append(record)
        return root

    def save_xml_to_file(self, xml_data, xml_filename):
        xml_tree = etree.ElementTree(xml_data)
        xml_tree.write(xml_filename, pretty_print=True)

    def close(self):
         logger.info("Programm is finished!")
         self.connection.close()
         self.cursor.close()
         




if __name__ == "__main__":
    # print('Введите имя сервера')
    # server=input()
    # print('Введите имя базы данных')
    # database=input()
    # print('Введите имя пользователя')
    # username=input()
    # print('Введите имя пользователя')
    # password=input()
    config = configparser.ConfigParser()
    config.read("config.ini")
    port=config.get('Task_1','Port')
    server = config.get('Task_1','Server')
    database = config.get('Task_1','Database')
    username = config.get('Task_1','Username')
    password = config.get('Task_1','Password')
    db = MyDatabase(port,server, database, username, password)
    if(connected is False):
        print('Программа завершена!')
        os.abort()
    print('Вводились ли ранее файлы rooms.json и students.json?\nPrint(Y/n)')
    enter='Y'
    while True:
        if(enter=='Y'):
            break
        elif(enter=='n'):
            db.create_tables()
            print('Введите полный путь до файла rooms.json')
            rooms_way='./rooms.json'
            print('Введите путь до файла students.json')
            students_way='./students.json'
            while db.load_data_from_json(rooms_way,students_way) == 1:
                print('Введите корректный путь до файла rooms.json')
                rooms_way='./rooms.json'
                print('Введите корректный путь до файла students.json')
                students_way='./students.json'
                db.load_data_from_json(rooms_way,students_way)
            break
        print('Введите один из предложенных вариантов')
    print('Выберите формат выходного файла:json или xml')
    form='json'
    while True:
        if form.find('json')!=-1:
            form='json'
            db.execute_sql_query_json('SQLQuery1.sql','SQLQuery1_result.'+str(form))
            db.execute_sql_query_json('SQLQuery2.sql','SQLQuery2_result.'+str(form))
            db.execute_sql_query_json('SQLQuery3.sql','SQLQuery3_result.'+str(form))
            db.execute_sql_query_json('SQLQuery4.sql','SQLQuery4_result.'+str(form))
            break
        elif form.find('xml')!=-1:
            form='xml'
            db.query_processing('SQLQuery1.sql', 'SQLQuery1_result.'+str(form))
            db.query_processing('SQLQuery2.sql','SQLQuery2_result.'+str(form))
            db.query_processing('SQLQuery3.sql','SQLQuery3_result.'+str(form))
            db.query_processing('SQLQuery4.sql','SQLQuery4_result.'+str(form))
            break
        print('Введите один из двух предложенных форматов!')
        form='json'
    db.close()
