# -*- coding: utf-8 -*-
import unittest
from qa_common import globaldata
import base64
from qa_common import commonfunctions as cf
try:
    import json
except ImportError:
    import simplejson as json


class BaseTestCase (unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        driver = cf.get_driver(cls.base_browser, cls.jenkins, cls.base_site)
        cls.driver = driver
        cf.driver_browser_info(driver)
        # return driver # RonC: why need to return?

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    # @classmethod
    # def getDriver(cls):

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
            # base64string = base64.encodebytes('%s:%s' % (config['username'], config['access-key']))[:-1]
            # encodestring function even deprecated but still can use or replace by the upper line
            base64string = base64.encodestring('%s:%s' % (config['username'], config['access-key']))[:-1]

            if failed:
                passed = False
            else:
                passed = True

            print("SauceOnDemandSessionID=" + jobid + " job-name=" + self.test_title)

            body_content = json.dumps({"passed": passed})
            try:
                import http.client # Python3
                connection = http.client.HTTPConnection("saucelabs.com")
            except ImportError:
                import httplib   # Python2 and was rename http.client in Python3
                connection = httplib.HTTPConnection("saucelabs.com")
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
