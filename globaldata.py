import platform
import os

REPORT_DIR = os.getcwd() + "/reports/"
SCREENSHOT_DIR = os.getcwd() + "/reports/screenshots/"
CHROME_DRIVER_DIR = os.environ["CHROME_DRIVER_DIR"]
FIREFOX_BINARY_PATH = os.environ["FIREFOX_BINARY_PATH"]
IE_DRIVER_DIR = "/Users/Briel/qa/common/IEDriverServer.exe"
SELENIUM = "selenium"

STG = 'stg'
PROD = 'prod'
DEV = 'dev'
QA = 'qa'

CHROME = 'chrome'
FF = 'firefox'
SAFARI = 'safari'
PHANTOMJS = 'phantomjs'
IE = 'ie11'
IPHONE = 'iphone'
IPAD = 'ipad'
HEADLESS = 'headless'
SAUCE = 'sauce'
SAUCE_CHROME = 'sauce_chrome'
SAUCE_FIREFOX = 'sauce_firefox'
SAUCE_IE8 = 'sauce_ie8'
SAUCE_IE9 = 'sauce_ie9'
SAUCE_IE10 = 'sauce_ie10'
SAUCE_IE11 = 'sauce_ie11'
SAUCE_IPHONE = 'sauce_iphone'
SAUCE_IPAD = 'sauce_ipad'
BROWSER_LIST = [CHROME, FF, SAFARI, IE, IPHONE, IPAD, SAUCE_CHROME,
                SAUCE_FIREFOX, SAUCE_IE11, SAUCE_IPHONE, SAUCE_IPAD, PHANTOMJS]
BROWSER_HELP = '''Browser to run tests on.  All options are listed in basetestcase.py,
and include one of the following (no quotes): ''' + str(BROWSER_LIST)

PUBLISH_HELP = "Optional True or False argument to publish results to a junitxml file (defaults to False)."

ID = "ID"
LT = "LINK_TEXT"
PLT = "PARTIAL_LINK_TEXT"
NAME = "NAME"
TAG = "TAG_NAME"
CN = "CLASS_NAME"
CSS = "CSS_SELECTOR"
XPATH = "XPATH"

TIMEOUT = 20
TIMEOUTSHORT = 10
TIMEOUTSHORTEST = 5
TIMEOUTLONG = 50
TIMEOUT_RETRY_INTERVAL = 0.1
TRANSFORM_TRANSITION_TIME = 1
LONG_TRANSITION_TIME = 2

FAILURE_MSG = "FAILED - The following verifications failed:\n"

def payment_type(self, type_payment='visa_success'):
    type_payment = type_payment.lower()

    if type_payment == 'visa_success':
        payment_type = {
            'cc' : ['4000100011112224', '123', '09', '19']
        }
        return payment_type

    elif type_payment == 'visa_decline':
        payment_type = {
            'cc' : [ '4000300011112220', '999', '09', '19']
        }
        return payment_type

    elif type_payment == 'master_success':
        payment_type = {
            'cc' : [ '5555444433332226', '999', '09', '19']
        }
        return payment_type

    elif type_payment == 'discover_success':
        payment_type = {
            'cc' : [ '6011222233332224', '09', '19', '999']
        }
        return payment_type

    elif type_payment == 'ach_success':
        payment_type = {
            'check' : ['wells', '091000019', '123456789', 'checking']
        }
        return payment_type

    elif type_payment == 'paper_success':
        payment_type = {
            'check' : ['usbank', '091000022', '123456789', 'checking']
        }
        return payment_type

    else:
        return False
