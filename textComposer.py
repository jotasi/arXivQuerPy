import feedparser
import datetime


class NotAFeedException(ValueError):
    """Raise when invalid input is given as a feed
    """


class NotADateException(ValueError):
    """Raise when invalid input is given as date
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
    def __init__(self, startingText="", date=None):
        """Constructor for a TextComposer

        Parameters
        ----------
        startingText: str
            greeting text to start the email
        date: datetime.date
            date until when to go back

        Raises
        ------
        NotADateException
            If the given date is not a datetime.date
        """
        self.text = startingText
        if ((not (date is None))
                and (not (type(date) == datetime.date))):
            raise NotADateException
        self.date = date

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

    def getDate(self):
        """Check the date search limit

        Returns
        -------
        date: datetime.date
            date until when to search
        """
        return self.date

    def updateDate(self, date):
        """Update date to search to

        Parameters
        ----------
        date: datetime.date
            date until when to go back

        Raises
        ------
        NotADateException
            If the given date is not a datetime.date
        """
        if not (type(date) == datetime.date):
            raise NotADateException
        self.date = date

    def addFeed(self, feed):
        """Adds another feed to the text

        Parameters
        ----------
        feed: feedparser.FeedParserDict
            feed to convert to valid string

        Returns
        -------
        finished: bool
            Indicates if the date was reached if any was given

        Raises
        ------
        NotAFeedException
            If the given feed has an invalid feed format
        """
        if not (type(feed) == feedparser.FeedParserDict):
            raise NotAFeedException
        reached = False
        if not (self.text == ""):
            self.text += u"\n"
        numEntries = len(feed.entries)
        for i, entry in enumerate(feed.entries):
            entryUpdateParsed = entry.updated_parsed
            if ((not (self.date is None))
                    and (datetime.date(*entryUpdateParsed[:3]) < self.date)):
                reached = True
                break
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
        return reached
