import unittest
import feedparser
import datetime
from feedDownloader import *
from textComposer import *


class test_textComposerDateConstructor(unittest.TestCase):
    def test_invalidDate(self):
        with self.assertRaises(NotADateException):
            TextComposer(date=10)

    def test_validDate(self):
        date = datetime.date(2016, 1, 1)
        self.assertEqual(TextComposer(date=date).getDate(), date)


class test_textComposer(unittest.TestCase):
    def setUp(self):
        self.textComposer = TextComposer()

    def test_addingInt(self):
        with self.assertRaises(NotAFeedException):
            self.textComposer.addFeed(1)

    def test_addingDict(self):
        with self.assertRaises(NotAFeedException):
            self.textComposer.addFeed({"title": "asdf",
                                       "authors": "fdsa",
                                       "link": "asdff",
                                       "summary": "ffdsa"})

    def test_updateDate(self):
        date = datetime.date(2016, 1, 1)
        self.textComposer.updateDate(date)
        self.assertEqual(self.textComposer.getDate(), date)

    def test_dateReachedEmpty(self):
        date = datetime.date(2016, 8, 11)
        self.textComposer.updateDate(date)
        feedDL = FeedDownloader(r"notNecessary")
        feedDL.loadFeed("./Tests/testFeedEmpty.pickle")
        feed = feedDL.getFeed()
        self.assertTrue(self.textComposer.addFeed(feed))

    def test_dateReached(self):
        date = datetime.date(2016, 8, 11)
        self.textComposer.updateDate(date)
        feedDL = FeedDownloader(r"notNecessary")
        feedDL.loadFeed("./Tests/testFeed.pickle")
        feed = feedDL.getFeed()
        self.assertTrue(self.textComposer.addFeed(feed))

    def test_dateNotReached(self):
        date = datetime.date(2016, 8, 9)
        self.textComposer.updateDate(date)
        feedDL = FeedDownloader(r"notNecessary")
        feedDL.loadFeed("./Tests/testFeed.pickle")
        feed = feedDL.getFeed()
        self.assertFalse(self.textComposer.addFeed(feed))

    def test_noFeed(self):
        self.assertEqual(str(self.textComposer), "")
        self.assertEqual(self.textComposer.getText(), "")

    def test_testFeed(self):
        expectedText = (u"Combinations of Adaptive Filters with Coefficients"
                        u" Feedback\n"
                        u"Luiz F. O. Chamon, Cassio G. Lopes\n"
                        u"http://arxiv.org/abs/1608.03248v1\n"
                        u"Parallel combinations of adaptive filters have been"
                        u" effectively used to\nimprove the performance of"
                        u" adaptive algorithms and address typical trade-offs"
                        u",\nsuch as the one between convergence rate and "
                        u"steady-state error. In these\ncombinations, the "
                        u"component filters are usually run independently and"
                        u" then\ncombined, which leads to a well known "
                        u"convergence stagnation effect.\nConditional "
                        u"transfers of coefficients between filters were "
                        u"introduced in an\nattempt to handle this issue. "
                        u"This work introduces a more natural way of\n"
                        u"accelerating convergence to steady-state by "
                        u"cyclically feeding back the overall\ncoefficients "
                        u"to all component filters. Besides coping with "
                        u"convergence\nstagnation, this new topology allows "
                        u"several adaptive algorithms (e.g., mixed\nnorm, "
                        u"data reusing, and variable step size) to be posed "
                        u"as combinations of\nsimple adaptive filters, "
                        u"bridging an important conceptual gap. Steady-state "
                        u"and\ntracking analysis accounting for a myriad of "
                        u"component filters are derived for\ncombinations "
                        u"with and without feedback. Transient analyses of "
                        u"the typical\nconvex and affine supervisors are "
                        u"extended to general activation functions and\n"
                        u"applied to combinations with cyclic coefficients "
                        u"feedback. Numerical examples\nare provided to "
                        u"illustrate how coefficients feedback can improve "
                        u"the\nperformance of several existing parallel "
                        u"combinations at a small additional\ncomputational "
                        u"cost.\n\n"
                        u"Valid population inference for information-based "
                        u"imaging: From the\n  second-level $t$-test to "
                        u"prevalence inference\n"
                        u"Carsten Allefeld, Kai G\xf6rgen, John-Dylan Haynes"
                        u"\n")
        if not isinstance(expectedText, str):
            expectedText = expectedText.encode("utf-8")
        feedDL = FeedDownloader(r"notNecessary")
        feedDL.loadFeed("./Tests/testFeed.pickle")
        feed = feedDL.getFeed()
        self.textComposer.addFeed(feed)
        stringText = str(self.textComposer)[:len(expectedText)]
        getTextText = self.textComposer.getText()[:len(expectedText)]
        self.assertEqual(stringText, expectedText)
        self.assertEqual(getTextText, expectedText)

    def tearDown(self):
        self.textComposer = None


class test_textComposerGreeting(unittest.TestCase):
    def setUp(self):
        self.greeting = "Hi\nThis is a test text\n"
        self.textComposer = TextComposer(self.greeting)

    def test_noFeedGreeting(self):
        self.assertEqual(str(self.textComposer), self.greeting)
        self.assertEqual(self.textComposer.getText(), self.greeting)

    def test_testFeedGreeting(self):
        expectedText = (self.greeting + "\n"
                        + u"Combinations of Adaptive Filters with Coefficients"
                          u" Feedback\n"
                          u"Luiz F. O. Chamon, Cassio G. Lopes\n"
                          u"http://arxiv.org/abs/1608.03248v1\n"
                          u"Parallel combinations of adaptive filters have "
                          u"been effectively used to\nimprove the performance "
                          u"of adaptive algorithms and address typical trade-"
                          u"offs,\nsuch as the one between convergence rate "
                          u"and steady-state error. In these\ncombinations, "
                          u"the component filters are usually run "
                          u"independently and then\ncombined, which leads to a"
                          u" well known convergence stagnation effect.\n"
                          u"Conditional transfers of coefficients between "
                          u"filters were introduced in an\nattempt to handle "
                          u"this issue. This work introduces a more natural "
                          u"way of\naccelerating convergence to steady-state "
                          u"by cyclically feeding back the overall\n"
                          u"coefficients to all component filters. Besides "
                          u"coping with convergence\nstagnation, this new "
                          u"topology allows several adaptive algorithms (e.g.,"
                          u" mixed\nnorm, data reusing, and variable step "
                          u"size) to be posed as combinations of\nsimple "
                          u"adaptive filters, bridging an important conceptual"
                          u" gap. Steady-state "
                          u"and\ntracking analysis accounting for a myriad of "
                          u"component filters are derived for\ncombinations "
                          u"with and without feedback. Transient analyses of "
                          u"the typical\nconvex and affine supervisors are "
                          u"extended to general activation functions and\n"
                          u"applied to combinations with cyclic coefficients "
                          u"feedback. Numerical examples\nare provided to "
                          u"illustrate how coefficients feedback can improve "
                          u"the\nperformance of several existing parallel "
                          u"combinations at a small additional\ncomputational "
                          u"cost.\n\n"
                          u"Valid population inference for information-based "
                          u"imaging: From the\n  second-level $t$-test to "
                          u"prevalence inference\n"
                          u"Carsten Allefeld, Kai G\xf6rgen, "
                          u"John-Dylan Haynes\n")
        if not isinstance(expectedText, str):
            expectedText = expectedText.encode("utf-8")
        feedDL = FeedDownloader(r"notNecessary")
        feedDL.loadFeed("./Tests/testFeed.pickle")
        feed = feedDL.getFeed()
        self.textComposer.addFeed(feed)
        stringText = str(self.textComposer)[:len(expectedText)]
        getTextText = self.textComposer.getText()[:len(expectedText)]
        self.assertEqual(stringText, expectedText)
        self.assertEqual(getTextText, expectedText)

    def tearDown(self):
        self.textComposer = None
        self.greeting = None


if __name__ == "__main__":
    unittest.main()
