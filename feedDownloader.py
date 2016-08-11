import urllib
import feedparser
import pickle
import os


class NoDownloadedFeedException(Exception):
    """Raised when no feed was downloaded, yet.
    """


class NoSavedFeedException(Exception):
    """Raised when no saved feed is found
    """


class FeedDownloader():
    """Downloads and parses xml file using arXiv's api for a given query string
    """
    def __init__(self, queryString):
        """Constructor for a FeedDownloader

        Parameters
        ----------
        queryString: str
            String to use for arXiv api query
        """
        self.queryString = queryString
        self.feed = None

    def updateQueryString(self, queryString):
        """Change the query string

        Parameters
        ----------
        queryString: str
            String to use for arXiv api query
        """
        self.queryString = queryString

    def getQueryString(self):
        """Getter for the query string

        Returns
        -------
        queryString: str
            current query string
        """
        return self.queryString

    def updateFeed(self):
        """Downloads the current feed
        """
        self.feed = feedparser.parse(urllib.urlopen(self.queryString).read())

    def getFeed(self):
        """Returns the current feed

        Raises
        ------
        NoDownloadedFeedException
            If no feed was downloaded, yet. Call updateFeed first!
        """
        if self.feed is None:
            raise NoDownloadedFeedException
        return self.feed

    def saveFeed(self, fileName=r"./feed.pickle"):
        """Saves the feed for further use
        """
        if self.feed is None:
            raise NoDownloadedFeedException
        pickle.dump(self.feed, open(fileName, "wb"))

    def loadFeed(self, fileName=r"./feed.pickle"):
        """Loads the feed for further use

        Raises
        ------
        NoSavedFeedException
            If no saved feed is found
        """
        if not os.path.exists(fileName):
            raise NoSavedFeedException
        self.feed = pickle.load(open(fileName, "rb"))
