# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name:         SignIn_to_lenovo
# Description:  
# Author:       skymoon9406@gmail.com
# Date:         2019/9/14
# -------------------------------------------------------------------------------

import selenium
import selenium.webdriver
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from loggers import Logger
log = Logger('info.log', level='info')
# 生成一个谷歌浏览器的Driver(同理也可以生产一个火狐浏览器的Driver)
# diver = selenium.webdriver.Firefox()
# driver = selenium.webdriver.Chrome()
# 生成一个无界面浏览器
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
driver = selenium.webdriver.Chrome(options=chrome_options)

# 利用get方式访问一个页面(必须写完整，如果只写成"www.baidu.com"则无法达到效果)
driver.get("https://club.lenovo.com.cn/signlist/")

# 隐式等待和显式等待
# 显式等待中presence_of_element_located的参数需要是元组形式
WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "login")))
# 模拟点击页面某个按钮
driver.find_element_by_class_name("login").click()

# 等待直到登录页面出现
WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "ppWrapper")))
account = driver.find_element_by_xpath('//div[@id="normal_login_box"]/div[@class="login_input login_inputa"]/input')
password = driver.find_element_by_xpath('//div[@id="normal_login_box"]/div[@class="login_input login_inputb"]/input')
submit = driver.find_element_by_class_name("submit")
account.send_keys("")
password.send_keys("")
submit.click()
time.sleep(5)
# 获取当前状态
sign_in_text = driver.find_element_by_class_name("signInTimeMiddleBtn").text
# 获取已有的延保券和积分
coupon = driver.find_element_by_id("warranty_sore").text
coins = driver.find_element_by_id("coins").text
sign_in_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
if sign_in_text == "已签到":
    log.logger.info(sign_in_time + "已经在其他平台签到\n当前延保券为： " + coupon + "\n当前积分为: " + coins)
else:
    # 点击签到
    sign_in_button = driver.find_element_by_class_name("signInTimeMiddleBtn")
    sign_in_button.click()
    log.logger.info(sign_in_time + "已经签到,\n当前延保券为： " + coupon + "\n当前积分为: " + coins)
log.logger.info("*****************************************************")
# 关闭这个驱动器
driver.close()

