import excel_shopping_tracker
import unittest
from unittest.mock import patch
import datetime
import os
import pathlib
from openpyxl import Workbook, load_workbook

categories = ["groceries", "game", "car related", "baby", "taxi"]
temp_file_path = os.path.join('C:/Users', os.environ['USERPROFILE'], 'AppData/Local/Temp/test_Finances.xlsx')
file_path = str(pathlib.Path().absolute()) + '/tests/test1.xlsx'

class TestApp(unittest.TestCase):

    def test_validate_date(self):
        self.assertEqual(excel_shopping_tracker.validate_date("12/12/2020"), True)
        self.assertEqual(excel_shopping_tracker.validate_date("2021/06/22"), False)
        self.assertEqual(excel_shopping_tracker.validate_date("test"), False)

    def test_ask_question(self):
        # First not allowed input is given, then yes
        with patch('builtins.input') as mocked_input:
            mocked_input.side_effect = ["test", "yes"]
            result = excel_shopping_tracker.ask_question("Would you like to add any rows to Excel?")
            self.assertEqual(result, True)
        
        with patch('builtins.input') as mocked_input:
            mocked_input.side_effect = ["yes"]
            result = excel_shopping_tracker.ask_question("Would you like to add any rows to Excel?")
            self.assertEqual(result, True)
        
        with patch('builtins.input') as mocked_input:
            mocked_input.side_effect = ["no"]
            result = excel_shopping_tracker.ask_question("Would you like to add any rows to Excel?")
            self.assertEqual(result, False)
    
    def test_collect_user_input(self):
        # One row
        with patch('builtins.input') as mocked_input:
            mocked_input.side_effect = ["10/12/2020", "123", "2", "Zelda rules", "no"]
            result = excel_shopping_tracker.collect_user_input(categories)
            self.assertEqual(result, [{'date': '10/12/2020', 'amount': 123, 'category': 'game', 'description': 'Zelda rules'}])
        
        # Wrong formats first
        with patch('builtins.input') as mocked_input:
            mocked_input.side_effect = ["10/13/2020", "2021/12/03", "10/12/2019", "one hundred", "100", "6", "4", "2 packages of diapers", "no"]
            result = excel_shopping_tracker.collect_user_input(categories)
            self.assertEqual(result, [{'date': '10/12/2019', 'amount': 100, 'category': 'baby', 'description': '2 packages of diapers'}])
        
        # Multiple rows
        with patch('builtins.input') as mocked_input:
            mocked_input.side_effect = (
                    "10/01/2021", "100", "3", "fuel", "yes",
                    "12/01/2021", "23", "2", "Mario", "yes",
                    "14/01/2021", "455", "1", "Auchan", "no"
                )
            result = excel_shopping_tracker.collect_user_input(categories)
            self.assertEqual(
                    result,
                    [
                        {'date': '10/01/2021', 'amount': 100, 'category': 'car related', 'description': 'fuel'},
                        {'date': '12/01/2021', 'amount': 23, 'category': 'game', 'description': 'Mario'}, 
                        {'date': '14/01/2021', 'amount': 455, 'category': 'groceries', 'description': 'Auchan'}
                    ]
                )

    def test_create_new_excel(self):       
        excel_shopping_tracker.create_new_excel(temp_file_path)
        assert os.path.isfile(temp_file_path)
        os.remove(temp_file_path)
        
    def setUp(self):
        excel_shopping_tracker.create_new_excel(file_path)
    
    def test_save_new_rows_to_excel(self):
        
        rows = [
            {'date': '01/01/2021', 'amount': 12, 'category': 'regular groceries', 'description': 'test test one'},
            {'date': '01/03/2021', 'amount': 123, 'category': 'regular groceries', 'description': 'test test 2'},
            {'date': '05/01/2021', 'amount': 12, 'category': 'taxi', 'description': 'test test three'},
        ]
        excel_shopping_tracker.save_new_rows_to_excel(rows, file_path)

        # Now verify if the rows were saved
        workbook = load_workbook(file_path)
        sheet = workbook.active
        all_rows = []
        for row in sheet.iter_rows(min_row=2,min_col=1, max_col=4, values_only=True):
            all_rows.append(row)
        self.assertEqual(
                    all_rows,
                    [
                        (datetime.datetime(2021, 1, 1, 0, 0), 12, 'regular groceries', 'test test one'),
                        (datetime.datetime(2021, 3, 1, 0, 0), 123, 'regular groceries', 'test test 2'), 
                        (datetime.datetime(2021, 1, 5, 0, 0), 12, 'taxi', 'test test three')
                    ]
                )
    
    def tearDown(self):
        os.remove(file_path)

if __name__ == '__main__':
    unittest.main()