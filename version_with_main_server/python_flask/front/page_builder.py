from abc import ABC, abstractmethod
from turtledemo import colormixer

from itsdangerous import NoneAlgorithm


class PageObject(ABC):
    @abstractmethod
    def get_html(self) -> str:
        pass
    @abstractmethod
    def get_wml(self) -> str:
        pass

class Card(PageObject):
    def __init__(self, title: str, lines: list,  id: str = None, time_reload: int = None):
        """

        :param lines: lists from page objects
        :param title: title in wml, label in html
        :param id: id for went in wml card
        :param time_reload: time auto reload page
        """
        self.lines = lines
        self.title = title
        self.id = id
    def get_wml(self) -> str:
        card = f'<card title=\"{self.title}\"'
        if not self.id is None:
            card += f' id=\"{self.id}\"'
        card += '>'

        for line in self.lines:
            if isinstance(line, list):
                for obj in line:
                    card += obj.get_wml()
            elif isinstance(line, PageObject):
                card += line.get_wml()
            else:
                raise Exception("Object in argument lines not is list or PageObject.")
            card += '<br/>'

        card += '</card>'
        return card

    def get_html(self) -> str:
        card = f'<h1>{self.title}<h1/>'

        for line in self.lines:
            if isinstance(line, list):
                for obj in line:
                    card += obj.get_html()
            elif isinstance(line, PageObject):
                card += line.get_html()
            else:
                raise Exception("Object in argument lines not is list or PageObject.")
            card += '<br/>'

        card += '<br/><br/><br/>'
        return card

class Label(PageObject):
    def __init__(self, text: str, size: int = 0, color: str = None):
        """
        demonstrate text
        :param text: text in label
        :param size: 0 - 3 size
        """
        if not 0 <= size <= 3:
            raise ValueError(f"Size in class Label have error value: {size}. It must be in range from 1 to 3.")
        self.text = text
        self.size = size
        self.color = color

    def get_wml(self) -> str:
        if self.color is None:
            return f"<p>{self.text}</p>"
        else:
            return f"<p color=\"{self.color}\">{self.text}</p>"

    def get_html(self) -> str:
        page_obj = str()
        color = self.color
        if not color is None:
            page_obj += f"<font color=\"{color}\">"
        page_obj += f"<p size={self.size * 10 + 10}>{self.text}</p>"
        if not color is None:
            page_obj += "</font>"
        return page_obj

class Url(PageObject):
    def __init__(self,title: str, url: str):
        self.utl = url
        self.title = title

    def get_wml(self) -> str:
        return f"<a href={self.utl}>{self.title}</a>"
    def get_html(self) -> str:
        return f"<a href={self.utl}>{self.title}</a>"

class UrlCard(PageObject):
    def __init__(self,title: str, url: str):
        if url.startswith("#"):
            self.utl = url
        else:
            self.url = "#" + url
        self.title = title

    def get_wml(self) -> str:
        return f"<a href={self.utl}>{self.title}</a>"
    def get_html(self) -> str:
        return ""
# ----------------------------- FORM SEND ----------------------------------------
class InputPageObject(PageObject):
    def get_wml(self) -> str:
        pass
    def get_html(self) -> str:
        pass
    @abstractmethod
    def get_wml_post_field(self):
        pass

class Form(PageObject):
    def __init__(self, inputs: list[InputPageObject], title: str = '', button_title = 'Отправить', url: str = None):
        """

        :param title: designation
        """
        self.url = url
        self.inputs = inputs
        self.title = title
        self.button_title = button_title

    def get_html(self) -> str:
        form = str()
        if self.url is None:
            form += '<form>'
        else:
            form += f'<form action=\"{self.url}\">'
        for inp in self.inputs:
            form += inp.get_html()
        form += f'<br/><button type="submit">{self.button_title}</button></form>'
        return form
    def get_wml(self) -> str:
        form = str()
        for inp in self.inputs:
            form += inp.get_wml()
        return form

class TextBox(InputPageObject):
    """
    TextBox - class denote input text box
        for user input and send form to server
    """
    def __init__(self, title: str, param: str, default_value: str = None):
        self.title = title
        self.param = param
        self.default_value = default_value
    def get_wml(self) -> str:
        text_box = f"<p>{self.title}</p>"
        text_box += f"<input type=\"text\" name=\"{self.param}\""
        if not self.default_value is None:
            text_box += f" value=\"{self.default_value}\""
        text_box += "/>"
        return text_box
    def get_html(self) -> str:
        text_box = f"<input type=\"text\" name=\"{self.param}\" placeholder=\"{self.title}\""
        if not self.default_value is None:
            text_box += f" value=\"{self.default_value}\""
        text_box += f"/>"
        return text_box
    def get_wml_post_field(self):
        return ""

class CheckBox(InputPageObject):
    """
    CheckBox - class denote input check box
        for user input and send form to server
    """
    def __init__(self, title: str, param: str):
        self.title = title
        self.param = param
    def get_wml(self) -> str:
        return f"<p>{self.title}</p><input type=\"text\" name=\"{self.param}\"/><br/>"
    def get_html(self) -> str:
        return f"<p>{self.title}: <input type=\"checkbox\" name=\"{self.param}\"> </p>"
    def get_wml_post_field(self):
        return ""

class ConstParam(InputPageObject):
    """
    ConstParam - class denote const param
        and send form to server
    """
    def __init__(self, param: str, value: str):
        self.value = value
        self.param = param
    def get_wml(self) -> str:
        return f"<p>{self.title}</p><input type=\"text\" name=\"{self.param}\"/><br/>"
    def get_html(self) -> str:
        return f"<input type=\"hidden\" name=\"{self.param}\" value=\"{self.value}\">"
    def get_wml_post_field(self):
        return ""

def create_page(cards: list, is_wml: bool = False):
    """
    create page from page objects
    :param data: this list of card list of string list of PageObjects
    :param is_wml: is wml page, if False, then html
    :return:
    """
    page = ''
    if is_wml:
        page += '<?xml version="1.0"?><!DOCTYPE wml PUBLIC "-//WAPFORUM//DTD WML 1.1//EN" "http://www.wapforum.org/DTD/wml_1.1.xml"><wml>'

    for card in cards:
        if is_wml:
            page += card.get_wml()
        else:
            page += card.get_html()

    if is_wml:
        page += '</wml>'

    return page

if __name__ == "__main__":
    page = create_page([
        Card([
            Label("Hello user!")
        ])
    ],
    True)

    print(page)