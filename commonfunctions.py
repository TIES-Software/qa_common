from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from common import custom_EC
import time
import datetime
import string
import random
import globaldata


# PAGE ELEMENTS
TAG_HEADER = "h1"
ID_CONTAINER = "Container"
ID_IFRAME = "iFrameId"


# FUNCTIONS
def get_driver(browser):
    if (browser == 'chrome'):
        path_to_chrome_driver = globaldata.CHROME_DRIVER_DIR
        options = webdriver.ChromeOptions()
        options.add_argument("--test-type")
        options.add_argument("--disable-popup-blocking")
        driver = webdriver.Chrome(executable_path=path_to_chrome_driver, chrome_options=options)

    else:
        if (browser != 'firefox'):
            print ("Unable to create driver for " + browser + ". Using Firefox instead.")
        caps = DesiredCapabilities.FIREFOX
        caps["marionette"] = True
        caps["binary"] = globaldata.FIREFOX_BINARY_PATH
        driver = webdriver.Firefox(capabilities=caps)

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


def generate_id(size=8, chars=string.letters + string.digits):
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


def get_current_date_no_leading_zeros():
    return '{dt.month}/{dt.day}/{dt.year}'.format(dt=datetime.datetime.now())


def get_past_date(days_ago):
    return_date = datetime.datetime.now() - datetime.timedelta(days=days_ago)
    return return_date.strftime('%m/%d/%Y')


def get_future_date(days_in_future):
    return_date = datetime.datetime.now() + datetime.timedelta(days=days_in_future)
    return return_date.strftime('%m/%d/%Y')


def wait_for_jquery_inactive(self, timeout=globaldata.TIMEOUTSHORT):
    # waits until jQuery finishes executing
    script = 'return jQuery.active'
    poll_until(self, script, "0", timeout=globaldata.TIMEOUTSHORT)

######
# Window Handle Functions
######


def close_all_additional_windows(self):
    driver = self.driver
    while len(driver.window_handles) > 1:
            driver.switch_to.window(driver.window_handles[-1])
            driver.close()
    driver.switch_to.window(driver.window_handles[0])


def wait_for_handle_to_load_and_switch(self, handle_index, timeout=globaldata.TIMEOUTSHORT):
    driver = self.driver
    count = 0
    while ((len(driver.window_handles) <= handle_index) and count <= timeout):
        count = count + 1
        time.sleep(1)
    driver.switch_to_window(driver.window_handles[handle_index])


def close_alert(self):
    driver = self.driver
    try:
        WebDriverWait(driver, 3).until(EC.alert_is_present())

        alert = driver.switch_to_alert()
        alert.accept()
    except TimeoutException:
        print "No alert."


def wait_for_popup_window(self, expected_num_windows, timeout=globaldata.TIMEOUTSHORT):
    driver = self.driver
    wait = WebDriverWait(driver, timeout)
    new_window_present = wait.until(
        lambda driver: len(driver.window_handles) == expected_num_windows)
    return alert_visible


######
# Page Element Functions
######


def check_if_element_clickable(self, by, locator):
    return wait_for_element_clickable(self, by, locator, 1)


def wait_for_element_clickable(self, by, locator, timeout=globaldata.TIMEOUTSHORT):
    driver = self.driver
    wait = WebDriverWait(driver, timeout)
    by = get_by(by)

    try:
        clickable = wait.until(EC.element_to_be_clickable((by, locator)))
    except TimeoutException:
        clickable = False
    return clickable


def wait_for_element_and_click(self, by, locator, timeout=globaldata.TIMEOUTSHORT):
    driver = self.driver
    clickable = wait_for_element_clickable(self, by, locator, timeout)
    try:
        clickable.click()
        return True
    except Exception as e:
        print(e)
        return False


def wait_for_element_text_to_equal(self, by, locator, text_to_equal, timeout=globaldata.TIMEOUTSHORT):
    driver = self.driver
    wait = WebDriverWait(driver, timeout)
    by = get_by(by)

    try:
        text_equal = wait.until(custom_EC.exact_text_to_be_present_in_element((by, locator), text_to_equal))
    except TimeoutException:
        text_equal = False
    return text_equal


def wait_for_element_text_not_null(self, by, locator, timeout=globaldata.TIMEOUTSHORT):
    driver = self.driver
    wait = WebDriverWait(driver, timeout)
    by = get_by(by)

    try:
        element_not_null = wait.until(custom_EC.element_text_to_be_non_null((by, locator)))
    except TimeoutException:
        element_not_null = False
    return element_not_null


def wait_for_element_text_to_contain(self, by, locator, text_to_contain, timeout=globaldata.TIMEOUTSHORT):
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


def check_if_element_not_present(self, by, locator):
    timeout = 1
    return wait_for_element_not_present(self, by, locator, timeout)


def wait_for_element_present(self, by, locator, timeout=globaldata.TIMEOUTSHORT):
    driver = self.driver
    wait = WebDriverWait(driver, timeout)
    by = get_by(by)
    try:
        present = wait.until(EC.presence_of_element_located((by, locator)))
    except TimeoutException:
        present = False
    return present


def wait_for_element_not_present(self, element, timeout=globaldata.TIMEOUTSHORT):
    driver = self.driver
    wait = WebDriverWait(driver, timeout)
    try:
        stale = wait.until(EC.staleness_of(element))
    except TimeoutException:
        stale = False
    return stale


def check_if_element_visible(self, by, locator):
    timeout = 1
    return wait_for_element_visible(self, by, locator, timeout)


def check_if_element_not_visible(self, by, locator):
    timeout = 1
    return wait_for_element_not_visible(self, by, locator, timeout)


def wait_for_element_visible(self, by, locator, timeout=globaldata.TIMEOUTSHORT):
    driver = self.driver
    wait = WebDriverWait(driver, timeout)

    try:
        visible = wait.until(EC.visibility_of_element_located((get_by(by), locator)))
    except TimeoutException:
        visible = False
    return visible


def wait_for_element_not_visible(self, by, locator, timeout=globaldata.TIMEOUTSHORT):
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
def wait_for_element_visible_in_iframe(self, iframe_id, by, locator, timeout=globaldata.TIMEOUTSHORT):
    driver = self.driver
    assert wait_for_element_visible(self, globaldata.ID, iframe_id, globaldata.TIMEOUTSHORT), "iframe not present in page"
    driver.switch_to.frame(iframe_id)
    try:
        visible = wait_for_element_visible(self, by, locator, timeout)
    finally:
        driver.switch_to.parent_frame()
    return visible


def wait_for_element_in_iframe_and_click(self, iframe_id, by, locator, timeout=globaldata.TIMEOUTSHORT):
    driver = self.driver
    assert wait_for_element_visible(self, globaldata.ID, iframe_id, timeout), "iframe not present in page"
    driver.switch_to.frame(iframe_id)
    try:
        element = wait_for_element_clickable(self, by, locator, timeout)
        if bool(element):
            element.click()
            clicked = True
        else:
            clicked = False
    finally:
        driver.switch_to.parent_frame()
    return clicked


def wait_for_child_element_visible(self, parent_element, by, locator, timeout=globaldata.TIMEOUTSHORT):
    driver = self.driver
    wait = WebDriverWait(driver, timeout)
    by = get_by(by)

    try:
        visible = wait.until(custom_EC.child_element_to_be_visible_in_element((by, locator), parent_element))
    except TimeoutException:
        visible = False
    return visible


def check_if_child_element_visible(self, parent_element, by, locator, timeout=globaldata.TIMEOUTSHORT):
    return wait_for_child_element_visible(self, parent_element, by, locator, 1)


def wait_for_popup(self):
    driver = self.driver
    try:
        popup_found = WebDriverWait(driver, globaldata.TIMEOUTSHORT).until(EC.alert_is_present())
        if popup_found:
            return popup_found
    except Exception, e:
        return False


# Migrate to Feepay common
def wait_for_overlay(self):
    driver = self.driver
    script = "return document.getElementsByClassName('ui-widget-overlay').length"
    if (poll_until(self, script, "0", globaldata.TIMEOUTSHORT) is False):
        print("Script overlay never completed loading!")


# Depricated
def wait_for_url(self, url, timeout=globaldata.TIMEOUTSHORT):
    driver = self.driver
    found = True
    first_time = time.time()
    last_time = first_time
    current_url = ""

    while (url not in current_url):
        try:
            current_url = driver.current_url
        except Exception, e:
            current_url = ""
        new_time = time.time()
        if new_time - last_time > timeout:
            found = False
            break
    return found


def check_script(self, script):
    driver = self.driver
    try:
        driver.execute_script(script)
    except Exception, e:
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


def poll_until(self, script, condition, timeout=globaldata.TIMEOUTSHORT):
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
