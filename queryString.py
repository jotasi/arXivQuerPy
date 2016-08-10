class EmptyQueryException(Exception):
    """Raise when trying to use empty QueryString
    """


class InvalidCategoryException(Exception):
    """Raise for unknown categories
    """


class NotInQueryException(Exception):
    """Raise when trying to access query elements that are not present
    """


class QueryString:
    """Composer of a query string for searches using arXiv's api
    """

    baseUrl = r"http://export.arxiv.org/api/query?"
    searchPrefix = r"search_query="
    blockStart = r"%28"
    blockEnd = r"%29"
    andString = r"+AND+"
    orString = r"+OR+"

    def __init__(self):
        pass

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
        return ""

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

    def getAllAuthorQueries(self):
        """Give a list of all authors that are searched for

        Returns
        -------
        authorList: list
            List of all authors that are searched for
        """

    def getAllTitleQueries(self):
        """Give a list of all title queries that are searched for

        Returns
        -------
        titleList: list
            List of all title queries that are searched for
        """

    def getAllAbstractQueries(self):
        """Give a list of all abstract queries that are searched for

        Returns
        -------
        abstractList: list
            List of all abstract queries that are searched for
        """

    def getAllCategories(self):
        """Give a list of all categories that are searched in

        Returns
        -------
        categoryList: list
            List of all categories that are searched in
        """

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

    def removeAllAuthorQueries(self):
        """Remove all authors from the query string

        Stop searching for authors. At least one query has to be
        specified overall to have a valid query string.
        """

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

    def removeAllTitleQueries(self):
        """Remove all titles from the query string

        Stop searching for titles. At least one query has to be
        specified overall to have a valid query string.
        """

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

    def removeAllAbstractQueries(self):
        """Remove all abstracts from the query string

        Stop searching for abstracts. At least one query has to be
        specified overall to have a valid query string.
        """

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