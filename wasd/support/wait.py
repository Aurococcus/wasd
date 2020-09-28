import time
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException


POLL_FREQUENCY = 0.5  # How long to sleep inbetween calls to the method
IGNORED_EXCEPTIONS = (NoSuchElementException,)  # exceptions ignored during calls to the method


class Wait(object):
    def __init__(self, browser, timeout, poll_frequency=POLL_FREQUENCY, ignored_exceptions=None):
        self._browser = browser
        self._timeout = float(timeout)
        self._poll = poll_frequency
        if self._poll <= 0:
            self._poll = POLL_FREQUENCY
        exceptions = list(IGNORED_EXCEPTIONS)
        if ignored_exceptions is not None:
            try:
                exceptions.extend(iter(ignored_exceptions))
            except TypeError:  # ignored_exceptions is not iterable
                exceptions.append(ignored_exceptions)
        self._ignored_exceptions = tuple(exceptions)

    def __repr__(self):
        return '<{0.__module__}.{0.__name__} (session="{1}")>'.format(
            type(self), self._browser._driver_instance.session_id)

    def until(self, method, message=''):
        screen = None
        stacktrace = None

        end_time = time.time() + self._timeout
        while True:
            try:
                value = method(self._browser)
                if value:
                    return value
            except self._ignored_exceptions as exc:
                screen = getattr(exc, 'screen', None)
                stacktrace = getattr(exc, 'stacktrace', None)
            time.sleep(self._poll)
            if time.time() > end_time:
                break
        raise TimeoutException(message, screen, stacktrace)

    def until_not(self, method, message=''):
        end_time = time.time() + self._timeout
        while True:
            try:
                value = method(self._browser)
                if not value:
                    return value
            except self._ignored_exceptions:
                return True
            time.sleep(self._poll)
            if time.time() > end_time:
                break
        raise TimeoutException(message)
