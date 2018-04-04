import unittest

from test.util import capture_output
from cli import main, parse_date_string


class TestCLI(unittest.TestCase):
    def test_parse_date(self):
        self.assertIsNotNone(parse_date_string("01/01/2000"))
        with self.assertRaises(ValueError):
            parse_date_string("1/01")
        with self.assertRaises(ValueError):
            parse_date_string("32/1/2018")
        with self.assertRaises(ValueError):
            parse_date_string("foo bar")

    def test_main(self):
        # integration tests
        with capture_output(main, ["02/06/1983", "22/06/1983"]) as output:
            self.assertEqual("19", output.strip())

if __name__ == '__main__':
    unittest.main()
