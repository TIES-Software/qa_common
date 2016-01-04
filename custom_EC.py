from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoSuchFrameException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support.expected_conditions import (_find_element, _find_elements)

class exact_text_to_be_present_in_element(object):
    """ An expectation for checking if the given text is present in the
    specified element. Must be an exact match.
    Custom function for FeePay
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
