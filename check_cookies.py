from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from config import DRIVER_PATH
import pickle

url = "https://my.dnevnik76.ru"
headles = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.85 YaBrowser/21.11.3.927 Yowser/2.5 Safari/537.36"

service = Service(executable_path=DRIVER_PATH)

options = webdriver.ChromeOptions()
options.headless = False
options.add_argument(f"user-agent={headles}")
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(
        service=service,
        options=options)

try:
    driver.get(url)
    time.sleep(2)
    for cookie in pickle.load(open("cook", "rb")):
        driver.add_cookie(cookie)
    driver.refresh()
    time.sleep(10)
except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()
