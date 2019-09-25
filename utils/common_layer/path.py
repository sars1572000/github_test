#coding=utf-8

import sys
import os
import utils.extension.globalvar as gl
from utils.common_layer.config import PageUrl

#  get script name
def get_script_name():
    basename = os.path.basename(os.path.splitext(sys.argv[0])[0])
    return basename

#  setting folder path
def set_report_path(device):
    basename = get_script_name()
    if device == 'pc' and basename == 'github':
        url = PageUrl[basename].value

    if len(sys.argv) == 1:
        report_path = os.getcwd() + "/" + 'Test-Reports' + "/" + "Testcase" + "/" + device + "/" + basename + "/" + gl.get_value('start_time') + "/"
        screenshot_path = os.getcwd() + "/" + 'Test-Reports' + "/" + "ScreenShots" + "/" + "QA" + "/" + device + "/" + gl.get_value('start_time') + "/"
        arg_count = len(sys.argv)
    elif len(sys.argv) == 2:
        arg_count = len(sys.argv)
        url = sys.argv[1]
        report_path = os.getcwd() + "/" + 'Test-Reports' + "/" + "Testcase" + "/" + device + "/" + basename + "/" + gl.get_value('start_time') + "/"
        screenshot_path = os.getcwd() + "/" + 'Test-Reports' + "/" + "ScreenShots" + "/" + "QA" + "/" + device + "/" + gl.get_value('start_time') + "/"


    return report_path, screenshot_path, arg_count, url