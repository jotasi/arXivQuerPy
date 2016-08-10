import unittest
from queryString import *


class test_queryString(unittest.TestCase):
    def setUp(self):
        self.queryString = QueryString()

    def tearDown(self):
        self.queryString = None


class test_emptyQueryString(test_queryString):
    def test_strEmpty(self):
        with self.assertRaises(EmptyQueryException):
            str(self.queryString)

    def test_getSearchStringEmpty(self):
        self.assertRaises(EmptyQueryException,
                          self.queryString.getSearchString)

    def test_getAllAuthorQueriesEmpty(self):
        self.assertEqual(self.queryString.getAllAuthorQueries(), [])

    def test_getAllTitleQueriesEmpty(self):
        self.assertEqual(self.queryString.getAllTitleQueries(), [])

    def test_getAllAuthorQueriesEmpty(self):
        self.assertEqual(self.queryString.getAllAbstractQueries(), [])

    def test_getAllCategoriesEmpty(self):
        self.assertEqual(self.queryString.getAllCategories(), [])

if __name__ == "__main__":
    unittest.main()
