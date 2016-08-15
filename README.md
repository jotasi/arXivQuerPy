# arXivQuerPy
(Very creative/funny, I know...)

E-Mail for comments and/or suggestions to siebertjonathan(at)aim.com

arXivQuerPy is a `python` code to automatically search arXiv for new uploads or
updates during the last days matching to queries that you defined.

## Download/Installation

Simply clone this git:

    cd some/folder/
    git clone git@gitlab.physik.uni-mainz.de:josieber/arXivQuerPy.git

You can check, that it works by running the unittests:

    cd arXivQuerPy
    python -m unittest discover Tests

You might need additional packages to run the code. Those can be installed by
`pip`:

    pip install --user argparse datetime feedparser

The python file to run is `arXivQuerPy.py`. You can get all options by use of
the `-h` flag. Also you could write you own script calling the functions of
arXivQuerPy to suite your needs.

## Functionality

You can specify authors(`-a`) and title/abstract keywords(`-t`/`-b`) to search
for in categories(`-c`/`-C`) of your choice. Specifying `-s` will prevent empty
emails being sent to you. Default search time is 1 day. To look back further
you can specify an amount of days with the `-l` flag.

The underlying classes also have further functionalities that are not parsed of
the script, yet. Feel free to implement further options. Also it should be
relatively straightforward to include additional feeds.

## Configuration file

You can use the arXiv updater with a configuration file as well. 
For that execute the file `arXivConfQuerPy.py`. It will guide you through the
first generation of a condifuration file. Feel free to change the file to a 
later stage if you want. By default the filename will be `.arXivQuerPyconfig`.

### Example configuration file
```bash
# email the results should be send to
email     = your.email@uni-mainz.de

# category in which should be searched (space separated list)
category  = cond-mat 

# keywords in the title (space separated list)
title     = 

# authors that should be searched (space separated list)
authors   = 

# keywords in abstract that should be searched (space separated list)
abstract  = active

# whether to suppress empty emails or not (True/False) 
suppress  = True

# the amount of days the you want your results to go back
lastNDays = 1 
```

## Automation

To get a daily update, you can add the script to your crontab. E.g. to run the
script Monday to Friday at 7am add two lines to your crontab:

    crontab -e  # Now add the following lines and then save
    0 7 * * 2,3,4,5   python /path/to/arXivQuerPy.py -e email@uni-mainz.de\
            -a /path/to/Authors.txt -t /path/to/titles -C category -s
    0 7 * * 1   python /path/to/arXivQuerPy.py -e email@uni-mainz.de\
            -a /path/to/Authors.txt -t /path/to/titles -C category -sl 3

If you choose to use the configuration file method, first generate the config 
file and then run:

    crontab -e
    0 7 * * 1 python /path/to/arXivConfQuerPy.py
