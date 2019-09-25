#coding=utf-8

import pages.login.BasePage as BasePage
import enum


class Elements(enum.Enum):
    username = "xpath>>>//*/input[@name='login']"
    password = "name>>>password"
    submit = "xpath>>>//*/input[@type='submit']"


class LoginPage(BasePage.BasePage):
    def click_button(self, element, wait_type='visibility'):
        self.driver.click_element(Elements[element].value, wait_type)

    def get_element_text(self, element, wait_type='visibility'):
        return self.driver.get_element_text(Elements[element].value, wait_type)

    def get_element_attribute(self, element, attribute, wait_type='visibility'):
        return self.driver.get_element_attribute(Elements[element].value, attribute, wait_type)

    def is_element_display(self, element, wait_type='visibility'):
        return self.driver.is_element_display(Elements[element].value, wait_type)

    def find_all_elements(self, elememt, wait_type='presence'):
        return self.driver.find_elements(Elements[elememt].value, wait_type)

    def select_by_visible_text(self, elememt, text, wait_type='presence'):
        self.driver.select_by_visible_text(Elements[elememt].value, text, wait_type)

    def input_element_text(self, elememt, text, wait_type='visibility'):
        self.driver.input_element_text(Elements[elememt].value, text, wait_type)

    def get_element_attribute(self, elememt, attribute, wait_type='visibility'):
        return self.driver.get_element_attribute(Elements[elememt].value, attribute, wait_type)
    
    def find_element(self, elememt, wait_type='presence'):
        return self.driver.find_element(Elements[elememt].value, wait_type)

    def execute_js(self, element, mode):
        self.driver.execute_js(element, mode)


