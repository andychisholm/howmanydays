import unittest
from itertools import chain
from datetime import datetime, timedelta

from dates import to_date, get_days_between


class TestDates(unittest.TestCase):
    def test_make_valid_date(self):
        # some basic dates over the expected range
        self.assertIsNotNone(to_date(1, 1, 1901))
        self.assertIsNotNone(to_date(15, 6, 2000))
        self.assertIsNotNone(to_date(31, 12, 2999))

        # leap day on a leap year
        self.assertIsNotNone(to_date(29, 2, 1996))
        self.assertIsNotNone(to_date(29, 2, 2000))

    def test_throw_on_invalid_date(self):
        with self.assertRaises(ValueError):
            to_date(-1, 1, 2000)  # negative day

        with self.assertRaises(ValueError):
            to_date(32, 1, 2000)  # invalid day

        # leap day on a non-leap year
        with self.assertRaises(ValueError):
            to_date(29, 2, 1999)
        with self.assertRaises(ValueError):
            to_date(29, 2, 2100)

        with self.assertRaises(ValueError):
            to_date(1, -1, 2000)  # invalid month

        with self.assertRaises(ValueError):
            to_date(10, 10, 0.1)  # non-integer year

        with self.assertRaises(ValueError):
            to_date(50, 50, 0.50)  # do three wrongs make a right?

    def test_get_days_between_basic(self):
        a = to_date(1, 1, 1111)
        a_plus_1 = to_date(2, 1, 1111)
        b = to_date(2, 2, 2222)

        # no days from self
        self.assertEqual(0, get_days_between(a, a))

        # no days between neighbour dates
        self.assertEqual(0, get_days_between(a, a_plus_1))

        # no days between when 'to' date before 'from' date
        self.assertEqual(0, get_days_between(b, a))

        # otherwise we should have a positive number of days
        self.assertLess(0, get_days_between(a, b))

        # validate cherry picked cases from the spec
        self.assertEqual(19, get_days_between(to_date(2, 6, 1983), to_date(22, 6, 1983)))
        self.assertEqual(173, get_days_between(to_date(4, 7, 1984), to_date(25, 12, 1984)))
        self.assertEqual(1979, get_days_between(to_date(3, 8, 1983), to_date(3, 1, 1989)))

    def test_agreement_with_python_datetime(self):
        # it's fairly easy to compute an offset, so we might as well compare
        # a huge range via brute force to the expected values produced by the python libs
        for start_yr in range(1801, 3101, 3):
            base_dt = datetime(start_yr, 1, 1)
            base_date = to_date(1, 1, start_yr)
            for offset in chain(range(1, 1000), range(1000, 10000, 10)):
                target_dt = base_dt + timedelta(days=offset)
                target_date = to_date(target_dt.day, target_dt.month, target_dt.year)
                self.assertEqual(offset-1, get_days_between(base_date, target_date),
                                 "Failed from {:s} to {:s}".format(str(base_date), str(target_date)))

if __name__ == '__main__':
    unittest.main()
