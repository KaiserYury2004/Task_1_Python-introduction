import unittest
from Task_1 import MyDatabase
##Здесь идет подключение именно к базе данных postgres,
#поэтому здесь будут выброшены ошибки по причине отсутствия на локальной машине данного сервера!
class TestMyDatabase(unittest.TestCase):
    def setUp(self):
        self.db = MyDatabase(server='postgres',port=5432, database="test", username="sa", password="18011871")
    def tearDown(self):
        self.db.close()
    def test_connection(self):
        self.assertIsNotNone(self.db.conn)
    def test_create_tables(self):
        self.db.create_tables()
    def test_load_data_from_json(self):
        rooms_file = "test_rooms.json"
        students_file = "test_students.json"
        result = self.db.load_data_from_json(rooms_file, students_file)
        self.assertEqual(result, 0)
    def test_query_processing(self):
        input_file = "SQLQuery2.sql"
        expected_result = "expected_result.json"
        self.db.query_processing(input_file, "test_result.json")
        with open("test_result.json", "r") as f1, open(expected_result, "r") as f2:
            self.assertEqual(f1.read(), f2.read())
if __name__ == '__main__':
    unittest.main()
