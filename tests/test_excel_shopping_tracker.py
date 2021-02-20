import excel_shopping_tracker
import unittest
from unittest.mock import patch

categories = ["groceries", "game", "car related", "baby", "taxi"]

class TestApp(unittest.TestCase):

    def test_collect_user_input_one_row(self):
        with patch('builtins.print') as mocked_print:
            with patch('builtins.input') as mocked_input:
                mocked_input.side_effect = ("10/12/2020", "123", "2", "Zelda rules", "no")

                result = excel_shopping_tracker.collect_user_input(categories)
                mocked_print.assert_called_with("cool")
                self.assertEqual(result, [{'date': '10/12/2020', 'amount': '123', 'category': 'game', 'description': 'Zelda rules'}])
    
    def test_collect_user_input_wrong_formats_first(self):
        with patch('builtins.print') as mocked_print:
            with patch('builtins.input') as mocked_input:
                mocked_input.side_effect = ("10/13/2020", "2021/12/03", "10/12/2019", "one hundred", "100", "6", "4", "2 packages of diapers", "no")

                result = excel_shopping_tracker.collect_user_input(categories)
                mocked_print.assert_called_with("cool")
                self.assertEqual(result, [{'date': '10/12/2019', 'amount': '100', 'category': 'baby', 'description': '2 packages of diapers'}])

    def test_collect_user_input_multiple_rows(self):
        with patch('builtins.print') as mocked_print:
            with patch('builtins.input') as mocked_input:
                mocked_input.side_effect = (
                    "10/01/2021", "100", "3", "fuel", "yes",
                    "12/01/2021", "23", "2", "Mario", "yes",
                    "14/01/2021", "455", "1", "Auchan", "no"
                )

                result = excel_shopping_tracker.collect_user_input(categories)
                mocked_print.assert_called_with("cool")
                self.assertEqual(
                    result,
                    [
                        {'date': '10/01/2021', 'amount': '100', 'category': 'car related', 'description': 'fuel'},
                        {'date': '12/01/2021', 'amount': '23', 'category': 'game', 'description': 'Mario'}, 
                        {'date': '14/01/2021', 'amount': '455', 'category': 'groceries', 'description': 'Auchan'}
                    ]
                )

if __name__ == '__main__':
    unittest.main()