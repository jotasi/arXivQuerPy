import unittest
import smtplib
from mailSender import *


class test_mailSender(unittest.TestCase):
    def test_invalidEmail(self):
        with self.assertRaises(smtplib.SMTPRecipientsRefused):
            sendMail("Test", "asdf")


if __name__ == "__main__":
    unittest.main()
