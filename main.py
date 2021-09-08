import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
from datetime import datetime
from datetime import date

# SYSTEM VARIABLES
delay = 1  # repeat timer
flag_if_run = False
login = "lenka6.v3@gmail.com"
secret_pass = "noschoolnow"
driverino = None
numberOfSrc = 1
source = ["https://www.coingecko.com/en/coins/cardano/eur",
          "https://www.investing.com/crypto/cardano/ada-eur",
          "https://digitalcoinprice.com/coins/cardano/eur",
          "https://ratesviewer.com/chart/ada-eur/year/",
          "https://www.marketwatch.com/investing/cryptocurrency/adaeur"]


def main_fun(my_driver, num_to_compare):
    my_driver.refresh()
    time.sleep(0.5)
    # better to use because it doesnt wait and works for every other waiting
    my_driver.implicitly_wait(2)

    result = get_price_by_src_num(my_driver)
    print(result, " ", datetime.now())
    if result < num_to_compare:
        print("call via Facebook: ", datetime.now())
        try:
            time.sleep(1)
            profile = webdriver.FirefoxProfile()
            profile.set_preference('permissions.default.microphone', 1)
            profile.set_preference('permissions.default.camera', 1)
            driver_fb = webdriver.Firefox(firefox_profile=profile, executable_path=r'C:\geckodriver.exe')
            call_on_facebook(driver_fb)
        except:
            print("SOMETHING WENT WRONG! ", datetime.now())
            driver_fb.quit()


def get_to_harvest(driverino):
    global delay
    print("Waiting " + str(delay) + " seconds.")
    time.sleep(delay)
    if not flag_if_run:
        driver = webdriver.Firefox(executable_path=r"C:\geckodriver.exe")
        driver.get(source[numberOfSrc])
        driver.maximize_window()
    else:
        return driverino
    return driver


def call_on_facebook(driver_fb):
    driver_fb.get("https://www.facebook.com/")
    time.sleep(0.5)
    driver_fb.maximize_window()
    time.sleep(1.5)
    driver_fb.execute_script("document.getElementsByClassName('_9o-r')[0].children[1].click();")
    username = driver_fb.find_element_by_name("email")
    username.send_keys(login)
    time.sleep(0.9)
    password = driver_fb.find_element_by_name("pass")
    password.send_keys(secret_pass)
    time.sleep(1)
    password.submit()
    time.sleep(6)
    # test this a lot ...next line will need refactor as well later
    driver_fb.execute_script("document.getElementsByClassName('oajrlxb2')[11].click()")
    time.sleep(1)
    ts = driver_fb.find_elements_by_css_selector("[data-testid=mwthreadlist-item]")[0]
    ts.click()  # yes! I'm there
    time.sleep(1)
    driver_fb.execute_script("document.getElementsByName('actions')[0].children[1].children[0].click()")
    time.sleep(30)
    driver_fb.quit()


def get_price_by_src_num(driver):
    driver.implicitly_wait(2)
    if numberOfSrc == 0:    # https://www.coingecko.com/en/coins/cardano/eur
        input_el = driver.find_elements_by_class_name("no-wrap")[0].text
        result = float(input_el[1:5])
    elif numberOfSrc == 1:  # https://www.investing.com/crypto/cardano/ada-eur
        input_el = driver.find_element_by_id("last_last").text
        result = float(input_el[0:4])
    elif numberOfSrc == 2:  # https://digitalcoinprice.com/coins/cardano/eur
        input_el = driver.find_element_by_id("quote_price").text
        result = float(input_el[1:5])
    elif numberOfSrc == 3:  # https://ratesviewer.com/chart/ada-eur/year/
        input_el = driver.find_elements_by_class_name("value")[0].text
        result = float(input_el[4:8])
    elif numberOfSrc == 4:  # https://www.marketwatch.com/investing/cryptocurrency/adaeur
        input_el = driver.find_elements_by_class_name("value")[6].text
        result = float(input_el[0:4])
    else:
        return "Something went wrong we dont have right Index!"

    return result


while 1:
    try:
        driverino = get_to_harvest(driverino)
        flag_if_run = True
        main_fun(driverino, 2.20)
    except:
        print(sys.exc_info()[0])
        # If failed set flag_if_run to False again and pick another method by incrementing counter
        # so here will set another source
        flag_if_run = False
        numberOfSrc = numberOfSrc + 1
        if numberOfSrc >= len(source):
            numberOfSrc = 0
        driverino.quit()
