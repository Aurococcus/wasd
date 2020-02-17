from lxml import etree
from cssselect import GenericTranslator, SelectorError


class Locator:

    minimal_xml = '<!DOCTYPE _[<!ELEMENT _ EMPTY>]><_/>'

    @classmethod
    def contains(cls, element, *text):
        """
        Находит элемент, содержащий текст.
        Можно передать CSS или XPath, однако они будут превращены в XPath.
        """
        condition = ""
        for string in text:
            condition += "[contains(., {})]".format(
                GenericTranslator().xpath_literal(string)
            )

        xpath = '{0}{1}'.format(
            cls.to_xpath(element),
            condition
        )
        return xpath

    @classmethod
    def equal(cls, element, text):
        xpath = '{0}[{1}]'.format(
            cls.to_xpath(element),
            ".= %s" % GenericTranslator().xpath_literal(text)
        )
        return xpath

    @classmethod
    def element_at(cls, locator, position):
        """
        Элемент по индексу.
        Если передать отрицательное значение, то счёт пойдёт с конца.
        Первый элемент имеет индекс 1.
        """
        if isinstance(position, int) and position < 0:
            position += 1
            position = 'last()-{0}'.format(abs(position))

        if position == 0:
            raise ValueError('0 is not valid element position. '
                             'XPath expects first element to have index 1')
        return "({0})[position()={1}]".format(cls.to_xpath(locator), position)

    @classmethod
    def to_xpath(cls, selector):
        """
        Конвертирует CSS селектор в XPath.
        Если передать валидный XPath, то вернёт его без изменений.
        """
        try:
            return GenericTranslator().css_to_xpath(selector)
        except SelectorError:
            if cls.is_xpath(selector):
                return selector
        return None

    @classmethod
    def is_xpath(cls, selector):
        """
        Проверяет, что переданный слектор - XPath
        """
        doc = etree.XML(cls.minimal_xml)
        try:
            doc.xpath(selector)
        except etree.XPathEvalError:
            return False
        return True

    @classmethod
    def is_css(cls, selector):
        """
        Проверяет, что переданный слектор - CSS
        """
        try:
            GenericTranslator().css_to_xpath(selector)
        except SelectorError:
            return False
        return True
