import os,sys,allure,pytest,traceback
from common.configLog import logger
from common.case_api import case_api
from invoke.abilityCoor import abilityCoor

class Test_cases:

    @pytest.mark.parametrize('case_id,story,title,info',case_api.getCasesData(os.path.dirname(__file__)))
    def test_cases(self, userReady, case_id, story, title, info):
        try:
            logger.info(f"执行用例：{title}")
            allure.dynamic.story(story)
            allure.dynamic.title(f'{case_id}---{title}')
            mobile, password, message = userReady
            ability_coor = abilityCoor()
            for sp in info:
                step = sp.get('step')
                substep = sp.get('substep')
                ability_coor.run(step,substep,mobile,password,message)
        except Exception:
            raise Exception(logger.error(traceback.format_exc()))