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
        self.text = startingText

    def __str__(self):
        return self.text.encode("utf-8")

    def getText(self):
        """Gives the current version of the text

        Returns
        -------
        text: str
            Current text version
        """
        return str(self)

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
        if not (type(feed) == feedparser.FeedParserDict):
            raise NotAFeedException
        if not (self.text == ""):
            self.text += u"\n"
        numEntries = len(feed.entries)
        for i, entry in enumerate(feed.entries):
            if i > 0:
                self.text += u"\n"
            self.text += entry.title+u"\n"
            numAuthors = len(entry.authors)
            for j, author in enumerate(entry.authors):
                self.text += author["name"]
                if j < numAuthors-1:
                    self.text += u", "
                else:
                    self.text += u"\n"
            self.text += entry.link+u"\n"
            self.text += entry.summary+u"\n"
