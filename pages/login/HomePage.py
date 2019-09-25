#coding=utf-8

import pages.login.BasePage as BasePage
import enum


class Elements(enum.Enum):
    sign_in_button = "xpath>>>//*/a[@href='/login']"
    avatar_img = "xpath>>>//*/summary[@class='Header-link']/img[@class='avatar']"
    user_name = "xpath>>>//*/strong[@class='css-truncate-target']"



class HomePage(BasePage.BasePage):
    def click_button(self, element, wait_type='visibility'):
        self.driver.click_element(Elements[element].value, wait_type)

    def get_element_text(self, element, wait_type='visibility'):
        return self.driver.get_element_text(Elements[element].value, wait_type)





