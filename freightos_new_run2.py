# Importing necessary Libraries
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import sys
import pandas as pd
import selenium.webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.options import Options
from proxy_list import *
from selenium.webdriver import FirefoxOptions, Firefox
from driver_selenium import *
import time
import random
import datetime
from creds import *
import mysql.connector
from database_connect import *
import logging
import os
os.chdir('/root/Desktop/scrapping_full/cron')
sys.path.insert(0, '/root/Desktop/scrapping_full/cron')

# to avoid selenium loggings
os.environ["WDM_LOG_LEVEL"] = str(logging.ERROR)

logging.getLogger("selenium").setLevel(logging.ERROR)
date = datetime.datetime.now().strftime(
    "%Y-%m-%d %H:%M:%S")  # -datetime.timedelta(days=6))
# now we will Create and configure logger
logging.basicConfig(
    filename=f"logs/Freightos_indices_{date}.log", format='%(asctime)s %(message)s', filemode='w')

# Let us Create an object
logger = logging.getLogger()

# Now we are going to Set the threshold of logger to WARNING
logger.setLevel(logging.ERROR)

# to get the print statement in the log
print = logging.error

# Browser
start_time = time.time()

# Database login

def master_db_login():
    connection = mysql.connector.connect(host=IP,
                                         database='brand_master',
                                         user='root',
                                         password=DB_PASS,
                                         port=3306, auth_plugin='caching_sha2_password')
    cursor = connection.cursor()
    return connection, cursor

# Login into the account

def login_new(driver):
    driver.find_element(By.XPATH, '//div[@class="login"]/a[1]').click()
#     driver.find_element(By.XPATH, '//a[@class = "sign__in"]').click()
    time.sleep(8)
    driver.find_element(
        By.XPATH, '//input[@name="email"]').send_keys('trendseedev@gmail.com')
    time.sleep(8)
    driver.find_element(
        By.XPATH, '//input[@name="password"]').send_keys('!3G6Twb!kytTTHy')
    time.sleep(8)
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()
    time.sleep(8)

# Logout from account


def logout():
    el1 = driver.find_element(By.XPATH, '//p[@class="sc-hBxehG dFvCcw"]')
    el1.click()
    logout_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, '//div[@class="sc-bcXHqe sc-gswNZR sc-jrcTuL jmoReX fpjZuY fwzrCP"]'))
    )

    # Click on the logout button
    logout_button.click()

# FB logout function
def logout2(driver):
    # Find the elements
    profile_menu = driver.find_element(
        By.XPATH, '//p[@class="sc-hBxehG dFvCcw"]')
    logout_button = driver.find_element(
        By.XPATH, '//div[@class="sc-bcXHqe sc-gswNZR sc-jrcTuL jmoReX fpjZuY fwzrCP"]')

    # Create an ActionChains object
    actions = ActionChains(driver)

    # Move to the profile menu to make it visible (optional)
    actions.move_to_element(profile_menu)

    # Click on the logout button
    actions.click(logout_button)

    # Perform the actions
    actions.perform()

def savedata_freightos(connection, cursor, Item, Price_in_USD, timestamp):
    """ This function inserts the argument datas in to the freightos data table"""

    try:

        sqlite_insert_with_param = """INSERT INTO freightos_data
                              (Item, Price_in_USD, updated_time)
                              VALUES (%s,%s,%s);"""
        data_tuple = (Item, Price_in_USD, timestamp)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        connection.commit()
        print(data_tuple)
        print('Saved')
    except Exception as e:
        print(e)


# main function
def freightos_running():
    try:
        connection, cursor = master_db_login()

        driver = getdriver_proxyless()
        time.sleep(10)
        print('driver opened')
        print(driver)
        driver.get('https://fbx.freightos.com/freight-index/FBX')
        time.sleep(10)
        print(driver.current_url)
        print('site opened')
        login_new(driver)
        print('Login is sucessfull')
        time.sleep(10)
        scroll_script = "window.scrollTo(10, document.body.scrollHeight);"
        driver.execute_script(scroll_script)
        time.sleep(10)
        key_element1 = [element.text for element in driver.find_elements(
            By.XPATH, '//div[@class="sc-bcXHqe sc-gswNZR lhWDT bRxjQa"]/span')]
        print(f'key_element1 is : {key_element1}')
        key_element2 = [element.text for element in driver.find_elements(
            By.XPATH, '//div[@class="sc-bcXHqe sc-gswNZR lhWDT bRxjQa"]/p')]
        print(f'key_element2 is  : {key_element2}')
        value_element = [element.text for element in driver.find_elements(
            By.XPATH, '//div[@class="sc-bcXHqe sc-gswNZR lbsYfa kUnye"]/p[1]')]
        print(f'value element is :  {value_element}')

        keys = []  # Index regions
        for a, b in zip(key_element1, key_element2):
            keys.append(a + '-' + b)
        print(keys)

        for key, val in zip(keys, value_element):
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # print(key,val,timestamp)
            savedata_freightos(connection, cursor, key, val, timestamp)
        print('data uploaded to table at:' +
              datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        print('completed')

        try:
            logout()
        except:
            logout2(driver)
        print('logout')
    except Exception as e:
        print(e)


freightos_running()

feed_time = time.time()
logger.error(f"new brands saving end, time taken {start_time-feed_time}")
