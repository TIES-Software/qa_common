from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoSuchFrameException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support.expected_conditions import (_find_element, _find_elements, _element_if_visible)

class exact_text_to_be_present_in_element(object):
    """ An expectation for checking if the given text is present in the
    specified element. Must be an exact match.
    Custom function for TIES
    locator, text
    """
    def __init__(self, locator, text_):
        self.locator = locator
        self.text = text_

    def __call__(self, driver):
        try :
            element_text = _find_element(driver, self.locator).text
            return self.text == element_text
        except StaleElementReferenceException:
            return False

class child_element_to_be_visible_in_element(object):
    """ An expectation for checking if the given element is visible in the
    parent element.
    Custom function for TIES
    locator, parent_element
    """
    def __init__(self, locator, parent_element):
        self.locator = locator
        self.parent = parent_element

    def __call__(self, driver):
        try :
            child_element = self.parent.find_element(*self.locator)
            return _element_if_visible(child_element)
        except StaleElementReferenceException:
            return False

class element_text_to_be_non_null(object):
    """ An expectation for checking if any text is present in the
    specified element.
    Custom function for TIES
    locator
    """
    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver):
        try :
            element = _find_element(driver, self.locator)
            if element.text is not "":
                return element
        except StaleElementReferenceException:
            return False
