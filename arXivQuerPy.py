import argparse
import datetime
import collections
import os
import sys

import queryString as qS
import feedDownloader as fD
import textComposer as tC
import mailSender as mS


class arXivQuerPy():
    """Main code that glues the other classes to do the full query
    """
    def __init__(self,
                 greeting=None,
                 date=datetime.date.today() - datetime.timedelta(days=1)):
        """Constructor for the glue class

        Parameters
        ----------
        greeting: str
            Beginning of the message
        date: datetime.date
            From when to get the updateDate
        """
        if (greeting is None):
            greeting = "arXiv update since {0}:\n".format(str(date))
        self.query = qS.QueryString()
        self.feedDL = None
        self.textComp = tC.TextComposer(greeting, date)

    def addCategory(self, categories):
        """Add a categories to search in
        """
        if (type(categories) == str):
            self.query.addCategory(categories)
        else:
            for category in categories:
                self.query.addCategory(category)

    def addAuthors(self, authors):
        """Add authors to search for
        """
        if (type(authors) == str):
            self.query.addAuthorQuery(authors)
        else:
            for author in authors:
                self.query.addAuthorQuery(author)

    def addTitleKeywords(self, titles):
        """Add title keywords to search for
        """
        if (type(titles) == str):
            self.query.addTitleQuery(titles)
        else:
            for title in titles:
                self.query.addTitleQuery(title)

    def addAbstractKeywords(self, abstracts):
        """Add abstract keywords to search for
        """
        if (type(abstracts) == str):
            self.query.addAbstractQuery(abstracts)
        else:
            for abstract in abstracts:
                self.query.addAbstractQuery(abstract)

    def search(self, andNotOr=False):
        """Perform the query with the chosen keywords/categories

        Set and=True if you want to only search titles/abstracts by the authors
        """
        if andNotOr:
            self.query.setConnector("and")
        else:
            self.query.setConnector("or")
        try:
            url = self.query.getSearchString()
        except qS.EmptyQueryException as e:
            print("You have to specify at least one of the following:")
            print(" - One or multiple authors")
            print(" - Title/Abstract keyword to search for")
            raise e
        if self.feedDL is None:
            self.feedDL = fD.FeedDownloader(url)
        else:
            self.feedDL.updateQueryString(url)
        self.feedDL.updateFeed()
        while(not self.textComp.addFeed(self.feedDL.getFeed())):
            self.query.nextNumberOfResults(10)
            self.feedDL.updateQueryString(self.query.getSearchString())
            self.feedDL.updateFeed()

    def sendMail(self, address, suppress):
        """Sends the gathered feed as text to the given address.
        Returns boolean whether mail was send.
        """
        text = self.textComp.getText()
        if ((not suppress) or (text.count('\n') > 2)):
            mS.sendMail(text, address)
            return True
        else:
            return False


if (__name__ == "__main__"):
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--email", type=str, required=True,
                        help="Update will be send to this email address")
    parser.add_argument("-c", "--categories", type=str, default=None,
                        help="File containing the categories to search in")
    parser.add_argument("-C", "--category", type=str, default=None,
                        help="Category to search in")
    parser.add_argument("-a", "--author", type=str, default=None,
                        help="File containing the author ids to search for")
    parser.add_argument("-A", "--authorList", nargs='+', default=None,
                        help="List of author ids to search for")
    parser.add_argument("-t", "--title", type=str, default=None,
                        help="File containing the keywords to search for in "
                             "titles")
    parser.add_argument("-T", "--titleList", nargs='+', default=None,
                        help="List of keywords to search for in titles")
    parser.add_argument("-b", "--abstract", type=str, default=None,
                        help="File containing the keywords to search for in "
                             "abstracts")
    parser.add_argument("-B", "--abstractList", nargs='+', default=None,
                        help="List of keywords to search for in abstracts")
    parser.add_argument("-s", "--suppress", action="store_true",
                        help="Don't send me empty EMails!")
    parser.add_argument("-l", "--lastNDays", type=int, default=None,
                        help="Go back this many days")
    parser.add_argument("--andNotOr", action="store_true",
                        help="Search for one of the titles from one of "
                             "the authors")
    args = parser.parse_args()

    if args.lastNDays is None:
        querPy = arXivQuerPy()
    else:
        querPy = arXivQuerPy(date=datetime.date.today() -
                             datetime.timedelta(days=args.lastNDays))

    if not (args.categories is None):
        with open(args.categories) as f:
            querPy.addCategory(f.read().split())
    if not (args.category is None):
        querPy.addCategory(args.category)
    if not (args.author is None):
        with open(args.author) as f:
            querPy.addAuthors(f.read().split())
    if not (args.authorList is None):
        querPy.addAuthors(args.authorList)
    if not (args.title is None):
        with open(args.title) as f:
            querPy.addTitleKeywords(f.read().split())
    if not (args.titleList is None):
        querPy.addTitleKeywords(args.titleList)
    if not (args.abstract is None):
        with open(args.abstract) as f:
            querPy.addAbstractKeywords(f.read().split())
    if not (args.abstractList is None):
        querPy.addAbstractKeywords(args.abstractList)

    try:
        querPy.search(args.andNotOr)
    except qS.EmptyQueryException:
        exit(1)

    querPy.sendMail(args.email, args.suppress)
