import platform
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

REPORT_DIR = os.getcwd() + "/reports/"
SCREENSHOT_DIR = os.getcwd() + "/reports/screenshots/"
CHROME_DRIVER_DIR = os.environ["CHROME_DRIVER_DIR"]
FIREFOX_DRIVER_DIR = os.environ["FIREFOX_DRIVER_DIR"]
GECKO_DRIVER = os.environ["FIREFOX_DRIVER_DIR"]

os_type = platform.system().lower()
if os_type == 'linux':
    GECKO_DRIVER = os.environ["GECKO_DRIVER"] + "/geckodriver"
elif os_type == 'windows':
    GECKO_DRIVER = os.environ["GECKO_DRIVER"] + "geckodriver"
elif os_type == 'darwin':
    GECKO_DRIVER = os.environ["GECKO_DRIVER"] + "/geckodriver"
else:
    GECKO_DRIVER = ''
    print('No gecko driver path for OS type of ' + os_type)

IE_DRIVER_DIR = "/Users/Briel/qa/common/IEDriverServer.exe"
SELENIUM = "selenium"

STG = 'stg'
PROD = 'prod'
DEV = 'dev'
QA = 'qa'

DEV_DEV = 'dev_dev'
DEV_REL = 'dev_rel'
DEV_HOT = 'dev_hot'
TEST_DEV = 'test_dev'
TEST_REL = 'test_rel'
TEST_HOT = 'test_hot'

CHROME = 'chrome'
CHROME_BETA = 'chrome_beta'
CHROME_STABLE = 'chrome_stable'
CHROME_HEADLESS = 'chrome_headless'
CHROME_BETA_HEADLESS = 'chrome_beta_headless'
CHROME_STABLE_HEADLESS = 'chrome_stable_headless'
FIREFOX_HEADLESS = 'firefox_headless'
FIREFOX_BETA = 'firefox_beta'
FIREFOX_STABLE = 'firefox_stable'
FIREFOX_BETA_HEADLESS = 'firefox_beta_headless'
FIREFOX_STABLE_HEADLESS = 'firefox_stable_headless'

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
BROWSER_LIST = [CHROME, CHROME_BETA, CHROME_BETA_HEADLESS, CHROME_STABLE, CHROME_STABLE_HEADLESS, CHROME_HEADLESS, FF, FIREFOX_BETA, FIREFOX_STABLE, FIREFOX_BETA_HEADLESS, FIREFOX_STABLE_HEADLESS, SAFARI, IE, IPHONE, IPAD, SAUCE_CHROME,
                SAUCE_FIREFOX, SAUCE_IE11, SAUCE_IPHONE, SAUCE_IPAD, PHANTOMJS, FIREFOX_HEADLESS]
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

#if 'feepay' in dir_path:
TIMEOUT = 4
TIMEOUTSHORT = 1
TIMEOUTSHORTEST = .25
TIMEOUTLONG = 8
TIMEOUT_RETRY_INTERVAL = 0.1
TRANSFORM_TRANSITION_TIME = 1
LONG_TRANSITION_TIME = 2
#else:
    #TIMEOUT = 20
    #TIMEOUTSHORT = 10
    #TIMEOUTSHORTEST = 5
    #TIMEOUTLONG = 50
    #TIMEOUT_RETRY_INTERVAL = 0.1
    #TRANSFORM_TRANSITION_TIME = 1
    #LONG_TRANSITION_TIME = 2

FAILURE_MSG = "FAILED - The following verifications failed:\n"
