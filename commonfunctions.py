from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
import custom_EC
import time
import datetime
import string
import random
import globaldata
import calendar
import platform
import itertools

# FUNCTIONS
def get_driver(browser, jenkins=""):
    os_type = platform.system().lower()
    browser_path = os_browser_path(browser_type=browser)

    if (browser == 'chrome') or (browser == 'chrome_headless'):
        path_to_chrome_driver = globaldata.CHROME_DRIVER_DIR
        options = webdriver.ChromeOptions()
        #options.add_argument("--start-maximized")
        #size of a 13 inch desktop screen
        #options.add_argument("--window-size=1280,1500")
        options.add_argument("--test-type")
        options.add_argument("--disable-popup-blocking")
        options.add_argument('--ignore-certificate-errors')

        options.add_argument("--no-first-run")
        options.add_argument("--no-default-browser-check")
        options.add_argument("--disable-infobars")
        options.add_argument("--no-sandbox")
        options.add_argument("--enable-precise-memory-info")
        options.add_argument("--disable-setuid-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--aggressive-cache-discard")
        options.add_argument("--disable-single-click-autofill")
        options.add_argument("--verbose")
        options.add_argument("--disable-autofill-keyboard-accessory-view[8]")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument('--log-level=3')
        options.add_argument("--start-maximized")
        options.add_argument("--ignore-urlfetcher-cert-requests")
        options.add_argument("--ignore-ssl-errors=true")
        options.add_argument("--ssl-protocol=any")
        options.add_argument("--window-size=1920,1080")

        if 'headless' in browser:
            options.add_argument("--headless")

        options.add_experimental_option("useAutomationExtension", False)


        capabilities = DesiredCapabilities.CHROME
        capabilities['loggingPrefs'] = {'performance': 'ALL'}
        capabilities['acceptInsecureCerts'] = True


        if os_type =='linux':
            output_dir='/tmp'
            service_log_path = "/tmp/chromedriver.log".format(output_dir)
            driver = webdriver.Chrome(executable_path=path_to_chrome_driver, chrome_options=options, desired_capabilities=capabilities, service_log_path=service_log_path )
        else:
            driver = webdriver.Chrome(executable_path=path_to_chrome_driver, chrome_options=options, desired_capabilities=capabilities)

    # elif (browser == 'chrome_headless'):
    #     path_to_chrome_driver = globaldata.CHROME_DRIVER_DIR
    #     options = webdriver.ChromeOptions()
    #     options.add_argument("--test-type")
    #     options.add_argument("--disable-popup-blocking")
    #     options.add_argument("--headless")
    #     options.add_argument("--disable-gpu")
    #     options.add_argument("--no-sandbox")
    #     options.add_argument("--ignore-certificate-errors")
    #
    #     options.add_argument("--disable-infobars")
    #
    #     capabilities = DesiredCapabilities.CHROME
    #     capabilities['loggingPrefs'] = {'performance': 'ALL'}
    #     capabilities['acceptInsecureCerts'] = True
    #
    #     driver = webdriver.Chrome(executable_path=path_to_chrome_driver, chrome_options=options)

    elif (browser == 'firefox') or (browser == 'firefox_beta'):
        path_to_geckodriver = globaldata.FIREFOX_DRIVER_DIR
        options = FirefoxOptions()
        caps = DesiredCapabilities.FIREFOX
        path_to_geckodriver = globaldata.GECKO_DRIVER
        print('path to gecko driver = ' + path_to_geckodriver)

        caps["marionette"] = True
        profile = webdriver.FirefoxProfile()
        profile.accept_untrusted_certs = True
        driver = webdriver.Firefox(executable_path=path_to_geckodriver, capabilities=caps, firefox_options=options, firefox_profile=profile)

    elif (browser == 'firefox_headless') or (browser == 'firefox_headless_beta'):
        path_to_geckodriver = globaldata.FIREFOX_DRIVER_DIR
        options = FirefoxOptions()
        options.add_argument('--headless')

        caps = DesiredCapabilities.FIREFOX
        caps["marionette"] = True
        profile = webdriver.FirefoxProfile()
        profile.accept_untrusted_certs = True
        driver = webdriver.Firefox(executable_path=path_to_geckodriver, capabilities=caps, firefox_options=options, firefox_profile=profile)

    elif 'frontend' in self.site or 'admin' in self.site:
        if 'beta' in browser:
            options.binary_location = browser_path[0]
        else:
            options.binary_location = browser_path[1]
    else:
        print(browser + "is not an option")

    window_size = driver.get_window_size()
    print('\nWindow size is ' + str(window_size))
    print('\nbeta browser binary location is ' + str(browser_path[0]))
    print('\ncurrent browser binary location is ' + str(browser_path[1]))

    return driver


def get_by(what):
    by = By.ID
    if what == globaldata.LT:
        by = By.LINK_TEXT
    elif what == globaldata.PLT:
        by = By.PARTIAL_LINK_TEXT
    elif what == globaldata.NAME:
        by = By.NAME
    elif what == globaldata.TAG:
        by = By.TAG_NAME
    elif what == globaldata.CN:
        by = By.CLASS_NAME
    elif what == globaldata.CSS:
        by = By.CSS_SELECTOR
    elif what == globaldata.XPATH:
        by = By.XPATH
    return by


#def generate_id(size=8, chars=string.letters + string.digits):
def generate_id(size=8, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def get_unique_name():
    d = datetime.datetime.now()
    unique_name = str(d.strftime('%m'))
    unique_name = unique_name + str(d.strftime('%d'))
    unique_name = unique_name + str(d.year)
    unique_name = unique_name + str(d.strftime('%H'))
    unique_name = unique_name + str(d.strftime('%M'))
    return unique_name


def get_current_date_formatted():
    return time.strftime('%m/%d/%Y')


def get_current_date(date_format='%m/%d/%y'):
    return time.strftime(date_format)


def get_current_date_no_leading_zeros():
    return '{dt.month}/{dt.day}/{dt.year}'.format(dt=datetime.datetime.now())


def get_past_date(days_ago):
    return_date = datetime.datetime.now() - datetime.timedelta(days=days_ago)
    return return_date.strftime('%m/%d/%Y')


def get_past_date_no_lead_zeros(days_ago):
    return_date = datetime.datetime.now() - datetime.timedelta(days=days_ago)
    return return_date.strftime('%-m/%-d/%Y')


def get_future_date(days_in_future):
    return_date = datetime.datetime.now() + datetime.timedelta(days=days_in_future)
    return return_date.strftime('%m/%d/%Y')


def get_current_year():
    return '{dt.year}'.format(dt=datetime.datetime.now())

def month_nbr(month=''):
    if month == '':
        month = '{dt.month}'.format(dt=datetime.datetime.now())
    elif month.isdigit():
        month = month
    elif isinstance(month,str):
        month = month.lower()
        month_dict = {
            'jan': 1,
            'january' : 1,
            'feb' : 2,
            'february' : 2,
            'mar' : 3,
            'march' : 3,
            'apr' : 4,
            'april' : 4,
            'may' : 5,
            'jun' : 6,
            'june' : 6,
            'jul' : 7,
            'july' : 7,
            'aug' : 8,
            'august' : 8,
            'sep' : 9,
            'september' : 9,
            'sept' : 9,
            'oct' : 10,
            'october' : 10,
            'nov' : 11,
            'november' : 11,
            'dec' : 12,
            'december' : 12,
        }
        month = int(month_dict[month])
    else:
        print('The month Value passed in by caller is not an integer and or a string')
        return False

    return month

def start_date_of_month(month):
    if month == '':
        month = '{dt.month}'.format(dt=datetime.datetime.now())
    first_day = calendar.monthrange(int(get_current_year()), int(month))
    return first_day[0]

def end_date_of_month(month):
    if month == '':
        month = '{dt.month}'.format(dt=datetime.datetime.now())
    last_day = calendar.monthrange(int(get_current_year()), int(month))
    return last_day[1]

def get_current_time():
    return time.strftime("%H:%M:%S", time.gmtime())


def wait_for_jquery_inactive(self, script='return jQuery.active', timeout=globaldata.TIMEOUT):
    # waits until jQuery finishes executing
    poll_until(self, script, "0", timeout=globaldata.TIMEOUT)

######
# Window Handle Functions
######


def close_all_additional_windows(self):
    driver = self.driver
    while len(driver.window_handles) > 1:
            driver.switch_to.window(driver.window_handles[-1])
            driver.close()
    driver.switch_to.window(driver.window_handles[0])


def wait_for_handle_to_load_and_switch(self, handle_index, timeout=globaldata.TIMEOUT):
    driver = self.driver
    count = 0
    while ((len(driver.window_handles) <= handle_index) and count <= timeout):
        count = count + 1
        time.sleep(1)
    driver.switch_to_window(driver.window_handles[handle_index])


def wait_for_popup_window(self, expected_num_windows, timeout=globaldata.TIMEOUT):
    driver = self.driver
    wait = WebDriverWait(driver, timeout)
    if not wait.until(lambda driver: len(driver.window_handles) == expected_num_windows):
        print("Expected number of " + expected_num_windows + " windows to display in " + timeout + " seconds")
        return False
    else:
        return True


# def wait_for_popup_window(self, expected_num_windows, timeout=globaldata.TIMEOUT):
#     driver = self.driver
#     wait = WebDriverWait(driver, timeout)
#     new_window_present = wait.until(
#         lambda driver: len(driver.window_handles) == expected_num_windows)
#     return alert_visible


def wait_for_url(self, url, timeout=globaldata.TIMEOUT):
    driver = self.driver
    found = True
    first_time = time.time()
    last_time = first_time
    current_url = ""

    while (url not in current_url):
        try:
            current_url = driver.current_url
        except Exception as e:
            current_url = ""
            new_time = time.time()
            if new_time - last_time > timeout:
                found = False
                break
        return found


######
# Page Element Functions
######


def check_if_element_clickable(self, by, locator):
    return wait_for_element_clickable(self, by, locator, 1)


def wait_for_element_clickable(self, by, locator, timeout=globaldata.TIMEOUT):
    driver = self.driver
    wait = WebDriverWait(driver, timeout)
    by = get_by(by)

    try:
        clickable = wait.until(EC.element_to_be_clickable((by, locator)))
    except TimeoutException:
        clickable = False
    return clickable


def wait_for_element_and_click(self, by, locator, timeout=globaldata.TIMEOUT):
    driver = self.driver
    clickable = wait_for_element_clickable(self, by, locator, timeout)

    try:
        clickable.click()
        return True
    except Exception as e:
        print(e)
        return False


def wait_for_element_text_to_equal(self, by, locator, text_to_equal, timeout=globaldata.TIMEOUT):
    driver = self.driver
    wait = WebDriverWait(driver, timeout)
    by = get_by(by)

    try:
        text_equal = wait.until(custom_EC.exact_text_to_be_present_in_element((by, locator), text_to_equal))
    except TimeoutException:
        text_equal = False
    return text_equal


def wait_for_element_text_not_null(self, by, locator, timeout=globaldata.TIMEOUT):
    driver = self.driver
    wait = WebDriverWait(driver, timeout)
    by = get_by(by)

    try:
        element_not_null = wait.until(custom_EC.element_text_to_be_non_null((by, locator)))
    except TimeoutException:
        element_not_null = False
    return element_not_null


def wait_for_element_text_to_contain(self, by, locator, text_to_contain, timeout=globaldata.TIMEOUT):
    driver = self.driver
    wait = WebDriverWait(driver, timeout)
    by = get_by(by)

    try:
        text_present = wait.until(EC.text_to_be_present_in_element((by, locator), text_to_contain))
    except TimeoutException:
        text_present = False
    return text_present


def check_if_element_present(self, by, locator):
    timeout = 1
    return wait_for_element_present(self, by, locator, timeout)


def check_if_element_not_present(self, element):
    timeout = 1
    return wait_for_element_not_present(self, element, timeout)


def wait_for_element_present(self, by, locator, timeout=globaldata.TIMEOUT):
    driver = self.driver
    wait = WebDriverWait(driver, timeout)
    by = get_by(by)
    try:
        present = wait.until(EC.presence_of_element_located((by, locator)))
    except TimeoutException:
        present = False
    return present


def wait_for_element_not_present(self, element, timeout=globaldata.TIMEOUT):
    driver = self.driver
    wait = WebDriverWait(driver, timeout)
    try:
        stale = wait.until(EC.staleness_of(element))
    except TimeoutException:
        stale = False
    return stale


def check_if_element_visible(self, by, locator, timeout=globaldata.TIMEOUT):
    try:
        if wait_for_element_visible(self, by, locator, timeout):
            return True
        #else:
            #print('Failed to find element visible with the locator of ' + locator)
    except Exception as e:
        print('something went wrong trying to find element \n', e)
        return False


def check_if_element_not_visible(self, by, locator, timeout=globaldata.TIMEOUT):
    # timeout = 1
    return wait_for_element_not_visible(self, by, locator, timeout)


def wait_for_element_visible(self, by, locator, timeout=globaldata.TIMEOUT):
    driver = self.driver
    wait = WebDriverWait(driver, timeout)

    try:
        visible = wait.until(EC.visibility_of_element_located((get_by(by), locator)))
    except TimeoutException:
        visible = False
    return visible


def wait_for_element_not_visible(self, by, locator, timeout=globaldata.TIMEOUT):
    driver = self.driver
    wait = WebDriverWait(driver, timeout)

    try:
        not_visible = wait.until(EC.invisibility_of_element_located((get_by(by), locator)))
    except TimeoutException:
        not_visible = False
    return not_visible


######
# Iframe Operations
######

# needed for adminBeta testing
def wait_for_element_visible_in_iframe(self, iframe_id, by, locator, timeout=globaldata.TIMEOUT):
    driver = self.driver
    assert wait_for_element_visible(self, globaldata.ID, iframe_id, timeout), "iframe '" + iframe_id + "' not present in page"
    driver.switch_to.frame(iframe_id)
    time.sleep(.25)
    try:
        visible = wait_for_element_visible(self, by, locator, timeout)
    finally:
        driver.switch_to.parent_frame()
    return visible


def wait_for_element_in_iframe_and_click(self, iframe_id, by, locator, timeout=globaldata.TIMEOUT):
    driver = self.driver
    if not wait_for_element_visible(self, globaldata.ID, iframe_id, timeout):
        print("\nCF: iframe '" + iframe_id + "' not present in page")
        return False

    driver.switch_to.frame(iframe_id)
    try:
        element = wait_for_element_clickable(self, by, locator, timeout)
        if isinstance(element, webdriver.remote.webelement.WebElement):
            element.click()
            return True
        else:
            print('\nCF: Unable to find clickable element in iFrame')
            return False
    finally:
        driver.switch_to.parent_frame()


def wait_for_child_element_visible(self, parent_element, by, locator, timeout=globaldata.TIMEOUT):
    driver = self.driver
    wait = WebDriverWait(driver, timeout)
    by = get_by(by)
    if not isinstance(parent_element,  webdriver.remote.webelement.WebElement):
        return False, '\ncommonfunctions: parent_element provided is NOT a webelement'

    try:
        visible = wait.until(custom_EC.child_element_to_be_visible_in_element((by, locator), parent_element))
    except TimeoutException:
        visible = False
    return visible


def check_if_child_element_visible(self, parent_element, by, locator, timeout=globaldata.TIMEOUT):
    return wait_for_child_element_visible(self, parent_element, by, locator, timeout=globaldata.TIMEOUT)


def wait_for_child_element_present(self, parent_element, by, locator, timeout=globaldata.TIMEOUT):
    driver = self.driver
    wait = WebDriverWait(driver, timeout)
    by = get_by(by)

    try:
        visible = wait.until(custom_EC.child_element_to_be_present_in_element((by, locator), parent_element))
    except TimeoutException:
        visible = False
    return visible


def wait_for_alert(self, timeout=globaldata.TIMEOUT):
    driver = self.driver
    try:
        alert = WebDriverWait(driver, timeout).until(EC.alert_is_present())
        if bool(alert):
            return alert
    except Exception as e:
        print('\n' + str(e))
        return False


# Depricated
def check_script(self, script):
    driver = self.driver
    try:
        driver.execute_script(script)
    except Exception as e:
        return False
    return True


def wait_for_script_runnable(self, script, **kwargs):
    passed = True
    first_time = time.time()
    last_time = first_time
    if 'timeout' in kwargs:
        timeout = kwargs['timeout']
    else:
        timeout = globaldata.TIMEOUT
    retry_interval = globaldata.TIMEOUT_RETRY_INTERVAL
    if 'retry' in kwargs:
        retry_interval = kwargs['retry']
    if 'timeout' in kwargs:
        timeout = kwargs['timeout']
    while(check_script(self, script) is False):
        new_time = time.time()
        if new_time - last_time > timeout:
            passed = False
            break
        else:
            time.sleep(retry_interval)
    return passed


def poll_until(self, script, condition, timeout=globaldata.TIMEOUT):
    driver = self.driver
    first_time = time.time()
    last_time = first_time
    passed = True
    try:
        while(str(driver.execute_script(script)) != condition):
            new_time = time.time()
            if new_time - last_time > timeout:
                passed = False
                break
        return passed
    except:
        return False


# TODO: Phase out this function and remove. Github issue #22
def wait_for_element(self, by, what, **kwargs):

    driver = self.driver
    found = True
    timeout_param = globaldata.TIMEOUT

    if 'timeout' in kwargs:
        timeout_param = kwargs['timeout']

    if 'exec_js' in kwargs:
        script = ""
        if by == globaldata.ID:
            script = "document.getElementById('" + what + "')"
        elif by == globaldata.CN:
            script = "document.getElementsByClassName('" + what + "')[0]"
        elif by == globaldata.NAME:
            script = "document.getElementsByName('" + what + "')[0]"
        elif by == globaldata.TAG:
            script = "document.getElementsByTagName('" + what + "')[0]"

        vscript = script + ".length"

        found = wait_for_script_runnable(self, vscript, timeout=timeout_param)
        if found:
            if 'click' in kwargs:
                script = script + ".click()"
                driver.execute_script(script)

    else:
        first_time = time.time()
        last_time = first_time
        while check_if_element_present(self, by, what) is False:
            new_time = time.time()
            if new_time - last_time > timeout_param:
                found = False
                break

        if (('click' in kwargs) and (found is True)):
            loc_type = get_by(by)
            driver.find_element(loc_type, what).click()

    return found


def get_checkbox_state(self, element):
    assert isinstance(element, webdriver.remote.webelement.WebElement), 'Element for checkbox field type was not provided'

    try:
        check_box_value = element.get_attribute('checked')
        time.sleep(1)
        return check_box_value
    except (StaleElementReferenceException, InvalidElementStateException):
        return False


def set_checkbox(self, element, desired_state='checked'):
    assert isinstance(element, webdriver.remote.webelement.WebElement), 'The element provided must be a webelement'
    time.sleep(2)
    try:
        if get_checkbox_state(self, element=element) != desired_state:
            time.sleep(1)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            element.click()
            time.sleep(.5)
    except (StaleElementReferenceException, InvalidElementStateException):
        print('Not able to click on the checkbox')
        return False
    return True


def edit_field_type_text(self, element, data):
    assert isinstance(element, webdriver.remote.webelement.WebElement), 'The element provided must be a webelement'
    assert isinstance(data, str), 'Data provided must be a string'
    element.clear()
    element.send_keys(data)
    return element.get_attribute('value')


def edit_field_type_select(self, element, field_name, data):
    assert isinstance(element, webdriver.remote.webelement.WebElement), 'The element provided must be a webelement'
    assert isinstance(field_name, str), 'Field provided must be a string'
    assert isinstance(data, str), 'Data provided must be a string'

    try:
        Select(element.find_element_by_id(field_name)).select_by_visible_text(data)
        select_element = wait_for_element_present(self, globaldata.CSS, 'select[id=\"' + field_name + '\"]', globaldata.TIMEOUTLONG)
    except (NoSuchElementException, ElementNotVisibleException, StaleElementReferenceException, InvalidElementStateException):
        print('\nData ' + data + ' is not an available selection or the select field is in an Invalid/stale element state')
        return False
    return select_element.get_attribute('value')


def start_of_school(self):
    return '07/01'

def end_of_school(self):
    return '06/30'

def calculate_current_school_year(self, date=get_current_date_formatted()):
    current_year = '{dt.year}'.format(dt=datetime.datetime.now())
    next_year = int(current_year)+1
    beg_school_year = start_of_school(self) + '/' + current_year
    end_school_year = end_of_school(self) + '/' + str(next_year)

    if time.strptime(date, "%m/%d/%Y") < time.strptime(beg_school_year, "%m/%d/%Y"):
        beg_school_month_year = start_of_school(self) + '/' + str(int(current_year)-1)
        end_school_month_year = end_of_school(self) + '/' +  str(int(next_year)-1)
        return beg_school_month_year + ' - ' + end_school_month_year

    elif time.strptime(date, "%m/%d/%Y") >= time.strptime(beg_school_year, "%m/%d/%Y") and time.strptime(date, "%m/%d/%Y") <= time.strptime(end_school_year, "%m/%d/%Y"):
        return beg_school_year + ' - ' + end_school_year

    elif time.strptime(date, "%m/%d/%Y") > time.strptime(end_school_year, "%m/%d/%Y"):
        beg_school_month_year = start_of_school(self) + '/' + str(int(current_year)+1)
        end_school_month_year = end_of_school(self) + '/' + str(int(next_year)+1)
        return beg_school_month_year + ' - ' + end_school_month_year

    else:
        print('Unable to calculate correct beginning and end of school year')
        return False


def driver_browser_info(driver):
    browser = driver.capabilities['browserName']
    print('Browser Name = ' + browser)
    if 'chrome' in browser:
        print('Browser Version = ' + driver.capabilities['version'])
        print('Driver Version = ' + driver.capabilities[browser]['chromedriverVersion'])
        print('Platform = ' + driver.capabilities['platform'])
    elif 'firefox' in browser:
        print('Browser Version = ' + driver.capabilities['browserVersion'])
        print('Platform = ' + driver.capabilities['platformName'])
        # FireFox says there is no need to give us normal humans the version of the geckodriver
    else:
        print ('\nCF: Chrome and Firefox are currently the only supported browsers')


def results_grouper(how_to_group, what_to_group, fill_value=None):
    # Sometimes results list is not returned as a group but as individualized records
    # This function will put the results in a group by how the caller wants them
    # the how to group is a number
    # if you have a list returned, ie [1, 2, 3, 4, 5, 6]
    # you want them in 2 groups, your how_to_group would be 3
    args = [iter(what_to_group)] * how_to_group
    grouped_list = itertools.zip_longest(*args, fillvalue=fill_value)
    return grouped_list


def get_timestamp(self, time_format='%H:%M:%S.%f'):
    ts = time.time()
    return datetime.datetime.fromtimestamp(ts).strftime(time_format)[:-3]


def get_current_env(self):
    driver = self.driver
    return fg.get_url(self.test_title)


def os_browser_path(browser_type):
    os_type = platform.system().lower()
    browser_type = browser_type.lower()

    if os_type == 'darwin':
        if 'chrome' in browser_type:
            beta_browser_path = '/Applications/Google BETA Chrome.app/Contents/MacOS/Google Chrome'
            stable_browser_path = '/Applications/Google STABLE Chrome.app/Contents/MacOS/Google Chrome'
        elif 'firefox' in browser_type:
            beta_browser_path = '/Applications/Firefox BETA.app/Contents/MacOS/Firefox-bin'
            stable_browser_path = '/Applications/Firefox STABLE.app/Contents/MacOS/Firefox-bin'
        else:
            return False, 'Browser type not coded yet'
    elif os_type == 'linux':
        if 'chrome' in browser_type:
            beta_browser_path = '/usr/bin/google-chrome-beta'
            stable_browser_path = '/usr/bin/google-chrome'
        elif 'firefox' in browser_type:
            beta_browser_path = '/usr/bin/firefox-beta'
            stable_browser_path = '/usr/bin/firefox'
        else:
            return False, 'Browser type not coded yet'

    elif os_type == 'windows':
        if 'chrome' in browser_type:
            beta_browser_path = 'C:\\Program Files (x86)\\Google\\Chrome Beta\\Application\\chrome.exe'
            stable_browser_path = 'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe'
        elif 'firefox' in browser_type:
            beta_browser_path = 'C:\\Program Files (x86)\\Mozilla Firefox\\firefox beta.exe'
            stable_browser_path = 'C:\\Program Files\\Mozilla Firefox\\firefox.exe'
        else:
            return False, 'Browser type not coded yet'

    elif os_type == 'IOS':
        return False, 'Not coded yet'

    else:
        return False, '\nCF: Did not find os type of ' + os_type

    return [beta_browser_path, stable_browser_path]
