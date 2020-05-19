from wasd.core import SettingsManager
import time
from selenium.webdriver.support.events import AbstractEventListener


class ElementHighlightListener(AbstractEventListener):
    '''
    Подсвечивает элемент с которым работает
    '''
    
    inset_shadow = 'box-shadow: inset 0 0 5px 1px #0a0;'


    def after_find(self, by, value, driver):
        self.highlight(by, value, driver)


    def highlight(self, by, value, driver):
        if by == 'css selector':
            elem = self.js_find_by_css(driver, value)
        if by == 'xpath':
            elem = self.js_find_by_xpath(driver, value)

        original_style = self.get_style(driver, elem)
        concat_style = f"{original_style};{self.inset_shadow}"

        self.apply_style(driver, elem, concat_style)
        time.sleep(.2)
        self.apply_style(driver, elem, original_style)


    def get_style(self, driver, web_element):
        get_style_script = '''
            if (arguments[0]) {
                return arguments[0].getAttribute('style');
            } else {
                return "";
            }'''


        return driver.execute_script(get_style_script, web_element)


    def apply_style(self, driver, web_element, style):
        apply_style_script = '''
            if (arguments[0]) {{
                arguments[0].setAttribute('style', '{0}');
            }}'''.format(style)

        return driver.execute_script(apply_style_script, web_element)


    def js_find_by_css(self, driver, selector):
        script = f'''return document.querySelector({selector.__repr__()});'''
        return driver.execute_script(script)


    def js_find_by_xpath(self, driver, selector):
        script = f'''
        return document.evaluate({selector.__repr__()}, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
        '''
        return driver.execute_script(script)
