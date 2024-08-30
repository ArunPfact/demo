# Importin g necessary libraries
from selenium.webdriver import FirefoxOptions, Firefox
import pickle
import pandas as pd
from bs4 import BeautifulSoup
import time
import requests
import datetime
import re
import datetime
from tqdm import tqdm
import undetected_chromedriver as uc
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selectorlib import Extractor
from selenium.webdriver import Chrome, ChromeOptions, DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
# scrapping list of categories and sub categories
import time
import urllib
import json
import random
from lxml.html import fromstring
import requests
from itertools import cycle
import traceback
# random user-agent
from selenium.common.exceptions import NoSuchElementException
import os
import numpy as np
# from database_connect import *
# from proxy_list import *
import numpy as np
from socket import timeout
import sys
import json
from urllib.parse import urljoin
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.support import expected_conditions as EC
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
from selenium.webdriver.common.by import By
import csv
import socket
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from fake_useragent import UserAgent
s = socket.socket()
s.settimeout(300)
# from proxy_list import *
# proxies = scoial_blade_proxies


def get_useragent():
    user_agent_list = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    ]
    useragent = user_agent_list[random.randint(0, 3)]
    return useragent


def getdriver_proxyless():  # proxy
    options = FirefoxOptions()
#     options.add_argument('--proxy-server={proxy}'.format(proxy=proxy))
    options.add_argument('log-level=3')
    options.add_argument("--window-size=1880x1020")
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument('--disable-dev-shm-usage')
    prefs = {"profile.default_content_setting_values.notifications": 2,
             "webrtc.ip_handling_policy": "disable_non_proxied_udp",
             "webrtc.multiple_routes_enabled": False,
             "webrtc.nonproxied_udp_enabled": False,
             "profile.default_content_setting_values.geolocation": 2}
    driver = Firefox(options=options)  # , capabilities=firefox_capabilities
    return driver
