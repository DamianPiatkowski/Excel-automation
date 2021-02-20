import excel_shopping_tracker
import unittest
from unittest.mock import patch

class TestApp(unittest.TestCase):

    def test_collect_user_input_one_row(self):
        with patch('builtins.print') as mocked_print:
            with patch('builtins.input') as mocked_input:
                mocked_input.side_effect = ("10/12/2020", "123", "2", "Zelda rules", "no")

                result = excel_shopping_tracker.collect_user_input(["groceries", "game"])
                mocked_print.assert_called_with("cool")
                self.assertEqual(result, [{'date': '10/12/2020', 'amount': '123', 'category': 'game', 'description': 'Zelda rules'}])

if __name__ == '__main__':
    unittest.main()