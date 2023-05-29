import random
from typing import Optional
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from single_pattern import driver
from common import utils
from common.configLog import logger
import time, re
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from common.processYaml import processYaml



default_timeout = 10
default_f_timeout = 5
default_frequency = 0.5
method_dict = {'xpath':By.XPATH, 'css':By.CSS_SELECTOR}


class bases:

    def __init__(self):
        pass

    @utils.catch_exception
    def start_browser(driverPath,urlPath):
        try:
            chrome_service = Service(executable_path=driverPath)
            options = Options()
            options.add_argument('lang=zh-CN.UTF-8')
            # options.add_argument('--headless')
            driver.driver.driver1 = webdriver.Chrome(service=chrome_service, options=options)
            driver.driver.driver1.maximize_window()
            driver.driver.driver1.get(urlPath)
        except BaseException as e:
            raise Exception(logger.error('启动报错%s' % e))

    @classmethod
    def get_pageData(self, file, element):
        # logger.info('正在查询元素%s定位数据'%element)
        read_data = processYaml(file).read_yaml()
        if element in read_data.keys():
            # logger.info('找到目标元素定位数据: [%s]' % read_data[element])
            return read_data[element]
        else:
            raise Exception('未找到元素测试数据,请检查')

    @classmethod
    def find_element(self, method: str, data: str, timeout: int = default_timeout, f_timeout: int = default_f_timeout):
        # logger.info('正在通过%s: [%s]定位元素'% (method, data))
        wait: WebDriverWait = WebDriverWait(driver.driver.driver1, f_timeout, default_frequency)
        status = 0
        element = None
        endtime = time.time()
        while time.time() < endtime + timeout:
            try:
                element = wait.until(EC.visibility_of_element_located((method_dict[method], data)))
                status = 1
                break
            except BaseException as e:
                logger.error(e)
                # time.sleep(0.5)
        if status == 1:
            # logger.info('元素定位成功')
            return element
        else:
            raise Exception('元素定位失败')

    @classmethod
    def find_element_clickable(self, method: str, data: str, timeout: int = default_timeout, f_timeout: int = default_f_timeout):
        # logger.info('正在通过%s: [%s]定位元素'% (method, data))
        wait: WebDriverWait = WebDriverWait(driver.driver.driver1, f_timeout, default_frequency)
        status = 0
        element = None
        endtime = time.time()
        while time.time() < endtime + timeout:
            try:
                element = wait.until(EC.element_to_be_clickable((method_dict[method], data)))
                status = 1
                break
            except BaseException as e:
                logger.error(e)
                # time.sleep(0.5)
        if status == 1:
            # logger.info('元素定位成功')
            return element
        else:
            raise Exception('元素定位失败')

    @classmethod
    def find_elements(self, method: str, data: str, timeout: int = default_timeout, f_timeout: int = default_f_timeout):
        # logger.info('正在通过%s: [%s]定位元素'% (method, data))
        wait: WebDriverWait = WebDriverWait(driver.driver.driver1, f_timeout, default_frequency)
        status = 0
        element_list = []
        endtime = time.time()
        while time.time() < endtime + timeout:
            try:
                element_list = wait.until(EC.visibility_of_all_elements_located((method_dict[method], data)))
                status = 1
                break
            except BaseException as e:
                logger.error(e)
                # time.sleep(0.5)
        if status == 1:
            # logger.info('元素定位成功')
            return element_list
        else:
            raise Exception('元素定位失败')

    @classmethod
    def find_element_by_js(self, js: str, timeout: int = default_timeout):
        # logger.info('正在通过JS: [%s]' % js)
        status = 0
        element = None
        enetime = time.time()
        while time.time() < enetime + timeout:
            try:
                element = driver.driver.driver1.execute_script(js)
                status = 1
                break
            except BaseException as e:
                logger.error(e)
                # time.sleep(0.5)
        if status == 1:
            # logger.info('元素定位成功')
            return element
        else:
            raise Exception('元素定位失败')

    @classmethod
    def check_text_by_pageSource(self, text: str, timeout: int = default_timeout) -> bool:
        # logger.info('正在通过页面源码查询文本: %s' % text)
        re_obj = re.compile(text)
        endtime = time.time()
        status = 0
        while time.time() < endtime + timeout:
            source = driver.driver.driver1.page_source
            res = re_obj.findall(source)
            logger.info('正则匹配结果: %s' % list(set(res)))
            if len(res) != 0:
                # logger.info('文本已显示')
                status = 1
                break
            else:
                # logger.error('未匹配成功')
                time.sleep(0.2)
                continue
        if status == 1:
            return True
        else:
            return False

    @classmethod
    def check_text_disappear_by_pageSource(self, text: str, timeout: int = default_timeout) -> bool:
        # logger.info('正在通过页面源码查询文本: %s' % text)
        re_obj = re.compile(text)
        endtime = time.time()
        status = 0
        while time.time() < endtime + timeout:
            source = driver.driver.driver1.page_source
            res = re_obj.findall(source)
            logger.info('正则匹配结果: %s' % list(set(res)))
            if len(res) == 0:
                # logger.info('文本消失')
                status = 1
                break
            else:
                # logger.error('文本匹配成功')
                time.sleep(0.2)
                continue
        if status == 1:
            return False
        else:
            return True

    @classmethod
    def click_element(self, element, validate_text: Optional[str] = None):
        # logger.info('元素执行点击操作')
        retry = 0
        while retry < 3:
            try:
                element.click()
                if validate_text:
                    res = self.check_text_by_pageSource(validate_text)
                    if not res:
                        raise Exception('点击未出现校验值,本次点击失败')
                break
            except BaseException as e:
                logger.error(e)
                retry += 1
                time.sleep(1)
        if retry >= 3:
            logger.error('三次点击均失败,用例失败')
            raise Exception('三次点击均失败,用例失败')

    @classmethod
    def element_send_keys(self, element, text, check: Optional[bool] = True):
        # logger.info('元素执行输入操作')
        retry = 0
        while retry < 3:
            try:
                element.clear()
                element.send_keys(text)
                if check:
                    value = element.get_attribute('value')
                    logger.info(value)
                    if value != text:
                        raise Exception('文本输入错误')
                else:
                    pass
                break
            except BaseException as e:
                logger.error(e)
                retry += 1
                time.sleep(1)
        if retry >= 3:
            logger.error('三次输入均失败,用例失败')
            raise Exception('三次输入均失败,用例失败')

    @staticmethod
    def scroll_page(type, pixel='', element=None):
        if type == 'top':
            js_line = "window.scrollTo(0, 0)"
        elif type == 'bottom':
            js_line = 'window.scroll(0, document.body.scrollHeight)'
        elif type == 'x':
            js_line = "window.scroll(%s, 0)" % pixel
        elif type == 'y':
            js_line = "window.scroll(0, %s)" % pixel
        # 滑动至元素可见
        elif type == 'toElement_down':
            js_line = "arguments[0].scrollIntoView();"
        elif type == 'toElement_up':
            js_line = "argument[0].scrollIntoView(false);"
        else:
            raise Exception(logger.error('未定义类型'))
        if element is None:
            driver.driver.driver1.execute_script(js_line)
        else:
            driver.driver.driver1.execute_script(js_line, element)

    @staticmethod
    def scroll_ele_inside(ele):
        try:
            time.sleep(1)
            action = ActionChains(driver.driver.driver1)
            action.scroll_to_element(ele)
            action.perform()
        except BaseException as e:
            logger.error(e)
            raise Exception('滑动出错')

    @staticmethod
    def get_element_text(element) -> str:
        text = element.get_attribute('innerText')
        logger.info(text)
        return str(text)

    @staticmethod
    def get_element_attribute(element, attribute) -> str:
        try:
            attribute_str = element.get_attribute(attribute)
            logger.info(attribute_str)
        except BaseException as e:
            logger.error(e)
            raise Exception('获取元素属性失败')
        return str(attribute_str)