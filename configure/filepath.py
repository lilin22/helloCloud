import os

'''根目录'''
PRO_PATH = os.path.dirname(os.path.realpath(__file__)[:os.path.realpath(__file__).find('configure')])  # 获取项目目录

'''一级目录'''
TEST_CASES_PATH = os.path.join(PRO_PATH, 'testCases')  # 测试用例存放目录
TEST_DATAS_PATH = os.path.join(PRO_PATH, 'testDatas')  # 测试文件存放目录
LOG_PATH = os.path.join(PRO_PATH, 'logs')  # 日志文件存放目录
REPORTS_PATH = os.path.join(PRO_PATH, 'reports')  # 测试报告存放目录

BROWSER_DRIVER_PATH = os.path.join(PRO_PATH,'chromedriver.exe')

PAGE_DATA_PATH = os.path.join(TEST_DATAS_PATH,'pageData')
