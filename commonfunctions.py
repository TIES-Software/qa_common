from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import (NoSuchElementException,
                                        WebDriverException,
                                        StaleElementReferenceException,
                                        ElementNotVisibleException,
                                        InvalidElementStateException,
                                        TimeoutException)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#Our custom Expected Conditions
from common import custom_EC
from selenium.webdriver.common.action_chains import ActionChains
import time, datetime
import string
import random
import basetestcase,globaldata

#***
#*  Nice set of common functions
#***

#PAGE ELEMENTS
TAG_HEADER = "h1"
ID_CONTAINER = "Container"
ID_IFRAME = "iFrameId"


#SCRIPTS

#CLASSES

#FUNCTIONS

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
    return '{dt.month}/{dt.day}/{dt.year}'.format(dt = datetime.datetime.now())


def get_past_date(days_ago):
    return_date = datetime.datetime.now() - datetime.timedelta(days=days_ago)
    return return_date.strftime('%m/%d/%Y')


def get_future_date(days_in_future):
    return_date = datetime.datetime.now() + datetime.timedelta(days=days_in_future)
    return return_date.strftime('%m/%d/%Y')


def wait_for_jquery_inactive(self, timeout):
    # waits until jQuery finishes executing
    script = 'return jQuery.active'
    poll_until(self, script, "0", timeout)


def close_alert(self):
    driver = self.driver
    try:
        WebDriverWait(driver, 3).until(EC.alert_is_present(),
                                       'Timed out waiting for PA creation ' +
                                       'confirmation popup to appear.')

        alert = driver.switch_to_alert()
        alert.accept()
    except TimeoutException:
        print "No alert."


def wait_for_popup_window(self, expected_no_windows, timeout):
    driver = self.driver
    wait = WebDriverWait(driver, timeout)
    new_window_present = wait.until(
        lambda driver: len(driver.window_handles) == expected_no_windows)
    return alert_visible


def wait_for_url(self, url, **kwargs):
    driver = self.driver
    found = True
    first_time = time.time()
    last_time = first_time
    current_url = ""

    if 'timeout' in kwargs:
        timeout = kwargs['timeout']
    else:
        timeout = globaldata.TIMEOUT

    while (url not in current_url):
        try:
            current_url = driver.current_url
        except Exception, e:
            current_url = ""
        new_time = time.time()
        if  new_time - last_time > timeout:
            found = False
            break
    return found


def wait_for_element_populated(self, what, element):
    driver = self.driver
    by = get_by(what)
    timeout = globaldata.LONG_TRANSITION_TIME
    populated = True
    first_time = time.time()
    last_time = first_time
    element_text = ""
    while element_text == "":
        new_time = time.time()
        try:
            element_text = driver.find_element(by, element).text
        except Exception, e:
            element_text = ""
        if  new_time - last_time > timeout:
            populated = False
            break
    return populated


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
        while check_if_element_present(self, by, what) == False:
            new_time = time.time()
            if  new_time - last_time > timeout_param:
                found = False
                break

        if (('click' in kwargs) and (found == True)):
            loc_type = get_by(by)
            driver.find_element(loc_type, what).click()

    return found


#returns true if element is or becomes visible and clickable. False otherwise.
def wait_for_element_clickable(self, by, locator, timeout):
    driver = self.driver
    wait = WebDriverWait(driver, timeout)
    by = get_by(by)
    #the EC.element_to_be_clickable takes in a locator, and the 'by' argument is
    #how it is located. (eg, Xpath, css selector, id)
    try:
        clickable = wait.until(EC.element_to_be_clickable((by, locator)))
    except TimeoutException:
        clickable = False
    return clickable


def wait_for_element_text_to_equal(self, by, locator, text_to_equal, timeout):
    driver = self.driver
    wait = WebDriverWait(driver, timeout)
    by = get_by(by)

    try:
        text_equal = wait.until(custom_EC.exact_text_to_be_present_in_element((by, locator), text_to_equal))
    except TimeoutException:
        text_equal = False
    return text_equal

def wait_for_element_text_not_null(self, by, locator, timeout):
    driver = self.driver
    wait = WebDriverWait(driver, timeout)
    by = get_by(by)

    try:
        #waits until text is not null within element
        element_not_null = wait.until(custom_EC.element_text_to_be_non_null((by, locator)))
    except TimeoutException:
        element_not_null = False
    return element_not_null


def wait_for_element_text_to_contain(self, by, locator, text_to_contain, timeout):
    driver = self.driver
    wait = WebDriverWait(driver, timeout)
    by = get_by(by)

    try:
        #waits until given text is present within element. This checks to see
        #if the element CONTAINS the text; does not have to be a direct match
        text_present = wait.until(EC.text_to_be_present_in_element((by, locator), text_to_contain))
    except TimeoutException:
        text_present = False
    return text_present

def wait_for_element_and_click (self, by, locator, timeout):
    driver = self.driver
    #per locator, is element there and clickable
    clickable = wait_for_element_clickable(self, by, locator, timeout)
    try:
        # if locator is there then click it
        clickable.click()
        return True
    except:
        return False

#Expects the element to be removed from the DOM. Return True if element is no longer in the DOM
def wait_for_element_not_present(self, element, timeout):
    driver = self.driver
    wait = WebDriverWait(driver, timeout)
    try:
        stale = wait.until(EC.staleness_of(element))
    except TimeoutException:
        #element is still attached to the DOM. Not what we expect
        stale = False
    return stale

#added for completeness
def check_if_element_not_present(self, element):
    timeout = 1
    return wait_for_element_not_present(self, element, timeout)


def wait_for_element_visible(self, by, locator, timeout):
    driver = self.driver
    wait = WebDriverWait(driver, timeout)

    try:
        visible = wait.until(EC.visibility_of_element_located((get_by(by), locator)))
    except TimeoutException:
        visible = False
    return visible


def check_if_element_visible(self, by, locator):
    timeout = 1
    return wait_for_element_visible(self, by, locator, timeout)

#this is more efficient than waiting for wait_for_element_visible to be false, because it skips the entire timeout
#because we are expecting the element to be invisible, this will return as soon as it is.
def wait_for_element_not_visible(self, by, locator, timeout):
    driver = self.driver
    wait = WebDriverWait(driver, timeout)

    try:
        not_visible = wait.until(EC.invisibility_of_element_located((get_by(by), locator)))
    except TimeoutException:
        not_visible = False
    return not_visible


#added for completeness, though check_if_element_visible can also provide this functionality
def check_if_element_not_visible(self, by, locator):
    timeout = 1
    return wait_for_element_not_visible(self, by, locator, timeout)


def wait_for_element_present(self, by, locator, timeout):
    driver = self.driver
    wait = WebDriverWait(driver, timeout)
    by = get_by(by)
    try:
        present = wait.until(EC.presence_of_element_located((by, locator)))
    except TimeoutException:
        present = False
    return present

def check_if_element_present(self, by, locator):
    timeout = 1
    return wait_for_element_present(self, by, locator, timeout)


def check_if_element_valid(self, what, element, action):
    by = get_by(what)
    if action == 'clear':
        try:
            self.driver.find_element(by, element).clear()
        except InvalidElementStateException:
            return False
        return True


def check_if_element_clickable(self, by, locator):
    #simply calls the function to wait for a clickable element with a
    # 1 second timeout
    return wait_for_element_clickable(self, by, locator, 1)


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


#AB 6/2, changed to general exception
def check_script(self, script):
    driver = self.driver
    try: driver.execute_script(script)
    except Exception, e: return False
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
    while(check_script(self, script) == False):
        new_time = time.time()
        if  new_time - last_time > timeout:
            passed = False
            break
        else:
            time.sleep(retry_interval)
    return passed


def poll_until(self, script, condition, timeout):
    driver = self.driver
    first_time = time.time()
    last_time = first_time
    passed = True
    try:
        while(str(driver.execute_script(script)) != condition):
            new_time = time.time()
            if  new_time - last_time > timeout:
                passed = False
                break
        return passed
    except:
        return False


#VERIFICATIONS SHARED ACROSS MULTIPLE PAGES
def check_if_error(self, page):
    failed = False
    failure = ""
    driver = self.driver
    switch_to_default = True

    try:
        driver.switch_to_frame(ID_IFRAME)
    except Exception, e:
        switch_to_default = False

    if (wait_for_element(self, globaldata.ID, ID_CONTAINER) == False):
        failed = True
        failure = "Container did not load.\n"
        print("Container did not load.")
    else:
        container_text = driver.find_element_by_id(ID_CONTAINER).text
        if ("EXCEPTION" in container_text.upper() and
            ("Exceptions" not in container_text)):
            failed = True
            failure = failure + "There was an exception on the page '" + page + "'.\n"
            print("FAILURE: There was an exception on the page '" + page + "'.")
        else:
            print("SUCCESS: There was no exception on the page.")

    if switch_to_default:
        driver.switch_to_default_content()

    return [failed, failure]


def get_element_number(self, element, text):
    driver = self.driver
    script = "elements = document.getElementsByClassName('" + element + "');"
    script = script + "for (i=0;i<elements.length;i++){ "
    script = script + "if (elements[i].textContent == '" + text + "') { return i; } }"
    element_num = driver.execute_script(script)

    return int(element_num)


def wait_for_overlay(self):
    driver = self.driver
    script = "return document.getElementsByClassName('ui-widget-overlay').length"
    if (poll_until(self, script, "0", globaldata.TIMEOUTSHORT) == False):
        print("Script overlay never completed loading!")

#needed for adminBeta testing
def wait_for_element_visible_in_iframe(self, iframe_id, by, locator, timeout):
    driver = self.driver
    #assert iframe is present on page
    self.assertTrue(wait_for_element_visible(self, globaldata.ID, iframe_id, globaldata.TIMEOUTSHORT),
                                            "iframe not present in page")
    #change DOM to iframe's
    driver.switch_to.frame(iframe_id)
    try:
        visible = wait_for_element_visible(self, by, locator, timeout)
    finally:
        #switch back
        driver.switch_to.parent_frame()
    return visible

def wait_for_child_element_visible(self, parent_element, by, locator, timeout):
    driver = self.driver
    wait = WebDriverWait(driver, timeout)
    by = get_by(by)

    try:
        visible = wait.until(custom_EC.child_element_to_be_visible_in_element((by, locator), parent_element))
    except TimeoutException:
        visible = False
    return visible

def check_if_child_element_visible(self, parent_element, by, locator, timeout):
    return wait_for_child_element_visible(self, parent_element, by, locator, 1)

def wait_for_popup(self):
    driver = self.driver
    try:
        popup_found = WebDriverWait(driver, globaldata.TIMEOUTSHORT).until(EC.alert_is_present())
        if popup_found:
            return popup_found
    except Exception, e:
        return False
