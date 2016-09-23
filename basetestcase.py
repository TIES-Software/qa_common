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


    @classmethod
    def getDriver(cls):

        sauce_username = cls.saucelabs.split("_")[0]
        sauce_accesskey = cls.saucelabs.split("_")[1]
        saucelabs_url = "http://" + sauce_username + ":" + sauce_accesskey  + "@ondemand.saucelabs.com:80/wd/hub"

        #ANDROID emulator or actual device
        if (cls.base_browser == 'android'):
            desired_capabilities = webdriver.DesiredCapabilities.ANDROID
            desired_capabilities['version'] = '4'
            desired_capabilities['platform'] = 'LINUX'
            cls.driver = webdriver.Remote(
                desired_capabilities=desired_capabilities,
                command_executor="http://localhost:8080/wd/hub"
            )


        #IPAD EMULATOR WITH APPIUM
        elif (cls.base_browser == 'ipad'):

            app = "/Users/Briel/Library/Developer/Xcode/DerivedData/ipad-emulator-ios8-alkwrhqevienelfrdxfpnpqzwpfh/Build/Products/Debug-iphonesimulator/ipad-emulator-ios8.app"
            cls.driver = webdriver.Remote(
                        command_executor='http://127.0.0.1:4723/wd/hub',
                        desired_capabilities={
                            'platformName': 'iOS',
                            'deviceName': 'iPad Simulator',
                            'platformVersion': '8.1',
                            'app': app,
                            'browserName' : "Safari"
                        }
            )


        #IPHONE EMULATOR WITH APPIUM
        elif (cls.base_browser == 'iphone'):

            app = "PATH TO IPHONE EMULATOR APP"
            cls.driver = webdriver.Remote(
                        command_executor='http://127.0.0.1:4723/wd/hub',
                        desired_capabilities={
                            'platformName': 'iOS',
                            'deviceName': 'iPhone Simulator',
                            'platformVersion': '8.1',
                            'app': app,
                            'browserName' : "Safari"
                        }
            )


        elif (cls.base_browser == 'phantomjs'):
            cls.driver = webdriver.PhantomJS(executable_path='/usr/bin/phantomjs-1.9.8-linux-x86_64/bin/phantomjs')

        elif (cls.base_browser == 'firefox'):
            cls.driver = webdriver.Firefox()

        elif (cls.base_browser == 'ie11'):
            #Forcing path of IEDriver to point to 32 bit version due to:
            #https://code.google.com/p/selenium/issues/detail?id=3072
            iedriver = globaldata.IE_DRIVER_DIR
            cls.driver = webdriver.Ie(executable_path=iedriver)

        elif (cls.base_browser == 'ie10'):
            cls.driver = webdriver.Ie()

        elif (cls.base_browser == 'ie9'):
            cls.driver = webdriver.Ie()

        elif (cls.base_browser == 'ie8'):
            cls.driver = webdriver.Ie()

        elif (cls.base_browser == 'safari'):
            cls.driver = webdriver.Safari()

        elif (cls.base_browser == 'chrome'):

            chromedriver = globaldata.CHROME_DRIVER_DIR
            os.environ["webdriver.chrome.driver"] = chromedriver
            options = webdriver.ChromeOptions()
            #Deals with chrome flag
            options.add_argument("--test-type")
            options.add_argument("--disable-popup-blocking")
            cls.driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=options)



        #=========================================================================
        #SAUCELABS CONFIGURATIONS

        elif (cls.base_browser == 'sauce_iphone'):
            desired_capabilities = webdriver.DesiredCapabilities.IPHONE
            desired_capabilities['version'] = '7'
            desired_capabilities['platform'] = 'OS X 10.9'
            desired_capabilities['device-orientation'] = 'portrait'
            desired_capabilities['name'] = cls.test_title
            cls.driver = webdriver.Remote(
                desired_capabilities=desired_capabilities,
                command_executor=saucelabs_url
            )


        elif (cls.base_browser == 'sauce_ipad'):
            desired_capabilities = webdriver.DesiredCapabilities.IPAD
            desired_capabilities['version'] = '7'
            desired_capabilities['platform'] = 'OS X 10.9'
            desired_capabilities['device-orientation'] = 'portrait'
            desired_capabilities['name'] = cls.test_title
            cls.driver = webdriver.Remote(
                desired_capabilities=desired_capabilities,
                command_executor=saucelabs_url
            )

        elif (cls.base_browser == 'sauce_ipad6'):
            desired_capabilities = webdriver.DesiredCapabilities.IPAD
            desired_capabilities['version'] = '6.1'
            desired_capabilities['platform'] = 'OS X 10.8'
            desired_capabilities['device-orientation'] = 'portrait'
            desired_capabilities['name'] = cls.test_title
            cls.driver = webdriver.Remote(
                desired_capabilities=desired_capabilities,
                command_executor=saucelabs_url
            )

        elif (cls.base_browser == 'sauce_ipad5'):
            desired_capabilities = webdriver.DesiredCapabilities.IPAD
            desired_capabilities['version'] = '5.1'
            desired_capabilities['platform'] = 'OS X 10.8'
            desired_capabilities['device-orientation'] = 'portrait'
            desired_capabilities['name'] = cls.test_title
            cls.driver = webdriver.Remote(
                desired_capabilities=desired_capabilities,
                command_executor=saucelabs_url
            )

        elif (cls.base_browser == 'sauce_android'):
            desired_capabilities = webdriver.DesiredCapabilities.ANDROID
            desired_capabilities['version'] = '4'
            desired_capabilities['platform'] = 'LINUX'
            desired_capabilities['name'] = cls.test_title
            cls.driver = webdriver.Remote(
                desired_capabilities=desired_capabilities,
                command_executor=saucelabs_url
            )

        elif (cls.base_browser == 'sauce_chrome'):
            desired_capabilities = webdriver.DesiredCapabilities.CHROME
            desired_capabilities['version'] = '33'
            desired_capabilities['platform'] = 'Windows 7'
            desired_capabilities['name'] = cls.test_title
            cls.driver = webdriver.Remote(
                desired_capabilities=desired_capabilities,
                command_executor=saucelabs_url
            )

        elif (cls.base_browser == 'sauce_firefox'):
            desired_capabilities = webdriver.DesiredCapabilities.FIREFOX
            desired_capabilities['version'] = '28'
            desired_capabilities['platform'] = 'Windows 7'
            desired_capabilities['name'] = cls.test_title
            cls.driver = webdriver.Remote(
                desired_capabilities=desired_capabilities,
                command_executor=saucelabs_url
            )

        elif (cls.base_browser == 'sauce_ie8'):
            desired_capabilities = webdriver.DesiredCapabilities.INTERNETEXPLORER
            desired_capabilities['version'] = '8'
            desired_capabilities['platform'] = 'Windows XP'
            desired_capabilities['name'] = cls.test_title
            desired_capabilities['avoid-proxy'] = 'true'
            cls.driver = webdriver.Remote(
                desired_capabilities=desired_capabilities,
                command_executor=saucelabs_url
            )

        elif (cls.base_browser == 'sauce_ie9'):
            desired_capabilities = webdriver.DesiredCapabilities.INTERNETEXPLORER
            desired_capabilities['version'] = '9'
            desired_capabilities['platform'] = 'Windows 7'
            desired_capabilities['name'] = cls.test_title
            desired_capabilities['avoid-proxy'] = 'true'
            cls.driver = webdriver.Remote(
                desired_capabilities=desired_capabilities,
                command_executor=saucelabs_url
            )

        elif (cls.base_browser == 'sauce_ie10'):
            desired_capabilities = webdriver.DesiredCapabilities.INTERNETEXPLORER
            desired_capabilities['version'] = '10'
            desired_capabilities['platform'] = 'Windows 7'
            desired_capabilities['name'] = cls.test_title
            desired_capabilities['avoid-proxy'] = 'true'
            cls.driver = webdriver.Remote(
                desired_capabilities=desired_capabilities,
                command_executor=saucelabs_url
            )

        elif (cls.base_browser == 'sauce_ie11'):
            desired_capabilities = webdriver.DesiredCapabilities.INTERNETEXPLORER
            desired_capabilities['version'] = '11'
            desired_capabilities['platform'] = 'Windows 8.1'
            desired_capabilities['name'] = cls.test_title
            desired_capabilities['avoid-proxy'] = 'true'
            cls.driver = webdriver.Remote(
                desired_capabilities=desired_capabilities,
                command_executor=saucelabs_url
            )

        elif (cls.base_browser == 'sauce_safari'):
            desired_capabilities = webdriver.DesiredCapabilities.SAFARI
            desired_capabilities['version'] = '7'
            desired_capabilities['platform'] = 'OS X 10.9'
            desired_capabilities['name'] = cls.test_title
            cls.driver = webdriver.Remote(
                desired_capabilities=desired_capabilities,
                command_executor=saucelabs_url
            )

        #=========================================================================

        return cls.driver
