#!/usr/bin/env python3

import unittest
from wphost import LineProcessor


class TestWpHost(unittest.TestCase):
    def setUp(self):
        pass

    maxDiff = None

    # @unittest.skip("skipping...")
    def testBasicTextLinks(self):
        lp = LineProcessor('local.dev', 'example.org', 'link')

        str1 = 'Links: <a href="http://local.dev/about">link</a>, ' \
               '<a href="https://local.dev">another one</a>. ' \
               'Not a link: local.dev'
        str2 = 'Links: <a href="http://example.org/about">link</a>, ' \
               '<a href="https://example.org">another one</a>. ' \
               'Not a link: local.dev'
        self.assertEqual(lp.process(str1), (str2, 2, 0))

    # @unittest.skip("skipping...")
    def testBasicTextLinks2(self):
        lp = LineProcessor('local.dev/one-blog', 'example.org/another-one', 'link')

        str1 = 'Links: <a href="http://local.dev/one-blog/about">link</a>, ' \
               '<a href="https://local.dev/one-blog">another one</a>. ' \
               'Not a link: local.dev'
        str2 = 'Links: <a href="http://example.org/another-one/about">link</a>, ' \
               '<a href="https://example.org/another-one">another one</a>. ' \
               'Not a link: local.dev'
        self.assertEqual(lp.process(str1), (str2, 2, 0))

    # @unittest.skip("skipping...")
    def testBasicTextEmails(self):
        lp = LineProcessor('local.dev', 'example.org', 'email')

        str1 = 'Emails: <a href="mailto:info@local.dev">info@local.dev</a>, ' \
               '<a href="mailto:info@other.dev">another one</a> ' \
               'in local.dev'
        str2 = 'Emails: <a href="mailto:info@example.org">info@example.org</a>, ' \
               '<a href="mailto:info@other.dev">another one</a> ' \
               'in local.dev'
        self.assertEqual(lp.process(str1), (str2, 2, 0))

    # @unittest.skip("skipping...")
    def testBasicTextBoth(self):
        lp = LineProcessor('local.dev', 'example.org', 'both')

        str1 = 'Both: <a href="http://local.dev/about">link</a>, ' \
               '<a href="mailto:info@local.dev">info@local.dev</a> ' \
               'in local.dev'
        str2 = 'Both: <a href="http://example.org/about">link</a>, ' \
               '<a href="mailto:info@example.org">info@example.org</a> ' \
               'in local.dev'

        self.assertEqual(lp.process(str1), (str2, 3, 0))

    # @unittest.skip("skipping...")
    def testSerializedText(self):
        lp = LineProcessor('www.development.net', 'www.production.com', 'link')

        str1 = 'a:6:{s:4:"file";s:43:"Depositphotos_15690599_original-940x198.jpg";s:5:"width";i:940;s:6:"height";i:198;s:9:"mime-type";s:10:"image/jpeg";s:4:"path";s:51:"2014/02/Depositphotos_15690599_original-940x198.jpg";s:3:"url";s:97:"http://www.development.net/wp-content/uploads/2014/02/Depositphotos_15690599_original-940x198.jpg";}' \
               'a:6:{s:4:"file";s:23:"mg_3358-1-6-312x416.jpg";s:5:"width";i:312;s:6:"height";i:416;s:9:"mime-type";s:10:"image/jpeg";s:4:"path";s:31:"2013/06/mg_3358-1-6-312x416.jpg";s:3:"url";s:77:"http://www.development.net/wp-content/uploads/2013/06/mg_3358-1-6-312x416.jpg";}'
        str2 = 'a:6:{s:4:"file";s:43:"Depositphotos_15690599_original-940x198.jpg";s:5:"width";i:940;s:6:"height";i:198;s:9:"mime-type";s:10:"image/jpeg";s:4:"path";s:51:"2014/02/Depositphotos_15690599_original-940x198.jpg";s:3:"url";s:96:"http://www.production.com/wp-content/uploads/2014/02/Depositphotos_15690599_original-940x198.jpg";}' \
               'a:6:{s:4:"file";s:23:"mg_3358-1-6-312x416.jpg";s:5:"width";i:312;s:6:"height";i:416;s:9:"mime-type";s:10:"image/jpeg";s:4:"path";s:31:"2013/06/mg_3358-1-6-312x416.jpg";s:3:"url";s:76:"http://www.production.com/wp-content/uploads/2013/06/mg_3358-1-6-312x416.jpg";}'
        self.assertEqual(lp.process(str1), (str2, 0, 2))

    # @unittest.skip("skipping...")
    def testSerializedText2(self):
        lp = LineProcessor('www.development.net/wp-content', 'www.production.com/whatever/wp-content', 'link')

        str1 = 'a:6:{s:4:"file";s:43:"Depositphotos_15690599_original-940x198.jpg";s:5:"width";i:940;s:6:"height";i:198;s:9:"mime-type";s:10:"image/jpeg";s:4:"path";s:51:"2014/02/Depositphotos_15690599_original-940x198.jpg";s:3:"url";s:97:"http://www.development.net/wp-content/uploads/2014/02/Depositphotos_15690599_original-940x198.jpg";}' \
               'a:6:{s:4:"file";s:23:"mg_3358-1-6-312x416.jpg";s:5:"width";i:312;s:6:"height";i:416;s:9:"mime-type";s:10:"image/jpeg";s:4:"path";s:31:"2013/06/mg_3358-1-6-312x416.jpg";s:3:"url";s:77:"http://www.development.net/wp-content/uploads/2013/06/mg_3358-1-6-312x416.jpg";}'
        str2 = 'a:6:{s:4:"file";s:43:"Depositphotos_15690599_original-940x198.jpg";s:5:"width";i:940;s:6:"height";i:198;s:9:"mime-type";s:10:"image/jpeg";s:4:"path";s:51:"2014/02/Depositphotos_15690599_original-940x198.jpg";s:3:"url";s:105:"http://www.production.com/whatever/wp-content/uploads/2014/02/Depositphotos_15690599_original-940x198.jpg";}' \
               'a:6:{s:4:"file";s:23:"mg_3358-1-6-312x416.jpg";s:5:"width";i:312;s:6:"height";i:416;s:9:"mime-type";s:10:"image/jpeg";s:4:"path";s:31:"2013/06/mg_3358-1-6-312x416.jpg";s:3:"url";s:85:"http://www.production.com/whatever/wp-content/uploads/2013/06/mg_3358-1-6-312x416.jpg";}'
        self.assertEqual(lp.process(str1), (str2, 0, 2))

    # @unittest.skip("skipping...")
    def testSerializedQuotedText(self):
        lp = LineProcessor('www.development.net', 'www.production.com', 'link')

        str1 = r'a:6:{s:4:\"file\";s:43:\"Depositphotos_15690599_original-940x198.jpg\";s:5:\"width\";i:940;s:6:\"height\";i:198;s:9:\"mime-type\";s:10:\"image/jpeg\";s:4:\"path\";s:51:\"2014/02/Depositphotos_15690599_original-940x198.jpg\";s:3:\"url\";s:97:\"http://www.development.net/wp-content/uploads/2014/02/Depositphotos_15690599_original-940x198.jpg\";}' \
               r'a:6:{s:4:\"file\";s:23:\"mg_3358-1-6-312x416.jpg\";s:5:\"width\";i:312;s:6:\"height\";i:416;s:9:\"mime-type\";s:10:\"image/jpeg\";s:4:\"path\";s:31:\"2013/06/mg_3358-1-6-312x416.jpg\";s:3:\"url\";s:77:\"http://www.development.net/wp-content/uploads/2013/06/mg_3358-1-6-312x416.jpg\";}'
        str2 = r'a:6:{s:4:\"file\";s:43:\"Depositphotos_15690599_original-940x198.jpg\";s:5:\"width\";i:940;s:6:\"height\";i:198;s:9:\"mime-type\";s:10:\"image/jpeg\";s:4:\"path\";s:51:\"2014/02/Depositphotos_15690599_original-940x198.jpg\";s:3:\"url\";s:96:\"http://www.production.com/wp-content/uploads/2014/02/Depositphotos_15690599_original-940x198.jpg\";}' \
               r'a:6:{s:4:\"file\";s:23:\"mg_3358-1-6-312x416.jpg\";s:5:\"width\";i:312;s:6:\"height\";i:416;s:9:\"mime-type\";s:10:\"image/jpeg\";s:4:\"path\";s:31:\"2013/06/mg_3358-1-6-312x416.jpg\";s:3:\"url\";s:76:\"http://www.production.com/wp-content/uploads/2013/06/mg_3358-1-6-312x416.jpg\";}'
        self.assertEqual(lp.process(str1), (str2, 0, 2))

    # @unittest.skip("skipping...")
    def testSerializedQuotedText2(self):
        lp = LineProcessor('www.development.net/wp-content', 'www.production.com/whatever/wp-content', 'link')

        str1 = r'a:6:{s:4:\"file\";s:43:\"Depositphotos_15690599_original-940x198.jpg\";s:5:\"width\";i:940;s:6:\"height\";i:198;s:9:\"mime-type\";s:10:\"image/jpeg\";s:4:\"path\";s:51:\"2014/02/Depositphotos_15690599_original-940x198.jpg\";s:3:\"url\";s:97:\"http://www.development.net/wp-content/uploads/2014/02/Depositphotos_15690599_original-940x198.jpg\";}' \
               r'a:6:{s:4:\"file\";s:23:\"mg_3358-1-6-312x416.jpg\";s:5:\"width\";i:312;s:6:\"height\";i:416;s:9:\"mime-type\";s:10:\"image/jpeg\";s:4:\"path\";s:31:\"2013/06/mg_3358-1-6-312x416.jpg\";s:3:\"url\";s:77:\"http://www.development.net/wp-content/uploads/2013/06/mg_3358-1-6-312x416.jpg\";}'
        str2 = r'a:6:{s:4:\"file\";s:43:\"Depositphotos_15690599_original-940x198.jpg\";s:5:\"width\";i:940;s:6:\"height\";i:198;s:9:\"mime-type\";s:10:\"image/jpeg\";s:4:\"path\";s:51:\"2014/02/Depositphotos_15690599_original-940x198.jpg\";s:3:\"url\";s:105:\"http://www.production.com/whatever/wp-content/uploads/2014/02/Depositphotos_15690599_original-940x198.jpg\";}' \
               r'a:6:{s:4:\"file\";s:23:\"mg_3358-1-6-312x416.jpg\";s:5:\"width\";i:312;s:6:\"height\";i:416;s:9:\"mime-type\";s:10:\"image/jpeg\";s:4:\"path\";s:31:\"2013/06/mg_3358-1-6-312x416.jpg\";s:3:\"url\";s:85:\"http://www.production.com/whatever/wp-content/uploads/2013/06/mg_3358-1-6-312x416.jpg\";}'
        self.assertEqual(lp.process(str1), (str2, 0, 2))

    # @unittest.skip("skipping...")
    def testSerializedHtml(self):
        lp = LineProcessor('developer-site.net', 'productionsite.com', 'link')

        str1 = r's:297:\"<div style=\"background-color:#1C2D3F\"><iframe src=\"http://developer-site.net/en/site/widget?type=search&amp;city=1&amp;ref=bhdirectorysearch\" scrolling=\"no\" style=\"display: block; overflow: hidden; border: none; padding: 0; margin: 0 auto;\" frameborder=\"0\" height=\"275\" width=\"230\"></iframe></div>\";s:6:\"filter\";'
        str2 = r's:297:\"<div style=\"background-color:#1C2D3F\"><iframe src=\"http://productionsite.com/en/site/widget?type=search&amp;city=1&amp;ref=bhdirectorysearch\" scrolling=\"no\" style=\"display: block; overflow: hidden; border: none; padding: 0; margin: 0 auto;\" frameborder=\"0\" height=\"275\" width=\"230\"></iframe></div>\";s:6:\"filter\";'
        self.assertEqual(lp.process(str1), (str2, 0, 1))

    # @unittest.skip("skipping...")
    def testSerializedMultipleMatches(self):
        lp = LineProcessor('www.development.net', 'www.production.com', 'link')
        str1 = 'a:6:{s:4:"file";s:43:"Depositphotos_15690599_original-940x198.jpg";s:5:"width";i:940;s:6:"height";i:198;s:9:"mime-type";s:10:"image/jpeg";s:4:"path";s:51:"2014/02/Depositphotos_15690599_original-940x198.jpg";s:3:"url";s:97:"http://www.development.net/wp-content/uploads/2014/02/Depositphotos_15690599_original-940x198.jpg";}' \
               'a:6:{s:4:"file";s:23:"mg_3358-1-6-312x416.jpg";s:5:"width";i:312;s:6:"height";i:416;s:9:"mime-type";s:10:"image/jpeg";s:4:"path";s:31:"2013/06/mg_3358-1-6-312x416.jpg";s:3:"url";s:163:"|||http://www.development.net/wp-content/uploads/2013/06/mg_3358-1-6-312x416.jpg|||http://www.development.net/wp-content/uploads/2013/06/mg_3358-1-6-312x416.jpg|||";}'
        str2 = 'a:6:{s:4:"file";s:43:"Depositphotos_15690599_original-940x198.jpg";s:5:"width";i:940;s:6:"height";i:198;s:9:"mime-type";s:10:"image/jpeg";s:4:"path";s:51:"2014/02/Depositphotos_15690599_original-940x198.jpg";s:3:"url";s:96:"http://www.production.com/wp-content/uploads/2014/02/Depositphotos_15690599_original-940x198.jpg";}' \
               'a:6:{s:4:"file";s:23:"mg_3358-1-6-312x416.jpg";s:5:"width";i:312;s:6:"height";i:416;s:9:"mime-type";s:10:"image/jpeg";s:4:"path";s:31:"2013/06/mg_3358-1-6-312x416.jpg";s:3:"url";s:161:"|||http://www.production.com/wp-content/uploads/2013/06/mg_3358-1-6-312x416.jpg|||http://www.production.com/wp-content/uploads/2013/06/mg_3358-1-6-312x416.jpg|||";}'
        self.assertEqual(lp.process(str1), (str2, 0, 3))

    # @unittest.skip("skipping...")
    def testMixed(self):
        lp = LineProcessor('development.net', 'production.com', 'both')

        str1 = '<a href="http://development.net/about">link</a>, ' \
               '<a href="mailto:info@development.net">info@development.net</a> ' \
               'a:6:{s:4:"file";s:43:"Depositphotos_15690599_original-940x198.jpg";s:5:"width";i:940;s:6:"height";i:198;s:9:"mime-type";s:10:"image/jpeg";s:4:"path";s:51:"2014/02/Depositphotos_15690599_original-940x198.jpg";s:3:"url";s:93:"http://development.net/wp-content/uploads/2014/02/Depositphotos_15690599_original-940x198.jpg";}' \
               'a:6:{s:4:"file";s:23:"mg_3358-1-6-312x416.jpg";s:5:"width";i:312;s:6:"height";i:416;s:9:"mime-type";s:10:"image/jpeg";s:4:"path";s:31:"2013/06/mg_3358-1-6-312x416.jpg";s:3:"url";s:73:"http://development.net/wp-content/uploads/2013/06/mg_3358-1-6-312x416.jpg";}'
        str2 = '<a href="http://production.com/about">link</a>, ' \
               '<a href="mailto:info@production.com">info@production.com</a> ' \
               'a:6:{s:4:"file";s:43:"Depositphotos_15690599_original-940x198.jpg";s:5:"width";i:940;s:6:"height";i:198;s:9:"mime-type";s:10:"image/jpeg";s:4:"path";s:51:"2014/02/Depositphotos_15690599_original-940x198.jpg";s:3:"url";s:92:"http://production.com/wp-content/uploads/2014/02/Depositphotos_15690599_original-940x198.jpg";}' \
               'a:6:{s:4:"file";s:23:"mg_3358-1-6-312x416.jpg";s:5:"width";i:312;s:6:"height";i:416;s:9:"mime-type";s:10:"image/jpeg";s:4:"path";s:31:"2013/06/mg_3358-1-6-312x416.jpg";s:3:"url";s:72:"http://production.com/wp-content/uploads/2013/06/mg_3358-1-6-312x416.jpg";}'
        self.assertEqual(lp.process(str1), (str2, 3, 2))

if __name__ == '__main__':
    unittest.main()

