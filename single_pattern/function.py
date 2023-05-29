import os
from single_pattern import exestatus
from common import logger
import time
from startserver import server



def update_startNoxexe_status(nox_name):
    cmdmsg = os.popen('netstat -ano').read()
    cmdlist = server.cmd_res_to_list(cmdmsg)
    for value in cmdlist:
        if nox_name in value and 'LISTENING' in value:
            exestatus.exestatus.exestatusdict[nox_name] = 'true'
            break
        else:
            exestatus.exestatus.exestatusdict[nox_name] = 'false'
            continue



def update_startappium_status(port):
    if port in os.popen('netstat -ano').read():
        exestatus.exestatus.exestatusdict['appium'] = 'true'
    elif port not in os.popen('netstat -ano').read():
        exestatus.exestatus.exestatusdict['appium'] = 'false'


def check_serverstatus(servernumber, appium_port, noxname):
    endtime = time.time()
    status = 0
    while time.time() <= endtime + 10:
        update_startNoxexe_status(noxname)
        update_startappium_status(appium_port)
        if servernumber == len(list(exestatus.exestatus.exestatusdict.values())):
            for value in list(exestatus.exestatus.exestatusdict.values()):
                if value != 'true':
                    status = 1
            if status == 0:
                logger.info('服务运行正常，服务状态%s' % exestatus.exestatus.exestatusdict)
                break
            elif status == 1:
                time.sleep(1)
                continue
        else:
            status = 1
            time.sleep(1)
            continue
    if status == 1:
        raise Exception(logger.error('服务运行失败，服务状态%s' % exestatus.exestatus.exestatusdict))
