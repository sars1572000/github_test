#coding=utf-8

import unittest
from pages.login.LoginPage import LoginPage
from pages.login.HomePage import HomePage
from utils.extension.SeleniumLayer import Selenium
import utils.extension.globalvar as gl
from utils.common_layer.screenshot import ScreenShot
import sys
import configparser
import os


DIR_NAME = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(DIR_NAME)
conf = configparser.ConfigParser()
conf.read(DIR_NAME + "/configs/github/setting.conf", encoding='utf8')

class LoginTest(unittest.TestCase):
    # get script name
    basename = gl.get_value('basename')
    # screenshot folder path
    folderpath = gl.get_value('screenshot_path')

    device = conf.get('BrowserInfo', 'device')

    check = True
    test_url = gl.get_value('test_url')

    def setUp(self):
        self.check = True
        self.driver = Selenium()
        self.driver.init()
        self.driver.open_link(self.test_url)
        self.home_page = HomePage(self.driver)
        self.login_page = LoginPage(self.driver)

    def tearDown(self):
        if self.check == False:
            picture_name = self.basename + "(" + self.id().split('.')[-1] + ")"
            ss = ScreenShot(self.driver, self.folderpath, picture_name)  
            ss.screenshot()
        self.driver.quit()

    def test_no_such_user(self):  # 1.no such user
        try:
            self.home_page.click_button("sign_in_button")
            self.login_page.input_element_text('username', "test25178489@gmail.com")
            self.login_page.input_element_text('password', "25178489test")
            self.login_page.click_button('submit')
            self.home_page.click_button('avatar_img')

            if "test25178489" in self.home_page.get_element_text('user_name'):
                print("pass")
            else:
                print("username= " + self.home_page.get_element_text('user_name'))
                raise Exception
        except Exception:
            self.check = False
            raise

