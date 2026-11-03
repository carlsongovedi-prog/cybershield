import unittest
from validator import validate_text


class TestValidateText(unittest.TestCase):

    def test_accepts_valid_text(self):
        self.assertEqual(validate_text("Hello CyberShield"), "Hello CyberShield")

    def test_rejects_empty_text(self):
        with self.assertRaises(ValueError):
            validate_text("")

    def test_rejects_whitespace(self):
        with self.assertRaises(ValueError):
            validate_text("   ")

    def test_rejects_non_string(self):
        with self.assertRaises(TypeError):
            validate_text(123)

    def test_rejects_oversized_text(self):
        with self.assertRaises(ValueError):
            validate_text("A" * 4001)


if __name__ == "__main__":
    unittest.main()
