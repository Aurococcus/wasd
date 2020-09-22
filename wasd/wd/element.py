# -*- coding: utf-8 -*-
from selenium.webdriver.common.by import By
from wasd.util.locator import Locator
from wasd.common.exceptions import MalformedLocatorException


# https://github.com/mfalesni/selenium-smart-locator

class Element:
    BY_MAPPING = {
        'partial_link_text':    By.PARTIAL_LINK_TEXT,
        'css':                  By.CSS_SELECTOR,
        'class_name':           By.CLASS_NAME,
        'link_text':            By.LINK_TEXT,
        'tag':                  By.TAG_NAME,
        'name':                 By.NAME,
        'xpath':                By.XPATH,
        'id':                   By.ID
    }
    REVERSE_BY_MAPPING = {v: k for k, v in BY_MAPPING.items()}

    def _get_by(self, by):
        try:
            if by in self.REVERSE_BY_MAPPING:
                by_ = self.REVERSE_BY_MAPPING[by]
            else:
                by_ = by
            return self.BY_MAPPING[by_]
        except KeyError:
            raise ValueError(f"'{by}' is not a recognized resolution strategy")


    def __init__(self, *args):
        ctx = None
        if len(args) == 1:
            if isinstance(args[0], Element):
                by = args[0].by
                val = args[0].val
                ctx = args[0].ctx
            elif isinstance(args[0], tuple):
                by = args[0][0]
                val = args[0][1]
            elif isinstance(args[0], str):
                by = By.CSS_SELECTOR if Locator.is_css(args[0]) else By.XPATH
                val = args[0]
        elif len(args) == 2:
            if isinstance(args[0], Element):
                by = args[0].by
                val = args[0].val
                ctx = args[1]
            elif isinstance(args[0], str):
                by = By.CSS_SELECTOR if Locator.is_css(args[0]) else By.XPATH
                val, ctx = args[0], args[1]
            elif isinstance(args[0], tuple):
                by = args[0][0]
                val = args[0][1]
                ctx = args[1]
        else:
            raise MalformedLocatorException(f"Wrong parameters specified for locator: {args}")


        self.by = self._get_by(by)
        self.val = val
        self.ctx = ctx


    def locator(self):
        '''Возвращает кортеж (By, Value)'''
        return (self.by, self.val)


    def __str__(self):
        return "({0} = '{1}', ctx = '{2}')".format(self.by, self.val, self.ctx)


class ShadowElement(Element):

    def __str__(self):
        return "(ShadowRoot::{0} = '{1}', ctx = '{2}')".format(self.by, self.val, self.ctx)
