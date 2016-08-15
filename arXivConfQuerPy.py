import datetime
import os
import sys

import queryString as qS
import feedDownloader as fD
import textComposer as tC
import mailSender as mS
from arXivQuerPy import arXivQuerPy


class FileExistsAlready(Exception):
    """The file exist already"""
    pass


class config():
    """Class that contains the configuration implementation of the arXiv
    updater.
    """
    def __init__(self, filename=".arXivQuerPyconfig"):
        """Constructor of the config class

        Parameters
        ----------
        filename: string
            path to the config file
        """
        self.args = {}
        self.filename = filename

    def get_args(self):
        """Returns the found arguments from the config files as a dict
        """
        return self.args

    def config_available(self):
        """Checks if the given config file is available.
        """
        return os.path.isfile(self.filename)

    def config_read(self):
        """Reads in the given config file.
        """
        self.args = {}

        if not self.config_available():
            raise Exception("File {0} does not exist.".format(self.filename))

        with open(self.filename) as config:
            content = config.read()

        # remove empty lines from content
        content = os.linesep.join([s for s in content.splitlines() if s])
        # remove lines starting with #
        content = os.linesep.join([s for s in content.splitlines()
                                   if not s.startswith('#')])

        print content

        key_args = ["email", "category", "title", "author", "abstract",
                    "suppress", "lastNDays"]
        for key in key_args:
            self.args[key] = None
            for line in content.split('\n'):
                split = line.split('=')
                if key == split[0].strip():
                    if split[1].strip() == "":
                        self.args[key] = None
                    else:
                        self.args[key] = split[1].strip()

    def generate_config(self):
        """Generator for the config file.
        Can only be called if the config file does not exist already.
        Requires user input, and can therefore not be used in a script.
        """
        if self.config_available():
            raise FileExistsAlready("File {0} already exists."
                                    .format(self.filename))
        else:
            content = """\
# email the results should be send to
email     = {email}

# category in which should be searched (space separated list)
category  = {category}

# keywords in the title (space separated list)
title     = {title}

# authors that should be searched (space separated list)
authors   = {author}

# keywords in abstract that should be searched (space separated list)
abstract  = {abstract}

# whether to suppress empty emails or not (True/False)
suppress  = {suppress}

# the amount of days the you want your results to go back
lastNDays = {lastNDays}
"""
            email     = raw_input("What is your email address? "
                                  "(Has to be from uni-mainz.de) ")
            category  = raw_input("Which categories should be searched? "
                                  "(cond-mat, cond-mat:soft) ")
            title     = raw_input("Which keywords should be in the title? ")
            author    = raw_input("Who are the authors? ")
            abstract  = raw_input("Which keywords should be in the abstract? ")
            suppress  = raw_input("Should empty email be suppressed? "
                                  "(True/False) ")
            lastNDays = raw_input("How many days from today should we search "
                                  "back? ")

            with open(self.filename, 'w') as conf:
                conf.write(content.format(email=email, category=category,
                                          title=title, author=author,
                                          abstract=abstract, suppress=suppress,
                                          lastNDays=lastNDays))


class DictToAttributes:
    """A helper class that turns a dict into a class with each key of the dict
    as an attribute of the class
    """
    def __init__(self, **entries):
        self.__dict__.update(entries)


if (__name__ == "__main__"):
    # Get the real path to the config file
    scriptpath = os.path.dirname(os.path.realpath(__file__))
    configpath = os.path.join(scriptpath, '.arXivQuerPyconfig')
    conf = config(configpath)

    # Check if a config file exists already, and
    # if not generate it together with the user.
    if not conf.config_available():
        print("Conf file not found create one first.")
        conf.generate_config()

    # Read in the arguments of the config file
    conf.config_read()
    if conf.get_args() == {}:
        print("No arguments available")
        sys.exit(1)
    args = conf.get_args()
    args = DictToAttributes(**args)

    # Generate the updater and feed in the arguments.
    if args.lastNDays is None:
        querPy = arXivQuerPy()
    else:
        querPy = arXivQuerPy(date=datetime.date.today() -
                             datetime.timedelta(days=int(args.lastNDays)))

    if not (args.category is None):
        querPy.addCategory(args.category.split(" "))
    if not (args.author is None):
        querPy.addAuthors(args.author.split(" "))
    if not (args.title is None):
        querPy.addTitleKeywords(args.title.split(" "))
    if not (args.abstract is None):
        querPy.addAbstractKeywords(args.abstract.split(" "))
    if args.suppress.lower() == "true":
        args.suppress = True

    # Do the search
    try:
        querPy.search()
    except qS.EmptyQueryException:
        exit(1)

    # Send the new papers if applicable
    if (querPy.sendMail(args.email, args.suppress)):
        print("Mail send.")
    else:
        print("No new papers matching the search.")
