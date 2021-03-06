class EmptyQueryException(Exception):
    """Raise when trying to use empty QueryString
    """


class InvalidCategoryException(Exception):
    """Raise for unknown categories
    """


class NotInQueryException(Exception):
    """Raise when trying to access query elements that are not present
    """


class InvalidConnectorException(Exception):
    """Raise when trying to set connector not being and/or
    """


class QueryString:
    """Composer of a query string for searches using arXiv's api
    """

    baseUrl = r"http://export.arxiv.org/api/query?"
    searchPrefix = r"search_query="
    blockStart = r"%28"
    blockEnd = r"%29"
    connectorStrings = {"and": r"+AND+", "or": r"+OR+"}
    validCategories = ["cond-mat",
                       "cond-mat.soft",
                       "cond-mat.stat-mech",
                       "cond-mat.dis-nn",
                       "cond-mat.other",
                       "cond-mat.mtrl-sci",
                       "physics.bio-ph",
                       "physics.comp-ph"]

    def __init__(self, N=10, start=0, connector="or"):
        """Constructor for a query string

        Parameters
        ----------
        N: int
            Number of results to search for
        start: int
            Result number to start from
        connector: str
            Can be either 'and' or 'or' between author and title/abstract

        Raises
        ------
        InvalidConnectorException
            If connector is not and/or
        """
        self.start = start
        self.N = N
        self.categories = []
        self.queries = {"ti":  [],
                        "abs": [],
                        "au":  []}
        self.connector = connector.lower()
        if not (self.connector in self.connectorStrings.keys()):
            raise InvalidConnectorException

    def __checkForEmptyQuery(self):
        """Check if there are any queries

        Returns
        -------
        empty: bool
            Indicates if this is a valid query.
        """
        empty = True
        for key in self.queries:
            if len(self.queries[key]) > 0:
                empty = False
                break
        return empty

    def __produceBlock(self, qType, qList=None):
        """Produce a block of queries for the given type (without parantheses)

        Parameters
        ----------
        qType: str
            Type to create the block for
        qList: list
            List of queries (if not given self.queries[qType] is used)

        Returns
        -------
        block: str
            Block for the given qType
        """
        block = ""
        first = True
        for query in (qList if not (qList is None) else self.queries[qType]):
            if first:
                block += qType + ":" + query
                first = False
            else:
                block += self.connectorStrings["or"] + qType + ":" + query
        return block

    def __str__(self):
        """Gives the current QueryString as string

        Gives a valid query string to use on arXiv's api containing all
        information previously added.

        Returns
        -------
        str
            query string

        Raises
        ------
        EmptyQueryException
            If there are no querys to search for.
        """
        if self.__checkForEmptyQuery():
            raise EmptyQueryException

        # What fields are needed?
        authors = (len(self.queries["au"]) > 0)
        titlesOrAbstracts = ((len(self.queries["ti"]) > 0)
                             or (len(self.queries["abs"]) > 0))
        titlesAndAbstracts = ((len(self.queries["ti"]) > 0)
                              and (len(self.queries["abs"]) > 0))
        categories = (len(self.categories) > 0)

        url = self.baseUrl + self.searchPrefix + self.blockStart
        # Start with authors
        if authors:
            url += self.blockStart + self.__produceBlock("au") + self.blockEnd
            if titlesOrAbstracts:
                url += self.connectorStrings[self.connector]

        # Now do title/abstract queries
        if titlesOrAbstracts:
            url += self.blockStart
        url += self.__produceBlock("ti")
        if titlesAndAbstracts:
            url += self.connectorStrings["or"]
        url += self.__produceBlock("abs") + self.blockEnd
        if titlesOrAbstracts:
            url += self.blockEnd

        # Lastly, do the categories
        if categories:
            url += (self.connectorStrings["and"] + self.blockStart
                    + self.__produceBlock("cat", self.categories)
                    + self.blockEnd)
        url += (r"&sortBy=lastUpdatedDate&start={0:d}&max_results={1:d}"
                .format(self.start, self.N))
        return url

    def getSearchString(self):
        """Gives the current QueryString as string

        Gives a valid query string to use on arXiv's api containing all
        information previously added.

        Returns
        -------
        str
            query string

        Raises
        ------
        EmptyQueryException
            If there are no querys to search for.
        """
        return str(self)

    def getAllAuthorQueries(self):
        """Give a list of all authors that are searched for

        Returns
        -------
        authorList: list
            List of all authors that are searched for
        """
        return self.queries["au"]

    def getAllTitleQueries(self):
        """Give a list of all title queries that are searched for

        Returns
        -------
        titleList: list
            List of all title queries that are searched for
        """
        return self.queries["ti"]

    def getAllAbstractQueries(self):
        """Give a list of all abstract queries that are searched for

        Returns
        -------
        abstractList: list
            List of all abstract queries that are searched for
        """
        return self.queries["abs"]

    def getAllCategories(self):
        """Give a list of all categories that are searched in

        Returns
        -------
        categoryList: list
            List of all categories that are searched in
        """
        return self.categories

    def setConnector(self, connector):
        """Set to do or/and searches

        Parameters
        ----------
        connector: str
            Can be either 'and' or 'or'

        Raises
        ------
        InvalidConnectorException
            If connector is not and/or
        """
        self.connector = connector.lower()
        if not (self.connector in self.connectorStrings.keys()):
            raise InvalidConnectorException

    def nextNumberOfResults(self, N=10):
        """Changes the query string to search for the next N results

        Parameters
        ----------
        N: int
            Number of next results to search for
        """
        self.start += self.N
        self.N = N

    def addAuthorQuery(self, authorName):
        """Add an author to be contained in the query string

        Add an author to also search for. All authors, title, and abstract
        queries will be searched for (or-connected). At least one of them has
        to be specified to have a valid query string.

        Parameters
        ----------
        authorName: str
            Name of an author to also search for
        """
        if not (authorName in self.queries["au"]):
            self.queries["au"].append(authorName)

    def addTitleQuery(self, titleQuery):
        """Add an string to be contained in a title to the query string

        Add a word to search in titles for. All authors, title, and abstract
        queries will be searched for (or-connected). At least one of them has
        to be specified to have a valid query string.

        Parameters
        ----------
        titleQuery: str
            Word to also search for in titles
        """
        if not (titleQuery in self.queries["ti"]):
            self.queries["ti"].append(titleQuery)

    def addAbstractQuery(self, abstractQuery):
        """Add an string to be contained in an abstract to the query string

        Add a word to search in an abstract for. All authors, title, and
        abstract queries will be searched for (or-connected). At least one of
        them has to be specified to have a valid query string.

        Parameters
        ----------
        abstractQuery: str
            Word to also search for in abstracts
        """
        if not (abstractQuery in self.queries["abs"]):
            self.queries["abs"].append(abstractQuery)

    def addCategory(self, category):
        """Add a category to be searched in

        Add a category in which to search. Multiple categories added
        subsequently will all be searched in. If no category is specified all
        are searched in (not recommended).
        Valid categories are (atm):
            cond-mat
            cond-mat.soft

        Raises
        ------
        InvalidCategoryException
            If the category is not a known category
        """
        if not (category in self.validCategories):
            raise InvalidCategoryException
        if not (category in self.categories):
            self.categories.append(category)

    def removeAuthorQuery(self, authorName):
        """Remove an author from the query string

        Stop searching for a given author. At least one query has to be
        specified overall to have a valid query string.

        Parameters
        ----------
        authorName: str
            Name of an author to stop searching for

        Raises
        ------
        NotInQueryException
            If the specified author was not in the query before
        """
        try:
            self.queries["au"].remove(authorName)
        except ValueError:
            raise NotInQueryException

    def removeAllAuthorQueries(self):
        """Remove all authors from the query string

        Stop searching for authors. At least one query has to be
        specified overall to have a valid query string.
        """
        self.queries["au"] = []

    def removeTitleQuery(self, titleQuery):
        """Remove an title query from the query string

        Stop searching for a given string in titles. At least one query has
        to be specified overall to have a valid query string.

        Parameters
        ----------
        titleQuery: str
            Word to stop searching for in titles

        Raises
        ------
        NotInQueryException
            If the specified word was not in the title queries before
        """
        try:
            self.queries["ti"].remove(titleQuery)
        except ValueError:
            raise NotInQueryException

    def removeAllTitleQueries(self):
        """Remove all titles from the query string

        Stop searching for titles. At least one query has to be
        specified overall to have a valid query string.
        """
        self.queries["ti"] = []

    def removeAbstractQuery(self, abstractQuery):
        """Remove an abstract query from the query string

        Stop searching for a given string in abstracts. At least one query has
        to be specified overall to have a valid query string.

        Parameters
        ----------
        abstractQuery: str
            Word to stop searching for in abstracts

        Raises
        ------
        NotInQueryException
            If the specified word was not in the title queries before
        """
        try:
            self.queries["abs"].remove(abstractQuery)
        except ValueError:
            raise NotInQueryException

    def removeAllAbstractQueries(self):
        """Remove all abstracts from the query string

        Stop searching for abstracts. At least one query has to be
        specified overall to have a valid query string.
        """
        self.queries["abs"] = []

    def removeCategory(self, category):
        """Remove a search category

        Stop searching for in a given category.

        Parameters
        ----------
        category: str
            Name of a category to stop searching in

        Raises
        ------
        InvalidCategoryException
            If the given category is not a known category
        NotInQueryException
            If the specified category was not searched in before
        """
        if not (category in self.validCategories):
            raise InvalidCategoryException
        try:
            self.categories.remove(category)
        except ValueError:
            raise NotInQueryException
