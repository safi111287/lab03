import unittest

from tvsummary import Show


class TestShow(unittest.TestCase):
    """Test Show using handmade records without network access."""

    def test_valid_record(self):
        record = {
            "name": "Example Show",
            "language": "English",
            "genres": ["Drama", "Comedy"],
            "rating": {"average": 8.5},
            "network": {"name": "Example Network"},
            "premiered": "2015-04-10",
        }

        show = Show(record)

        self.assertEqual(str(show), "Example Show")
        self.assertEqual(show.language, "English")
        self.assertEqual(show.genres, ["Drama", "Comedy"])
        self.assertEqual(show.rating, 8.5)
        self.assertTrue(show.has_network)
        self.assertEqual(show.network_name, "Example Network")
        self.assertEqual(show.premiered, "2015-04-10")
        self.assertEqual(show.year, 2015)

    def test_missing_values(self):
        show = Show({})

        self.assertEqual(show.name, "Unknown")
        self.assertIsNone(show.language)
        self.assertEqual(show.genres, [])
        self.assertIsNone(show.rating)
        self.assertFalse(show.has_network)
        self.assertEqual(show.network_name, "No Network")
        self.assertIsNone(show.premiered)
        self.assertIsNone(show.year)

    def test_malformed_values(self):
        record = {
            "language": 123,
            "genres": "Drama",
            "rating": {"average": "invalid"},
            "network": None,
            "premiered": "unknown",
        }

        show = Show(record)

        self.assertIsNone(show.language)
        self.assertEqual(show.genres, [])
        self.assertIsNone(show.rating)
        self.assertEqual(show.network_name, "No Network")
        self.assertIsNone(show.year)


if __name__ == "__main__":
    unittest.main()
