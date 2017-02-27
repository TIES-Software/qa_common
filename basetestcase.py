# -*- coding: utf-8 -*-
from selenium import webdriver
#from selenium.webdriver.firefox.webdriver import FirefoxBinary
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
import unittest
import globaldata
import httplib
import sys
import base64
import os
import commonfunctions as cf

try:
    import json
except ImportError:
    import simplejson as json


class BaseTestCase (unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        driver = cls.getDriver()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    @classmethod
        def getDriver(cls):
        driver = cf.get_driver(cls.base_browser)
        cls.driver = driver
        return driver

    def set_test_status(self, failed, failure, **kwargs):

        if 'savescreenshot' in kwargs:
            import time
            filename = str( lambda: int(round(time.time() * 1000)))
            self.driver.save_screenshot(globaldata.SCREENSHOT_DIR + filename)

        if ('sauce' in self.base_browser):

            jobid = self.driver.session_id
            sauce_username = self.saucelabs.split("_")[0]
            sauce_accesskey = self.saucelabs.split("_")[1]

            config = {"username": sauce_username,
                      "access-key": sauce_accesskey}

            base64string = base64.encodestring('%s:%s' % (config['username'], config['access-key']))[:-1]

            if failed:
                passed = False
            else:
                passed = True

            print("SauceOnDemandSessionID=" + jobid + " job-name=" + self.test_title)

            body_content = json.dumps({"passed": passed})
            connection =  httplib.HTTPConnection("saucelabs.com")
            connection.request('PUT', '/rest/v1/%s/jobs/%s' % (config['username'], jobid),
                               body_content,
                               headers={"Authorization": "Basic %s" % base64string})
            result = connection.getresponse()
            return result.status == 200

        else:
            if failed:
                self.fail(msg=failure)
            else:
                print("PASSED.\n")
