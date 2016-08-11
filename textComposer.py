import feedparser


class NotAFeedException(Exception):
    """Raise when invalid input is given as a feed
    """


class TextComposer():
    """Makes feeds from the arXiv api readable

    Feed will include all entries in the form:
    Title
    Author1, Author2, ...
    URL
    Abstract
    newLine
    """
    def __init__(self, startingText=""):
        """Constructor for a TextComposer

        Parameters
        ----------
        startingText: str
            greeting text to start the email
        """
        self.text = ""

    def __str__(self):
        return self.text

    def getText(self):
        """Gives the current version of the text

        Returns
        -------
        text: str
            Current text version
        """

    def addFeed(self, feed):
        """Adds another feed to the text

        Parameters
        ----------
        feed: feedparser.FeedParserDict
            feed to convert to valid string

        Raises
        ------
        NotAFeedException
            If the given feed has an invalid feed format
        """
