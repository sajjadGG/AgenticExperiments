import unittest
from main import to_snake_slug
class TestSnakeSlug(unittest.TestCase):
    """
    Test suite for the to_snake_slug function.
    """

    def test_simple_case(self):
        """Tests a standard 'Title Case' input."""
        self.assertEqual(
            to_snake_slug('Ten of Pentacles'), 
            'ten_of_pentacles'
        )

    def test_apostrophe(self):
        """Tests that apostrophes are correctly removed."""
        self.assertEqual(
            to_snake_slug("The Fool's Journey"), 
            'the_fools_journey'
        )

    def test_parentheses_and_symbols(self):
        """Tests that parentheses and roman numerals are handled."""
        self.assertEqual(
            to_snake_slug('The World (XXI)'), 
            'the_world_xxi'
        )

    def test_hyphen_and_extra_spaces(self):
        """Tests that hyphens and leading/trailing spaces are handled."""
        self.assertEqual(
            to_snake_slug('  High-Priestess  '), 
            'high_priestess'
        )

    def test_multiple_spaces(self):
        """Tests that multiple spaces are collapsed into one underscore."""
        self.assertEqual(
            to_snake_slug('King   of   Wands'), 
            'king_of_wands'
        )
        
    def test_empty_string(self):
        """Tests that an empty string returns an empty string."""
        self.assertEqual(
            to_snake_slug(''), 
            ''
        )

    def test_string_with_only_symbols(self):
        """Tests that a string with only symbols becomes empty."""
        self.assertEqual(
            to_snake_slug('!@#$%^&*()'), 
            ''
        )
        
    def test_no_change_needed(self):
        """Tests that a valid slug is not changed."""
        self.assertEqual(
            to_snake_slug('already_a_slug'), 
            'already_a_slug'
        )

# This allows the file to be run directly
if __name__ == "__main__":
    unittest.main()