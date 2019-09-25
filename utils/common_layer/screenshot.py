#coding=utf-8

import os


class ScreenShot(object):

    def __init__(self, driver, folderpath, image_name):
        self.folderpath = folderpath
        self.driver = driver
        self.image_name = image_name

    def screenshot(self):
        #  if not exists folder name screenshots, create one
        if not os.path.exists(self.folderpath):
            os.makedirs(self.folderpath)

        index = 0
        while True:
            if index == 0:
                image_path = self.folderpath + self.image_name + ".png"
            elif index > 0:
                image_path = self.folderpath + self.image_name + str(index) + ".png"

            if os.path.exists(image_path):
                index += 1
            elif not os.path.exists(image_path):
                break

        self.driver.GetBrowserScreenShot(image_path)
        print('ScreenShot: ' + image_path)
