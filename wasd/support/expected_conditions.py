from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException


def _element_if_visible(element, visibility=True):
    return element if element.is_displayed() == visibility else False


class visibility_of(object):
    def __init__(self, element):
        self.element = element

    def __call__(self, browser):
        try:
            return _element_if_visible(browser._match_first_or_fail(self.element))
        except StaleElementReferenceException:
            return False


class invisibility_of(object):
    def __init__(self, element):
        self.element = element

    def __call__(self, browser):
        try:
            return _element_if_visible(
                browser._match_first_or_fail(self.element),
                visibility=False,
            )
        except (NoSuchElementException, StaleElementReferenceException):
            return True


class staleness_of(object):
    def __init__(self, element):
        self.element = element

    def __call__(self, browser):
        try:
            # Calling any method forces a staleness check
            browser._match_first_or_fail(self.element).is_enabled()
            return False
        except StaleElementReferenceException:
            return True
