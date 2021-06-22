from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException


class visibility_of(object):
    def __init__(self, element):
        self.element = element

    def __call__(self, browser):
        try:
            return len(browser._match_visible(self.element)) > 0
        except StaleElementReferenceException:
            return False


class invisibility_of(object):
    def __init__(self, element):
        self.element = element

    def __call__(self, browser):
        try:
            return len(browser._match_visible(self.element)) == 0
        except (NoSuchElementException, StaleElementReferenceException):
            return True


class staleness_of(object):
    def __init__(self, element):
        self.element = element

    def __call__(self, browser):
        try:
            # Calling any method forces a staleness check
            el.is_enabled()
            return False
        except StaleElementReferenceException:
            return True
