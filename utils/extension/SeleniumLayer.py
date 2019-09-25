#coding=utf-8

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
import os
import sys
import configparser
import enum
import utils.extension.globalvar as gl
from utils.common_layer.config import ConfigPath

class WaitType(enum.Enum):
    presence = EC.presence_of_element_located
    visibility = EC.visibility_of_element_located
    invisibility = EC.invisibility_of_element_located

DIR_NAME = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(DIR_NAME)
conf = configparser.ConfigParser()
conf.read(DIR_NAME + ConfigPath[gl.get_value('basename')].value, encoding='utf8')

class Selenium(object):
       
    def init(self):
        browser_name = conf.get('BrowserInfo', 'browser_name')
        browser_type = conf.get('BrowserInfo', 'browser_type')
        device = conf.get('BrowserInfo', 'device')

        if os.name == 'nt':
            chrome_path = conf.get("ChromeForWindows", "chrome_path")  # Windows
        elif os.name == 'posix':
            chrome_path = conf.get("ChromeForMac", "chrome_path")  # Mac

        if browser_name == 'chrome' and browser_type == 'ui' and device == 'pc':
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--disable-infobars') # disable-notifications
            chrome_options.add_argument('--start-maximized') # Windows size maximized
            chrome_options.add_argument('--start-fullscreen')  # Mac size maximized
            chrome_options.add_argument('--allow-running-insecure-content') #don't pupup non safe content page
            chrome_path = os.path.join(DIR_NAME, chrome_path)
            driver = webdriver.Chrome(executable_path=chrome_path, chrome_options=chrome_options)
        elif browser_name == 'chrome' and browser_type == 'headless' and device == 'pc':
            chrome_options_headless = webdriver.ChromeOptions()
            chrome_options_headless.add_argument('--window-size=1920,974')
            chrome_options_headless.add_argument('--headless')
            chrome_options_headless.add_argument('--no-sandbox')
            chrome_path = os.path.join(DIR_NAME, chrome_path)
            driver = webdriver.Chrome(executable_path=chrome_path, chrome_options=chrome_options_headless)
        elif browser_name == 'chrome' and browser_type == 'ui' and device == 'mobile':
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--disable-infobars') # disable-notifications
            chrome_options.add_argument('--window-size=736,414') # Windows size maximized
            chrome_options.add_argument('--allow-running-insecure-content') #don't pupup non safe content page
            chrome_path = os.path.join(DIR_NAME, chrome_path)
            driver = webdriver.Chrome(executable_path=chrome_path, chrome_options=chrome_options)
        elif browser_name == 'chrome' and browser_type == 'headless' and device == 'mobile':
            chrome_options_headless = webdriver.ChromeOptions()
            chrome_options_headless.add_argument('--window-size=736,414')
            chrome_options_headless.add_argument('--headless')
            chrome_options_headless.add_argument('--no-sandbox')
            chrome_path = os.path.join(DIR_NAME, chrome_path)
            driver = webdriver.Chrome(executable_path=chrome_path, chrome_options=chrome_options_headless) 
        elif device == 'android':
            driver = webdriver.Remote('http://localhost:%s/wd/hub' % gl.get_value('port'), gl.get_value('desired_caps'))
            driver.orientation = "LANDSCAPE"
        elif browser_name == 'safari':
            driver = webdriver.Safari()

        self.driver = driver

    def find_element(self, selector, wait_type):
        """
        find the the element, and return the element

        Usage:
        driver.find_element("id>>>username")
        """
        try:
            _wait_element_localed(self.driver, selector, wait_type)
            element = self.driver.find_element(*_selector_to_by(selector))
        except Exception:
            element = ''

        return element

    def find_elements(self, selector, wait_type):
        """
        find the the element, and return the element

        Usage:
        driver.find_elements("id>>>username")
        """
        try:
            _wait_element_localed(self.driver, selector, wait_type)
            elements = self.driver.find_elements(*_selector_to_by(selector))
        except Exception:
            elements = []

        return elements

    def open_link(self, url):
        """
        open target url

        Usage:
        driver.open_link("http://192.168.128.191:20380/member")
        """
        self.driver.get(url)

    def set_max_window(self):
        """
        Set browser window maximize

        Usage:
        driver.set_max_window
        """
        self.driver.maximize_window()

    def set_window_size(self, wide, high):
        """
        Set browser window winde and high

        Usage:
        driver.set_window_size(wide, high)
        """

        self.driver.set_window_size(wide, high)

    def input_element_text(self, selector, text, wait_type):
        """
        type text into the selected element。

        Usage:
        driver.input_element_text("id>>>username", "test")
        """

        _wait_element_localed(self.driver, selector, wait_type)
        element = self.find_element(selector, wait_type)
        element.clear()
        element.send_keys(text)

    def input_element_clear(self, selector, wait_type):
        """
        Clear the content of the input box

        Usage:
        driver.input_element_clear("id>>>username")
        """

        _wait_element_localed(self.driver, selector, wait_type)
        element = self.find_element(selector, wait_type)
        element.clear()

    #def input_element_clear_enter(self, selector, text):
    #    """
    #    Clear text and enter new text into element

    #    Usage:
    #    driver.input_element_clear_enter("id>>>username", "test")
    #    """
    #    _wait_element_localed(self.driver, selector)
    #    element = self.get_element(selector)
    #    element.clear()
    #    element.click()
    #    element.send_keys(text)

    def click_element(self, selector, wait_type):
        """
        click the ang element can be clicked, like: text, image, check box, button. radio button etc...

        Usage:
        driver.click_element("id>>>username")
        """
        _wait_element_localed(self.driver, selector, wait_type)
        element = self.find_element(selector, wait_type)
        element.click()

    #def right_click(self, selector):
    #    """
    #    Right clcik element

    #    Usage:
    #    driver.right_click("id>>>username")
    #    """
    #    _wait_element_localed(self.driver, selector)
    #    element = self.find_element(selector)
    #    ActionChains(self.driver).context_click(element).perform()

    #def double_click(self, selector):
    #    """
    #    Double click element

    #    Usage:
    #    driver.double_click("id>>>username")
    #    """

    #    _wait_element_localed(self.driver, selector)
    #    element = self.find_element(selector)
    #    ActionChains(self.driver).double_click(element)

    #def click_text(self, text):
    #    """
    #    click the lick text element

    #    Usage:
    #    driver.click_text("test")
    #    """

    #    self.driver.find_element_by_partial_link_text(text)

    #def drag_and_drop(self, source_selector, target_selector):
    #    """
    #    Drags the source_selector element a certain distance and then drop it.

    #    Usage:
    #    driver.drag_and_drop("id>>>username", "id>>>password")
    #    """

    #    _wait_element_localed(self.driver, source_selector)
    #    source = self.get_element(source_selector)
    #    _wait_element_localed(self.driver, target_selector)
    #    target = self.get_element(target_selector)
    #    ActionChains(self.driver).drag_and_drop(source, target)

    def close(self):
        """
        close currect the window

        Usage:
        driver.close()
        """
        self.driver.close()

    def quit(self):
        """
        Quit the driver and close all the windows

        Usage:
        driver.quit
        """
        self.driver.quit()

    #def submit(self, selector):
    #    """
    #    Submit the form

    #    Usage:
    #    driver.submit("class>>>submit")
    #    """
    #    _wait_element_localed(self.driver, selector)
    #    element = self.find_element(selector)
    #    element.submit()

    def refresh_page(self):
        """
        Refresh the current page

        Usage:
        driver.refresh_page()
        """
        self.driver.refresh()

    def execute_js(self, element, mode):
        """
        Execute JavaScript script in the current window/frame

        Usage:
        element = driver.find_element_by_id("myid")
        driver.execute_script("arguments[0].click();", element)
        """
        if mode == 'click':
            self.driver.execute_script("arguments[0].click();", element)

        #self.driver.execute_script(script)

    def get_element_attribute(self, selector, attribute, wait_type):
        """
        Get the value of an element attribute

        Usage:
        driver.get_element_attribute("id>>>username", "class")
        """
        _wait_element_localed(self.driver, selector, wait_type)
        element = self.find_element(selector, wait_type)
        attr = element.get_attribute(attribute)

        return attr

    def get_element_text(self, selector, wait_type):
        """
        Get the text information of the element

        Usage:
        driver.get_element_text("id>>>username")
        """

        _wait_element_localed(self.driver, selector, wait_type)
        element = self.find_element(selector, wait_type)
        text = element.text

        return text

    def get_window_title(self):
        """
        Get current window title

        Usage:
        driver.get_window_title()
        """
        title = self.driver.title
        return title

    def get_currect_url(self):
        """
        Get the URL address of the current page

        Usage:
        driver.get_currect_url()
        """

        url = self.driver.current_url
        return url

    def is_element_display(self, selector, wait_type):
        """
        Check the element Whether the element is visible to a user.

        Usage:
        driver.is_element_display("id>>>username")
        """
        element = self.find_element(selector, wait_type)
        if element == '':
            return False
        else:
            return self.find_element(selector, wait_type).is_displayed()

        #return True if self.find_element(selector, wait_type).is_displayed() else False


    def set_implicitly(self, seconds):
        """
        Implicitly wait.All elements on the page.

        Usage:
        driver.set_implicitly(10)
        """
        self.driver.implicitly_wait(seconds)

    def accept_alert(self):
        """
        Accept warning box

        Usage:
        driver.accept_alert()
        """
        self.driver.switch_to_alert().accept()

    def dismiss_alert(self):
        """
        Dismiss the alert

        Usage:
        driver.dismiss_alert()
        """
        self.driver.switch_to_alert().dismiss()

    def switch_to_frame(self, selector, wait_type):
        """
        Switch to the specified frame

        Usage:
        driver.switch_to_frame("id>>>username")
        """
        _wait_element_localed(self.driver, selector, wait_type)
        iframe_element = self.find_element(selector, wait_type)
        self.driver.switch_to_frame(iframe_element)

    def switch_to_default_content(self):
        """
        Returns the current form machine form at the next higher level.
        Corresponding relationship with switch_to_frame () method.

        Usage:
        driver.switch_to_default_content()
        """
        self.driver.switch_to.default_content()

    def open_new_window(self, selector, wait_type):
        """
        Open the new window and switch to the newly opened windows

        Usage:
        driver.open_new_window("id>>>username")
        """
        current_window = self.driver.current_window_handle
        element = self.find_element(selector, wait_type)
        element.click()
        all_handles = self.driver.window_handles
        for handle in all_handles:
            if handle != current_window:
                self.driver.switch_to_window(handle)

    def open_new_tab(self, url):
        """
        For Windows system method , open a new tab to open new url and switch to the newly tab.

        Usage:
        driver.open_new_tab("http://192.168.128.191:20380/member")
        """
        current_window = self.driver.current_window_handle
        ActionChains(self.driver).send_keys(Keys.CONTROL + 't').perform()
        all_handles = self.driver.window_handles
        for handle in all_handles:
            if handle != current_window:
                self.driver.switch_to_window(handle)
        self.driver.get(url)

    def open_new_table_for_Mac(self, url):
        """
        For MacOS method , open a new tab to open new url and switch to the newly tab.

        Usage:
        driver.open_new_tab_for_Mac("https://www.baidu.com/")
        """
        ActionChains(self.driver).send_keys(Keys.COMMAND + 't').perform()
        self.driver.get(url)

    #def take_screenshot(self, filepath):
    #    """
    #    Get the current window screenshot.

    #    Usage:
    #    driver.take_screenshot('../test.png')
    #    """
    #    self.driver.get_screenshot_as_file(filepath)

    @property
    def wd(self):
        """
        Return the original driver,Can use webdriver API.

        Usage:
        driver.wd
        """
        return self.driver

    def GetBrowserScreenShot(self, path):
        self.driver.save_screenshot(path)

    def select_by_value(self, selector, value, wait_type):
        _wait_element_localed(self.driver, selector, wait_type)
        select = Select(self.find_element(selector, wait_type))
        select.select_by_value(value)

    def select_by_visible_text(self, selector, text, wait_type):
        _wait_element_localed(self.driver, selector, wait_type)
        select = Select(self.find_element(selector, wait_type))
        select.select_by_visible_text(text)


def _selector_to_by(selector):
    """
    Change the selector to ('by', 'value') mode

    :param selector: "id>>>username"
    :return: ('by', 'value')
    """
    if ">>>" not in selector:
        raise NameError("selector syntax errors, lack of '>>>'")

    by = selector.split('>>>')[0]
    value = selector.split('>>>')[1]

    if by == "id":
        by = By.ID
    elif by == "name":
        by = By.NAME
    elif by == "link_text":
        by = By.LINK_TEXT
    elif by == "css" or by == "css_selector":
        by = By.CSS_SELECTOR
    elif by == "xpath":
        by = By.XPATH
    elif by == "tag" or by == "tag_name":
        by = By.TAG_NAME
    elif by == "class" or by == "class_name":
        by = By.CLASS_NAME
    elif by == "text" or by == "partial_link_text":
        by = By.PARTIAL_LINK_TEXT
    else:
        raise NameError("please enter correct element attribute, 'id','name','xpath','css','tag','class','text','link_text'.")

    return by, value


def _wait_element_localed(driver, selector, wait_type,time_out=10, interval=0.5):
    """
    Wait for an element localed on DOM.
    """
    type = WaitType[wait_type]
    type = type.value
    WebDriverWait(driver, time_out, interval).until(type(_selector_to_by(selector)))