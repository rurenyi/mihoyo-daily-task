# python -m pip install maafw
import subprocess
import datetime
import signal
import time
import os

from maa.resource import Resource
from maa.controller import AdbController
from maa.tasker import Tasker
from maa.toolkit import Toolkit

import logging
logging.basicConfig(level=logging.INFO,filename='log',filemode='a',format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',encoding='utf-8')

mu_mu_player_path = r"D:\\mumu\\MuMu Player 12\\shell\\MuMuPlayer.exe"
launch_waiting_time = 30

def launch_task():
    user_path = "./"
    Toolkit.init_option(user_path)

    resource = Resource()
    res_job = resource.post_path("resource/genshin")
    res_job.wait()

    adb_devices = Toolkit.find_adb_devices()
    if not adb_devices:
        logging.error("No ADB device found.")
        return False

    device = adb_devices[0]
    controller = AdbController(
        adb_path=device.adb_path,
        address=device.address,
        screencap_methods=device.screencap_methods,
        input_methods=device.input_methods,
        config=device.config,
    )
    controller.post_connection().wait()

    tasker = Tasker()

    tasker.bind(resource, controller)

    if not tasker.inited:
        logging.error("Failed to init MAA.")
        return False

    task_detail = tasker.post_pipeline("启动原神").wait()
    return task_detail.done()

def main():
    logging.info(f'正在启动mumu模拟器，等待{launch_waiting_time}s')
    process = subprocess.Popen(mu_mu_player_path)
    time.sleep(launch_waiting_time)
    if process.poll() is None:
        logging.info("MuMu Player 启动成功!")
    else:
        logging.error("MuMu Player 启动失败!")

    logging.info("即将执行任务......")

    result = launch_task()
    
    if result:
        logging.info("执行任务成功......")
    else:
        logging.error("执行任务失败")

    if os.path.exists("./debug/vision"):
        os.rename("./debug/vision","./debug/genshin_"+str(datetime.date.today()))

    os.kill(process.pid, signal.SIGTERM)  
    process.wait()

if __name__ == "__main__":
    main()