class BasePage(object):

    def __init__(self, driver):
        self.driver = driver
        self.driver.set_implicitly = 10
