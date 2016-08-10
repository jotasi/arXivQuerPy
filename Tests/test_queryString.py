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


class test_addingRemovingCategories(test_queryString):
    def test_addingValidCategories(self):
        self.queryString.addCategory("cond-mat")
        self.queryString.addCategory("cond-mat.soft")
        self.assertEqual(self.queryString.getAllCategories(),
                         ["cond-mat", "cond-mat.soft"])

    def test_addingValidCategoryTwice(self):
        self.queryString.addCategory("cond-mat")
        self.queryString.addCategory("cond-mat")
        self.assertEqual(self.queryString.getAllCategories(), ["cond-mat"])

    def test_addingEmptyCategory(self):
        with self.assertRaises(InvalidCategoryException):
            self.queryString.addCategory("")

    def test_addingUnknownCategory(self):
        with self.assertRaises(InvalidCategoryException):
            self.queryString.addCategory("definetlyInvalid")

    def test_removeExistingCategory(self):
        self.queryString.addCategory("cond-mat")
        self.queryString.addCategory("cond-mat.soft")
        self.queryString.removeCategory("cond-mat")
        self.assertEqual(self.queryString.getAllCategories(),
                         ["cond-mat.soft"])

    def test_removeInvalidCategory(self):
        with self.assertRaises(InvalidCategoryException):
            self.queryString.removeCategory("definetlyInvalid")

    def test_removeNotExistingCategory(self):
        self.queryString.addCategory("cond-mat.soft")
        with self.assertRaises(NotInQueryException):
            self.queryString.removeCategory("cond-mat")


class test_addingRemovingSearchQueries(test_queryString):
    def test_addAuthors(self):
        self.queryString.addAuthorQuery("Testfrau_T")
        self.queryString.addAuthorQuery("Mustermann_M")
        self.assertEqual(self.queryString.getAllAuthorQueries(),
                         ["Testfrau_T", "Mustermann_M"])

    def test_addAbstracts(self):
        self.queryString.addAbstractQuery("Awesome")
        self.queryString.addAbstractQuery("Stuff")
        self.assertEqual(self.queryString.getAllAbstractQueries(),
                         ["Awesome", "Stuff"])

    def test_addTitles(self):
        self.queryString.addTitleQuery("Awesome")
        self.queryString.addTitleQuery("Stuff")
        self.assertEqual(self.queryString.getAllTitleQueries(),
                         ["Awesome", "Stuff"])

    def test_addExistingAuthors(self):
        self.queryString.addAuthorQuery("Testfrau_T")
        self.queryString.addAuthorQuery("Testfrau_T")
        self.assertEqual(self.queryString.getAllAuthorQueries(),
                         ["Testfrau_T"])

    def test_addExistingAbstracts(self):
        self.queryString.addAbstractQuery("Awesome")
        self.queryString.addAbstractQuery("Awesome")
        self.assertEqual(self.queryString.getAllAbstractQueries(), ["Awesome"])

    def test_addExistingTitles(self):
        self.queryString.addTitleQuery("Awesome")
        self.queryString.addTitleQuery("Awesome")
        self.assertEqual(self.queryString.getAllTitleQueries(), ["Awesome"])

    def test_removeExistingAuthors(self):
        self.queryString.addAuthorQuery("Testfrau_T")
        self.queryString.addAuthorQuery("Mustermann_M")
        self.queryString.removeAuthorQuery("Testfrau_T")
        self.assertEqual(self.queryString.getAllAuthorQueries(),
                         ["Mustermann_M"])

    def test_removeExistingAbstracts(self):
        self.queryString.addAbstractQuery("Awesome")
        self.queryString.addAbstractQuery("Stuff")
        self.queryString.removeAbstractQuery("Awesome")
        self.assertEqual(self.queryString.getAllAbstractQueries(),
                         ["Stuff"])

    def test_removeExistingTitles(self):
        self.queryString.addTitleQuery("Awesome")
        self.queryString.addTitleQuery("Stuff")
        self.queryString.removeTitleQuery("Awesome")
        self.assertEqual(self.queryString.getAllTitleQueries(),
                         ["Stuff"])

    def test_removeNotExistingAuthors(self):
        self.queryString.addAuthorQuery("Mustermann_M")
        with self.assertRaises(NotInQueryException):
            self.queryString.removeAuthorQuery("Testfrau_T")

    def test_removeNotExistingAbstracts(self):
        self.queryString.addAbstractQuery("Stuff")
        with self.assertRaises(NotInQueryException):
            self.queryString.removeAbstractQuery("Awesome")

    def test_removeNotExistingTitles(self):
        self.queryString.addTitleQuery("Stuff")
        with self.assertRaises(NotInQueryException):
            self.queryString.removeTitleQuery("Awesome")

    def test_removeAllExistingAuthors(self):
        self.queryString.addAuthorQuery("Testfrau_T")
        self.queryString.addAuthorQuery("Mustermann_M")
        self.queryString.removeAllAuthorQueries()
        self.assertEqual(self.queryString.getAllAuthorQueries(),
                         [])

    def test_removeAllExistingAbstracts(self):
        self.queryString.addAbstractQuery("Awesome")
        self.queryString.addAbstractQuery("Stuff")
        self.queryString.removeAllAbstractQueries()
        self.assertEqual(self.queryString.getAllAbstractQueries(),
                         [])

    def test_removeAllExistingTitles(self):
        self.queryString.addTitleQuery("Awesome")
        self.queryString.addTitleQuery("Stuff")
        self.queryString.removeAllTitleQueries()
        self.assertEqual(self.queryString.getAllTitleQueries(),
                         [])

    def test_removeEmptyAuthors(self):
        self.queryString.removeAllAuthorQueries()
        self.assertEqual(self.queryString.getAllAuthorQueries(),
                         [])

    def test_removeEmptyAbstracts(self):
        self.queryString.removeAllAbstractQueries()
        self.assertEqual(self.queryString.getAllAbstractQueries(),
                         [])

    def test_removeEmptyTitles(self):
        self.queryString.removeAllTitleQueries()
        self.assertEqual(self.queryString.getAllTitleQueries(),
                         [])


if __name__ == "__main__":
    unittest.main()
