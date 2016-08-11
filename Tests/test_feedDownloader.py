import unittest
import os
from feedDownloader import *
from queryString import *


class test_feedDownloader(unittest.TestCase):
    def setUp(self):
        self.feedDownloader = FeedDownloader(r"hereShouldBeAnUrl")

    def tearDown(self):
        self.feedDownloader = None
        if os.path.exists("./feed.pickle"):
            os.remove("./feed.pickle")


class test_queryStringManipulationAndEmptyFeed(test_feedDownloader):
    def test_getter(self):
        self.assertEqual(self.feedDownloader.getQueryString(),
                         r"hereShouldBeAnUrl")

    def test_updateFunction(self):
        self.feedDownloader.updateQueryString(r"notAProperUrlAgain")
        self.assertEqual(self.feedDownloader.getQueryString(),
                         r"notAProperUrlAgain")

    def test_emptyFeed(self):
        with self.assertRaises(NoDownloadedFeedException):
            self.feedDownloader.getFeed()

    def test_saveEmptyFeed(self):
        with self.assertRaises(NoDownloadedFeedException):
            self.feedDownloader.saveFeed()

    def test_loadOldBackUp(self):
        fileName = "./Tests/testFeed.pickle"
        self.feedDownloader.loadFeed(fileName)
        feed = self.feedDownloader.getFeed()
        self.assertEqual(type(feed), feedparser.FeedParserDict)
        self.assertEqual(len(feed.entries), 10)


class test_feedDownload(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.feedDownloader = FeedDownloader(r"http://export.arxiv.org/api/"
                                            r"query?search_query="
                                            r"%28abs:active%29&sortBy="
                                            r"lastUpdatedDate&start=0&"
                                            r"max_results=10")
        cls.feedDownloader.updateFeed()

    def test_loadInexistingBackUp(self):
        with self.assertRaises(NoSavedFeedException):
            self.feedDownloader.loadFeed()

    def test_saveLoadBackUp(self):
        self.feedDownloader.saveFeed()
        newFeedDownloader = FeedDownloader("garbageString")
        newFeedDownloader.loadFeed()
        self.assertEqual(self.feedDownloader.getFeed(),
                         newFeedDownloader.getFeed())

    def test_saveBackUpChangedName(self):
        fileName = "./nameTest.pickle"
        self.feedDownloader.saveFeed(fileName)
        self.assertTrue(os.path.exists(fileName))
        if os.path.exists(fileName):
            os.remove(fileName)

    def test_saveLoadBackUpChangedName(self):
        fileName = "./nameTest.pickle"
        self.feedDownloader.saveFeed(fileName)
        newFeedDownloader = FeedDownloader("garbageString")
        newFeedDownloader.loadFeed(fileName)
        self.assertEqual(self.feedDownloader.getFeed(),
                         newFeedDownloader.getFeed())
        if os.path.exists(fileName):
            os.remove(fileName)

    def test_getFeed(self):
        feed = self.feedDownloader.getFeed()
        self.assertEqual(type(feed), feedparser.FeedParserDict)
        self.assertEqual(len(feed.entries), 10)

    @classmethod
    def tearDownClass(cls):
        cls.feedDownloader = None
        if os.path.exists("./feed.pickle"):
            os.remove("./feed.pickle")


if __name__ == "__main__":
    unittest.main()
