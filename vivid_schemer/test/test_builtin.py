# -*- coding: utf-8 -*-

from vivid_schemer.builtin import *
from vivid_schemer.parser import new_symbol

import unittest


class TestBuiltin(unittest.TestCase):
    def testIsLetterBeginStr(self):
        self.assertTrue(is_letter_begin_str(new_symbol('aaa')))
        self.assertTrue(is_letter_begin_str(new_symbol('aa11133')))
        self.assertTrue(is_letter_begin_str(new_symbol('aa11133')))
        self.assertTrue(is_letter_begin_str(new_symbol('*abc$')))
        self.assertTrue(is_letter_begin_str(new_symbol('你好')))
        self.assertTrue(is_letter_begin_str(new_symbol('*abc1231$')))
        self.assertFalse(is_letter_begin_str(new_symbol('1231$')))
        self.assertFalse(is_letter_begin_str(new_symbol('2.2')))

    def testIsDigitStr(self):
        self.assertTrue(is_digit_str(new_symbol('123456789')))
        self.assertFalse(is_digit_str(new_symbol('123456789a')))
        self.assertFalse(is_digit_str(new_symbol('aa11133')))
        self.assertFalse(is_digit_str(new_symbol('111s33')))
        self.assertFalse(is_letter_begin_str(new_symbol('2.2')))
