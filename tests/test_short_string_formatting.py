import unittest
import datetime
from helpers import format_timedelta_to_short_string


class TestShortStringFormatting(unittest.TestCase):
    def test_only_seconds(self):
        delta = datetime.timedelta(seconds=5)

        self.assertEqual(format_timedelta_to_short_string(delta), "5 sec")

    def test_minutes_and_seconds(self):
        delta = datetime.timedelta(seconds=5, minutes=5)

        self.assertEqual(format_timedelta_to_short_string(delta), "5m5sec")

    def test_full_string(self):
        delta = datetime.timedelta(seconds=5, minutes=5, hours=5)

        self.assertEqual(format_timedelta_to_short_string(delta), "5h5m5s")
