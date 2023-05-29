import sys,os,re,pytest,allure
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from common.configLog import logger
from single_pattern import driver
from configure.filepath import BROWSER_DRIVER_PATH
from configure.setting import user_uri
from common.bases import bases

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    '''
    获取每个用例状态的钩子函数
    :param item:
    :param call:
    :return:
    '''
    # 获取钩子方法的调用结果
    outcome = yield
    rep = outcome.get_result()
    # 仅仅获取用例call 执行结果是失败的情况, 不包含 setup/teardown
    if rep.when == "call" and rep.failed:
        # 添加allure报告截图
        if hasattr(driver.driver.driver1, "get_screenshot_as_png"):
            with allure.step('用例失败截图'):
                allure.attach(driver.driver.driver1.get_screenshot_as_png(), "失败截图", allure.attachment_type.PNG)
    if rep.when == "setup" and rep.failed:
        # 添加allure报告截图
        if hasattr(driver.driver.driver1, "get_screenshot_as_png"):
            with allure.step('前置失败截图'):
                allure.attach(driver.driver.driver1.get_screenshot_as_png(), "失败截图", allure.attachment_type.PNG)
    if rep.when == "teardown" and rep.failed:
        # 添加allure报告截图
        if hasattr(driver.driver.driver1, "get_screenshot_as_png"):
            with allure.step('后置失败截图'):
                allure.attach(driver.driver.driver1.get_screenshot_as_png(), "失败截图", allure.attachment_type.PNG)

def pytest_addoption(parser):
    parser.addoption(
        "--mobile", action="store", default="18965125035", help="my option: type1 or type2"
    )
    parser.addoption(
        "--password", action="store", default="qa123456!", help="my option: type1 or type2"
    )
    parser.addoption(
        "--nickname", action="store", default="test", help="my option: type1 or type2"
    )
    parser.addoption(
        "--message", action="store", default="520634", help="my option: type1 or type2"
    )

@pytest.fixture(scope="session")
def mobile(request):
    return request.config.getoption("--mobile")

@pytest.fixture(scope="session")
def password(request):
    return request.config.getoption("--password")

@pytest.fixture(scope="session")
def message(request):
    return request.config.getoption("--message")

def pytest_collection_modifyitems(items):
    """
    测试用例收集完成时，将收集到的item的name和nodeid的中文显示在控制台上
    :param items:
    :return:
    """
    for item in items:
        try:
            re_case_name = re.findall(r"(\[.*\])", item._nodeid)
            if re_case_name:
                case_name = re_case_name[0]
                item._nodeid = item._nodeid.replace(case_name, case_name.encode("utf-8").decode("unicode-escape"))
        except Exception as e:
            logger.error(e)


@pytest.fixture(scope='session',autouse=True)
def userReady(mobile,password,message):
    logger.info(f"测试用户：{mobile},密码：{password},验证码：{message}")
    bases.start_browser(BROWSER_DRIVER_PATH,user_uri)
    yield mobile, password, message