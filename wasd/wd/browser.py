from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from wasd.core import SettingsManager
from urllib.parse import urljoin, urlparse



class Browser:

    def click(self):
        print("Browser :: click()")


    def open(self, path):
        """
        Переходит по относительному URL (/login, /admin/users, etc ...)

        Args:
            path (str): Путь

        Examples:
            >>> browser.open("/")
            # На главную

            >>> browser.open("/admin")
            # В админку
        """
        # with self._step(f"Navigate to {path}"):
        self._driver_instance.get( urljoin(SettingsManager.get('url'), path) )


    def open_url(self, url):
        """
        Переходит по абсолютному URL.

        Args:
            url (str): URL

        Examples:
            >>> browser.open_url("https://google.com")
        """
        # with self._step(f"Navigate to URL {url}"):
        self._driver_instance.get(url)


    def fill_field(self, element, text):
        el = self._match_first_or_fail(element)
        el.clear()
        el.send_keys(text)


    _driver_instance    = None
    # _configuration      = Configuration()

    def get_driver(self):
        # global _driver_instance
        if not self._driver_instance:
            command_executor = "{0}://{1}:{2}{3}".format(
                SettingsManager._config['protocol'],
                SettingsManager.get('host'),
                SettingsManager.get('port'),
                SettingsManager.get('path')
            )
            self._driver_instance = webdriver.Remote(
                command_executor=command_executor,
                desired_capabilities=SettingsManager.get('capabilities')
            )
            self._driver_instance.implicitly_wait(5)
            self._driver_instance.maximize_window()

        return self._driver_instance


    def close_driver(self):
        if self._driver_instance:
            self._driver_instance.quit()
            self._driver_instance = None


    def _match_first_or_fail(self, element):
        self._enable_implicit_wait()
        els = self._match(element)
        self._disable_implicit_wait()
        if not els:
            raise Exception("Element {0} was not found.".format(element))
        return els[0]


    def _match(self, element):
        return self.finds(element)


    def find(self, element):
        context = self._driver_instance
        try:
            if element.ctx is not None:
                context = element.ctx.find()
            if element.by == 'xpath':
                if element.val.startswith('/'):
                    return context.find_element('xpath', f".{element.val}")
                else:
                    return context.find_element('xpath', f".//{element.val}")
            return context.find_element(*element.locator())
        except NoSuchElementException as e:
            e.msg = f"No such element: Unable to locate element: {element}"
            raise


    def finds(self, element):
        context = self._driver_instance
        try:
            if element.ctx is not None:
                context = element.ctx.find()
        except NoSuchElementException as e:
            e.msg = f"No such element: Unable to locate element: {element}"
            raise

        if element.by == 'xpath':
            if element.val.startswith('/'):
                return context.find_elements('xpath', f".{element.val}")
            else:
                return context.find_elements('xpath', f".//{element.val}")
        return context.find_elements(*element.locator())


    def _enable_implicit_wait(self):
        self._driver_instance.implicitly_wait( SettingsManager.get('implicit_timeout') )


    def _disable_implicit_wait(self):
        self._driver_instance.implicitly_wait(0)


    def _convert_key_modifier(self, keys):
        if not isinstance(keys, tuple):
            return (keys,)
        if keys[0] in ["ctrl", "contol"]:
            return (Keys.CONTROL, keys[1])
        if keys[0] == "alt":
            return (Keys.ALT, keys[1])
        if keys[0] == "shift":
            return (Keys.SHIFT, keys[1])
        if keys[0] == "meta":
            return (Keys.META, keys[1])
        return keys