# coding=utf-8

import unittest
import os
import sys
import utils.extension.globalvar as gl
import utils.common_layer.path as Path
import datetime
from utils.extension.HTMLTestRunner_PY3 import HTMLTestRunner
import configparser
from utils.common_layer.config import ConfigPath
from utils.common_layer.config import TestCasePath


DIR_NAME = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(DIR_NAME)
conf = configparser.ConfigParser()
conf.read(DIR_NAME + ConfigPath[Path.get_script_name()].value, encoding='utf8')

# testcase path
case_path = os.path.join(DIR_NAME, TestCasePath[Path.get_script_name()].value)



def get_test_cases(dirpath, casefile):
    test_cases = unittest.TestSuite()
    if '*' in casefile:
        suites = unittest.defaultTestLoader.discover(dirpath, 'testcase*.py', top_level_dir=None)
    else:
        suites = unittest.defaultTestLoader.discover(dirpath, casefile + '.py', top_level_dir=None)
    for suite in suites:
        test_cases.addTests(suite)
    return test_cases

def env_init(devicename, port='', desired_caps=''):
    gl._init()
    gl.set_value('port', port)
    gl.set_value('desired_caps', desired_caps)
    start_time = datetime.datetime.now().strftime('%Y-%m-%d_%H%M_%S')
    gl.set_value('start_time', start_time)
    report_folder_path, screenshot_path, arg_count, test_url = Path.set_report_path(devicename)
        
    folderpath = gl.get_value('screenshot_path')
    if folderpath is None:
        gl.set_value('screenshot_path', screenshot_path)

    gl.set_value('test_url', test_url)
    basename = Path.get_script_name()
    gl.set_value('basename', basename)
    
    cases = get_test_cases(case_path, '*')

    if not os.path.exists(report_folder_path):
        os.makedirs(report_folder_path)

    if arg_count == 1 or arg_count == 2:
        with open(report_folder_path + '/HTMLReport.html', 'wb') as f:
            runner = HTMLTestRunner(f,
                                    title=devicename+' Test Report',
                                    description='',
                                    verbosity=2
                                    )
            runner.run(cases)


def get_device():
    return conf.get('BrowserInfo', 'device')


def pc_env_init():
    env_init('pc')