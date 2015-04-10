import unittest

import test_lexer

def suite():
    suite = unittest.TestSuite()
    suite.addTest(test_lexer.TestLex('test_bool'))
    suite.addTest(test_lexer.TestLex('test_string'))
    # suite.addTest(test_lexer.TestLex('test_identifier'))
    return suite

def run():
    unittest.main(defaultTest='test.suite')
