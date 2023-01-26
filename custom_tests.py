#!/usr/bin/env python
# Copyright 2023 Shehraj Singh
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# run python freetests.py

from urllib import request
import unittest

BASEURL = "http://127.0.0.1:8080"

class TestYourWebserver(unittest.TestCase):
    def setUp(self,baseurl=BASEURL):
        """do nothing"""
        self.baseurl = baseurl

    def test_relativepath_noredirect(self):
        url = self.baseurl + "/deep/../"
        req = request.urlopen(url, None, 3)
        self.assertTrue( req.getcode()  == 200 , "200 OK Not FOUND!")
        self.assertTrue( req.info().get_content_type() == "text/html", ("Bad mimetype for html! %s" % req.info().get_content_type()))

    # def test_relativepath_redirect(self):
    #     url = self.baseurl + "/deep/.."
    #     req = request.urlopen(url, None, 3)
    #     self.assertTrue( req.getcode()  == 301 , "301 Moved Not FOUND!")

    def test_relativepath_noredirect(self):
        url = self.baseurl + "/../../../"
        try:
            req = request.urlopen(url, None, 3)
            self.assertTrue(False, "Should have thrown 404!")
        except request.HTTPError as e:
            self.assertTrue( e.getcode()  == 404 , "404 Not Found Not FOUND!")
        else:
            self.assertTrue(False, "Another error occurred")

    def test_incorrect_relative_path(self):
        url = self.baseurl + "/deep/../../../"
        try:
            req = request.urlopen(url, None, 3)
            self.assertTrue(False, "Should have thrown 404!")
        except request.HTTPError as e:
            self.assertTrue( e.getcode()  == 404 , "404 Not Found Not FOUND!")
        else:
            self.assertTrue(False, "Another error occurred")

if __name__ == '__main__':
    unittest.main()
