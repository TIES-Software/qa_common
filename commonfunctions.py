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
from selenium.webdriver.common.action_chains import ActionChains
import time, datetime
from random import randint
import basetestcase,globaldata


#PAGE ELEMENTS
TAG_HEADER = "h1"
ID_CONTAINER = "Container"
ID_IFRAME = "iFrameId"


#SCRIPTS



#CLASSES
        

#FUNCTIONS

def get_unique_name():
    d = datetime.datetime.now()
    unique_name = str(d.strftime('%m'))
    unique_name = unique_name + str(d.strftime('%d'))
    unique_name = unique_name + str(d.year)
    unique_name = unique_name + str(d.strftime('%H'))
    unique_name = unique_name + str(d.strftime('%M'))
    return unique_name


def get_day_number(**kwargs):
    if 'date' in kwargs:
        day = kwargs['date'].split("/")[1].split("/")[0]
    else:
        day = datetime.datetime.today().day
    return day


def get_current_date_formatted():
    return time.strftime('%m/%d/%Y')


def get_past_date(**kwargs):
    return_date = datetime.datetime.now()
    if 'days' in kwargs:
        return_date = (datetime.datetime.now() + datetime.timedelta(-kwargs['days']))
    #if 'months' in kwargs:
    #    return_date = (return_date.replace(return_date.month - kwargs['months']))
    if 'years' in kwargs:
        return_date = (return_date.replace(return_date.year - kwargs['years']))
    return return_date.strftime('%m/%d/%Y')


def get_future_date(**kwargs):
    return_date = datetime.datetime.now()
    if 'days' in kwargs:
        return_date = (datetime.datetime.now() + datetime.timedelta(+kwargs['days']))
    #if 'months' in kwargs:
    #    return_date = (return_date.replace(return_date.month - kwargs['months']))
    if 'years' in kwargs:
        return_date = (return_date.replace(return_date.year + kwargs['years']))
    return return_date.strftime('%m/%d/%Y')


def readystate_complete(self):
    driver = self.driver
    return driver.execute_script("return document.readyState") == "complete"


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



def wait_for_url(self, url, **kwargs):
    driver = self.driver
    found = True    
    first_time = time.time()
    last_time = first_time  
    #AB 6/1, refactored to try to eliminate false failures
    current_url = ""#driver.current_url

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
    #AB 6/2, refactored to prevent false failure with try catch
    #and initializing to empty string
    element_text = ""#driver.find_element(by, element).text
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


def wait_for_element_to_equal(self, what, element, value, **kwargs):
    driver = self.driver
    by = get_by(what)
    
    if 'timeout' in kwargs:
        timeout = kwargs['timeout']
    else:
        timeout = globaldata.TIMEOUTSHORT

    equal = True
    first_time = time.time()
    last_time = first_time
    #AB 6/2, trying to eliminate possible false failure
    element_text = ""
    #element_text = driver.find_element(by, element).text
    while element_text != value: 
        new_time = time.time()
        try:
            element_text = driver.find_element(by, element).text
        except Exception, e:
            element_text = ""
        if  new_time - last_time > timeout:
            equal = False
            break  
    return equal
    

def wait_for_element(self, by, what, **kwargs):
    
    driver = self.driver
    found = True
    timeout_param = globaldata.TIMEOUT
    
    if 'timeout' in kwargs:
        timeout_param = kwargs['timeout'] 
    
    #AB 6/2, moved within non js conditional to eliminate a false failure
    #self.driver.implicitly_wait(timeout_param)    
        
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
        self.driver.implicitly_wait(timeout_param) 
        first_time = time.time()
        last_time = first_time   
        while check_if_element_present(self, by, what, 
                                       timeout=0) == False: 
            new_time = time.time()
            if  new_time - last_time > timeout_param:
                found = False
                break
                
        if (('click' in kwargs) and (found == True)):
            loc_type = get_by(by)
            driver.find_element(loc_type, what).click()
                        
    return found



def wait_for_element_clickable(self, by, what, **kwargs):
    driver = self.driver
    timeout_param = globaldata.TIMEOUT
    if 'timeout' in kwargs:
        timeout_param = kwargs['timeout'] 
    self.driver.implicitly_wait(timeout_param)      
    clicked = True
    first_time = time.time()
    last_time = first_time   
    while check_if_element_clickable(self, by, what, 
                                     timeout=0) == False: 
        new_time = time.time()
        if  new_time - last_time > timeout_param:
            clicked = False
            break 
    return clicked


#HEREYO: Finish adding other data types (by)
def wait_for_element_text(self, by, what, link_text, **kwargs):
    driver = self.driver
    found = False
    if 'timeout' in kwargs:
        timeout = kwargs['timeout']
    else:
        timeout = globaldata.TIMEOUT
    script = "found = false; "
    if by == globaldata.CN:
        script = script + "obj = document.getElementsByClassName('" + what + "'); "
    elif by == globaldata.ID:
        script = script + "obj = document.getElementById('" + what + "'); "
    script = script + "for (i=0;i<obj.length; i++) { "
    script = script + "if (obj[i].textContent.indexOf('" + link_text + "')>-1) "
    script = script + "{ found = true; } }; return found;" 

    found = poll_until(self, script, "True", timeout) 
        
    return found



def wait_for_link_and_click(self, by, what, link_text, **kwargs):
    driver = self.driver
    found = False
    script = "obj = document.getElementsByClassName('" + what + "'); "
    script = script + "for (i=0;i<obj.length; i++) { "
    if 'exclude' in kwargs:
        script = script + "if ((obj[i].textContent.indexOf('" + link_text + "')>-1) && "
        script = script + "(obj[i].textContent.indexOf('" + kwargs['exclude'] + "')==-1))"
    else:
        script = script + "if (obj[i].textContent.indexOf('" + link_text + "')>-1) "
    script = script + "{ obj[i].click(); } }"      
    found = wait_for_element(self, by, what, exec_js=True, timeout=globaldata.TIMEOUTSHORT)  
    if found:
        driver.execute_script(script)
        
    return found



def wait_for_element_not_present(self, by, what):
    first_time = time.time()
    last_time = first_time 
    not_present = True
    while check_if_element_present(self, by, what) == True: 
        new_time = time.time()
        if  new_time - last_time > globaldata.TIMEOUT:
            not_present = False
    return not_present

#HEREYO remove all thses        
def wait_for_element_visible(self, by, what):
    first_time = time.time()
    last_time = first_time 
    visible = True
    while check_if_element_visible(self, by, what) == False: 
        new_time = time.time()
        if  new_time - last_time > globaldata.TIMEOUT:
            visible = False
    return visible


def wait_for_element_not_visible(self, by, what):
    first_time = time.time()
    last_time = first_time 
    visible = False
    while check_if_element_visible(self, by, what) == True: 
        new_time = time.time()
        if  new_time - last_time > globaldata.TIMEOUT:
            visible = True
    return visible

        
def check_if_element_present(self, what, element, **kwargs):
    timeout = globaldata.TIMEOUT
    if 'timeout' in kwargs:
        timeout = kwargs['timeout']  
     
    self.driver.implicitly_wait(timeout) 
    by = get_by(what)

    try:
        self.driver.find_element(by, element)
    except NoSuchElementException:
        return False
    return True


def check_if_element_visible(self, what, element):
    by = get_by(what)
    try:
        self.driver.find_element(by, element)
    except ElementNotVisibleException:
        return False
    return True


def check_if_element_valid(self, what, element, action):
    by = get_by(what)
    if action == 'clear':        
        try:
            self.driver.find_element(by, element).clear()
        except InvalidElementStateException:
            return False
        return True 
    
def check_if_element_clickable(self, by, what, **kwargs):
    timeout = globaldata.TIMEOUTSHORT
    if 'timeout' in kwargs:
        timeout = kwargs['timeout']
    self.driver.implicitly_wait(kwargs['timeout']) 
    try:
        self.driver.find_element(by, element).click()
    except:
        return False
    return True
    
    
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
    

def verify_text_listed(self, text, element, element_type, **kwargs):
    failed = False
    failure = ""
    driver = self.driver
    if 'index' in kwargs:
        index = kwargs['index']
    else:
        index = 0
    if (globaldata.CN in element_type):
        script = "return document.getElementsByClassName('" + element + "')[" + str(index) + "].textContent.indexOf('" + text + "')>-1"
    elif (globaldata.ID in element_type):
        script = "return document.getElementById('" + element + "').textContent.indexOf('" + text + "')>-1"

    if (poll_until(self, script, "True", globaldata.TRANSFORM_TRANSITION_TIME) == False):
        failed = True
        failure = "'" + text + "' was not visible in element.\n"
        print("FAILURE: '" + text + "' was not visible in element.")
    else: 
        print("SUCCESS: Verified '" + text + "' was in element.")

    return [failed, failure]
    
    
def verify_page_title(self, page, title, **kwargs):
    failed = False
    failure = ""
    print("Verifying page title '" + title + "'...")
    script = 'return document.getElementsByTagName("' + TAG_HEADER
    script = script + '")[0].textContent.indexOf( "' + title + '")>-1'
    passed = poll_until(self, script, "True", globaldata.TIMEOUTSHORT) 
    if passed:
        print("Validated page title is '" + title + "'.")
    else:
        failed = True
        failure = "Page '" + page + "' did not contain title '" + title + "'.\n"
        print("FAILURE: Page '" + page + "' did not containt title '" + title + "'.")

    return [failed, failure]



def get_element_number(self, element, text):
    driver = self.driver
    script = "elements = document.getElementsByClassName('" + element + "');"
    script = script + "for (i=0;i<elements.length;i++){ "
    script = script + "if (elements[i].textContent == '" + text + "') { return i; } }"
    element_num = driver.execute_script(script)
    return int(element_num)


def set_date(self, page, **kwargs):
    
    CN_DAY = "day"
    if page == globaldata.PAGE_ACTIVITIES:
        ID_ENDDATE = "ctl00_ContentPlaceHolder1_ActivityEndDate"
        
    driver = self.driver
    failed = False
    failure = ""

    #Default behavior is to set end date in future
    if 'past' in kwargs:
        month = 'prev'
    else:
        month = 'next'

    if (wait_for_element(self, globaldata.ID, ID_ENDDATE, exec_js=True,
                                        timeout=globaldata.TIMEOUTSHORT) == False):
        failed = True
        failure = failure + "End Date widget not found.\n"
        print("FAILURE: End Date widget not found.")
    else:
        driver.find_element_by_id(ID_ENDDATE).click()
        wait_for_element(self, globaldata.CN, month)
        driver.find_element_by_class_name(month).click()            
        script = "obj = document.getElementsByClassName('day'); for (i=0;i<obj.length; i++) { " 
        script = script + "if (obj[i].textContent == '1') { return i;  } }"              
        el_num = driver.execute_script(script)
        driver.find_elements_by_class_name(CN_DAY)[el_num].click()
    
    return [failed, failure]


def wait_for_overlay(self):
    driver = self.driver
    script = "return document.getElementsByClassName('ui-widget-overlay').length"
    if (poll_until(self, script, "0", globaldata.TIMEOUTSHORT) == False):
        print("Script overlay never completed loading!")