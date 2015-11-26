#!/usr/bin/env python3

import unittest
from wphost import LineProcessor


class TestWpHost(unittest.TestCase):
    def setUp(self):
        pass

    #@unittest.skip("skipping...")
    def testBasicTextLinks(self):
        lp = LineProcessor('local.dev', 'example.org', 'link')

        str1 =  'Links: <a href="http://local.dev/about">link</a>, ' \
                '<a href="https://local.dev">another one</a>. ' \
                'Not a link: local.dev'

        str2 =  'Links: <a href="http://example.org/about">link</a>, ' \
                '<a href="https://example.org">another one</a>. ' \
                'Not a link: local.dev'

        self.assertEqual(lp.process(str1), (str2, 2, 0))



    def testBasicTextEmails(self):
        lp = LineProcessor('local.dev', 'example.org', 'email')

        str1 =  'Emails: <a href="mailto:info@local.dev">info@local.dev</a>, ' \
                '<a href="mailto:info@other.dev">another one</a> ' \
                'in local.dev'

        str2 =  'Emails: <a href="mailto:info@example.org">info@example.org</a>, ' \
                '<a href="mailto:info@other.dev">another one</a> ' \
                'in local.dev'

        self.assertEqual(lp.process(str1), (str2, 2, 0))



    def testBasicTextBoth(self):
        lp = LineProcessor('local.dev', 'example.org', 'both')

        str1 =  'Both: <a href="http://local.dev/about">link</a>, ' \
                '<a href="mailto:info@local.dev">info@local.dev</a> ' \
                'in local.dev'

        str2 =  'Both: <a href="http://example.org/about">link</a>, ' \
                '<a href="mailto:info@example.org">info@example.org</a> ' \
                'in local.dev'

        self.assertEqual(lp.process(str1), (str2, 3, 0))



    def testSerializedText(self):
        lp = LineProcessor('www.development.net', 'www.production.com', 'link')

        str1 =  'a:6:{s:4:"file";s:43:"Depositphotos_15690599_original-940x198.jpg";s:5:"width";i:940;s:6:"height";i:198;s:9:"mime-type";s:10:"image/jpeg";s:4:"path";s:51:"2014/02/Depositphotos_15690599_original-940x198.jpg";s:3:"url";s:97:"http://www.development.net/wp-content/uploads/2014/02/Depositphotos_15690599_original-940x198.jpg";}' \
                'a:6:{s:4:"file";s:23:"mg_3358-1-6-312x416.jpg";s:5:"width";i:312;s:6:"height";i:416;s:9:"mime-type";s:10:"image/jpeg";s:4:"path";s:31:"2013/06/mg_3358-1-6-312x416.jpg";s:3:"url";s:77:"http://www.development.net/wp-content/uploads/2013/06/mg_3358-1-6-312x416.jpg";}'

        str2 =  'a:6:{s:4:"file";s:43:"Depositphotos_15690599_original-940x198.jpg";s:5:"width";i:940;s:6:"height";i:198;s:9:"mime-type";s:10:"image/jpeg";s:4:"path";s:51:"2014/02/Depositphotos_15690599_original-940x198.jpg";s:3:"url";s:96:"http://www.production.com/wp-content/uploads/2014/02/Depositphotos_15690599_original-940x198.jpg";}' \
                'a:6:{s:4:"file";s:23:"mg_3358-1-6-312x416.jpg";s:5:"width";i:312;s:6:"height";i:416;s:9:"mime-type";s:10:"image/jpeg";s:4:"path";s:31:"2013/06/mg_3358-1-6-312x416.jpg";s:3:"url";s:76:"http://www.production.com/wp-content/uploads/2013/06/mg_3358-1-6-312x416.jpg";}'

        self.assertEqual(lp.process(str1), (str2, 0, 2))



    def testMixed(self):
        lp = LineProcessor('development.net', 'production.com', 'both')

        str1 =  '<a href="http://development.net/about">link</a>, ' \
                '<a href="mailto:info@development.net">info@development.net</a> ' \
                'a:6:{s:4:"file";s:43:"Depositphotos_15690599_original-940x198.jpg";s:5:"width";i:940;s:6:"height";i:198;s:9:"mime-type";s:10:"image/jpeg";s:4:"path";s:51:"2014/02/Depositphotos_15690599_original-940x198.jpg";s:3:"url";s:93:"http://development.net/wp-content/uploads/2014/02/Depositphotos_15690599_original-940x198.jpg";}' \
                'a:6:{s:4:"file";s:23:"mg_3358-1-6-312x416.jpg";s:5:"width";i:312;s:6:"height";i:416;s:9:"mime-type";s:10:"image/jpeg";s:4:"path";s:31:"2013/06/mg_3358-1-6-312x416.jpg";s:3:"url";s:73:"http://development.net/wp-content/uploads/2013/06/mg_3358-1-6-312x416.jpg";}'

        str2 =  '<a href="http://production.com/about">link</a>, ' \
                '<a href="mailto:info@production.com">info@production.com</a> ' \
                'a:6:{s:4:"file";s:43:"Depositphotos_15690599_original-940x198.jpg";s:5:"width";i:940;s:6:"height";i:198;s:9:"mime-type";s:10:"image/jpeg";s:4:"path";s:51:"2014/02/Depositphotos_15690599_original-940x198.jpg";s:3:"url";s:92:"http://production.com/wp-content/uploads/2014/02/Depositphotos_15690599_original-940x198.jpg";}' \
                'a:6:{s:4:"file";s:23:"mg_3358-1-6-312x416.jpg";s:5:"width";i:312;s:6:"height";i:416;s:9:"mime-type";s:10:"image/jpeg";s:4:"path";s:31:"2013/06/mg_3358-1-6-312x416.jpg";s:3:"url";s:72:"http://production.com/wp-content/uploads/2013/06/mg_3358-1-6-312x416.jpg";}'

        self.assertEqual(lp.process(str1), (str2, 3, 2))


if __name__ == '__main__':
    unittest.main()