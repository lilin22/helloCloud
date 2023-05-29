import time
import allure,json,time
from string import Template
from typing import Optional
from  common.configLog import logger
from common.bases import bases
from configure.filepath import PAGE_DATA_PATH

class abilityCoor:
    def __init__(self):
        self.page_data = PAGE_DATA_PATH

    def check_text(self, data):
        text = data.get('text', '')
        timeout = data.get('timeout', 10)
        res = bases.check_text_by_pageSource(text, int(timeout))
        if not res:
            raise Exception(logger.error('未找到文本值,用例失败'))
    
    
    def check_text_disappear(self, data):
        text = data.get('text', '')
        timeout = data.get('timeout', 10)
        endtime = time.time()
        status = 0
        while time.time() < endtime + timeout:
            res = bases.check_text_disappear_by_pageSource(text, 2)
            if res:
                time.sleep(0.2)
                # raise logger.error('文本暂未消失,重新检查')
            else:
                status = 1
                break
        if status == 0:
            raise Exception('指定时间内,文本未消失')
    
    
    def use_element(self, data):
        element = data.get('element', '')
        page = data.get('page', '')
        action = data.get('action', '')
        element_data = bases.get_pageData(f'{self.page_data}\\{page}.yaml', element)
        # if element_data[0] == 'js':
        # 测试代码
        if element_data[0] == {}:
            bases.find_element_by_js(element_data[1])
        else:
            ele = bases.find_element(method=element_data[0], data=element_data[1])
            if action == 'click':
                ele = bases.find_element_clickable(method=element_data[0], data=element_data[1])
                # 点击元素
                if 'validate_text' in data.keys() and data.get('validate_text') != '':
                    validate_text = data.get('validate_text')
                    bases.click_element(element=ele, validate_text=validate_text)
                else:
                    bases.click_element(element=ele)
            elif action == 'send_keys':
                text = data.get('text')
                if 'validate_text' not in data.keys() or data.get('validate_text') == '':
                    bases.element_send_keys(element=ele, text=text, check=False)
                else:
                    bases.element_send_keys(element=ele, text=text)
            elif action == 'check_innerText':
                # 判断标签内的文本值是否符合传入值
                text = data.get('text', '')
                element_text = bases.get_element_text(element=ele)
                if text == element_text:
                    logger.info('标签文本校验成功')
                else:
                    logger.error('标签文本校验失败')
                    raise Exception('标签文本校验失败')
            elif action == 'check_attribute':
                # 判断元素属性值是否符合传入值
                attr = data.get('attr', '')
                attr_str = data.get('attr_str', '')
                element_attribute_str = bases.get_element_attribute(element=ele, attribute=attr)
                if attr_str == element_attribute_str:
                    logger.info('元素属性值符合预期')
                else:
                    logger.error('元素属性值不符合预取')
                    raise Exception('元素属性值不符合预取')
            else:
                logger.error('未定义参数')
                raise Exception('未定义参数')
    
    
    def check_cannot_find_element(self, data):
        element = data.get('element', '')
        page = data.get('page', '')
        timeout = data.get('timeout', 10)
        element_data = bases.get_pageData(self.page_data, element)
        endtime = time.time()
        status = 0
        while time.time() < endtime + timeout:
            try:
                bases.find_element(element_data[0], element_data[1], 2)
                time.sleep(0.2)
                # raise logger.error('元素暂未消失,重新检查')
            except:
                status = 1
                break
        if status == 0:
            raise Exception('指定时间内,元素未消失')
    
    
    def scrollPage(self, data):
        type = data.get('type')
        pixel = data.get('pixel', '')
    
        element = data.get('element', '')
        ele = None
        if element == '':
            pass
        else:
            page = data.get('page', '')
            element_data = bases.get_pageData(self.page_data, element)
            if element_data[0] == 'js':
                ele = bases.find_element_by_js(element_data[1])
            else:
                ele = bases.find_element(method=element_data[0], data=element_data[1])
    
        bases.scroll_page(type, pixel, ele)
    
    
    def scrollToElement(self, data):
        element = data.get('element', '')
        page = data.get('page', '')
        element_data = bases.get_pageData(self.page_data, element)
        if element_data[0] == 'js':
            ele = bases.find_element_by_js(element_data[1])
        else:
            ele = bases.find_element(method=element_data[0], data=element_data[1])
        bases.scroll_ele_inside(ele)

    @allure.step("{step}")
    def run(self, step,substep,mobile: Optional[str] = None,password: Optional[str] = None,message: Optional[str] = None):
        logger.info(f'步骤：{step}')
        for ss in substep:
            order = ss.get('order')
            function = ss.get('function')
            data = ss.get('data')
            function = getattr(self, function)
            if not data:
                data = dict()
            if 'text' in data.keys():
                if data['text'] == '$mobile':
                    data['text'] = mobile
                elif data['text'] == '$password':
                    data['text'] = password
                elif data['text'] == '$message':
                    data['text'] = message
            logger.info(f'元素：{order},data：{data}')
            function(data)