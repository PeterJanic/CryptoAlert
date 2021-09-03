import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys

# SYSTEM VARIABLES
# TODO: bolo by vhodne nejake premenne ukladat do suboru a nacitavat ich odtial
#  ak nahodou prerusim script ale ta i tak neviem no jedine ak ich ulozim pred zavretim alebo v aktualnom stave
#  alebo sa ulozi jeden cas a delta a ak current time bude mensi ako jeden cas + delta ta to zisti (ale to ma cas este)
delay = 4  # ze sa spusti kazde 10 min ale najprv daj par sekund
flag_if_run = False
server = "sk65"
# zatim dam na pevno lebo je to bugle, mozno ze by pomohlo to dat na zaciatok
login = "lenka6.v3@gmail.com"
secret_pass = "noschoolnow"
# set proper server, units_count and number of harvesting mode unlocked from that server
units_count = 8
harvesting_mode = 3
# user, pass, server...
driverino = None
numberOfSrc = 1
source = ["https://www.coingecko.com/en/coins/cardano/eur",
          "https://coinmarketcap.com/currencies/cardano/",
          "https://www.binance.com/en/trade/ada_Eur",
          "https://markets.businessinsider.com/currencies/ada-eur",
          "https://www.investing.com/crypto/cardano/ada-eur",
          "https://pro.coinbase.com/trade/ADA-EUR",
          "https://digitalcoinprice.com/coins/cardano/eur"]


# kvoli alternativam bude treba checkovat aj ci je to Eur or USD
def main_fun(my_driver, num_to_compare):
    my_driver.refresh()
    time.sleep(0.5)
    # better to use cuz it doesnt w8 for nothing if not needed a zaroven to plati pre vsetky dalsie hladania na drivery
    my_driver.implicitly_wait(2)
    # my_driver.quit()  # TODO: tu je ten breakpoint co treba odjebat - musi nasledovat clenenie
    # TODO: asi bude treba prirobit alternativy ak mi to kokot zablokuje a potom podla toho na akej alternative sme tak
    #  podla toho vyberat sposob get-u sumy
    # btw kava alebo mleko mi skodi

    # result = get_price_by_src_num(my_driver)

    input_el = my_driver.find_elements_by_class_name("priceValue")[0]

    print(float(input_el.text[1:5]))
    result = float(input_el.text[1:5])

    if result < num_to_compare:
        # pod ma alertnut
        print("volam cez facebook")
        call_on_facebook()


def get_to_harvest(driverino):
    global delay
    print("Waiting " + str(delay) + " seconds.")
    time.sleep(delay)
    if not flag_if_run:
        driver = webdriver.Firefox(executable_path=r"C:\geckodriver.exe")
        # TODO: este neviem jak ale tu to musi vyberat ine metody ak preodsle nesli aj bola vynimka
        #  a nasledne predat premennu ze ktora je vybrata a kazda metoda ma inak hladanie sumy nasledne [ALTERNATIVES]:
        # https://www.coingecko.com/en/coins/cardano/eur
        # ... aspon 10

        driver.get(source[numberOfSrc])
        driver.maximize_window()
    else:
        return driverino
    return driver


def call_on_facebook():
    time.sleep(1)

    profile = webdriver.FirefoxProfile()
    profile.set_preference('permissions.default.microphone', 1)
    # profile.set_preference('permissions.default.camera', 1)
    driver = webdriver.Firefox(firefox_profile=profile, executable_path=r'C:\geckodriver.exe')
    driver.get("https://www.facebook.com/")
    time.sleep(0.5)
    driver.maximize_window()
    time.sleep(1.5)
    driver.execute_script("document.getElementsByClassName('_9o-r')[0].children[1].click();")
    username = driver.find_element_by_name("email")
    username.send_keys(login)
    time.sleep(0.9)
    password = driver.find_element_by_name("pass")
    password.send_keys(secret_pass)
    time.sleep(1)
    password.submit()
    time.sleep(10)
    # tu sa nejako inak preklikat na ucet kt. chcem volat (toto bude treba testovat ci to funguje inac)
    # driver.get("https://www.facebook.com/peter.janic.9")
    driver.execute_script("document.getElementsByClassName('oajrlxb2')[11].click()")
    time.sleep(1)
    time.sleep(1)
    driver.execute_script("document.getElementsByClassName('oajrlxb2')[28].click()")
    time.sleep(1)
    driver.execute_script("document.getElementsByClassName('oajrlxb2')[49].click()")
    time.sleep(60)
    driver.quit()


def get_price_by_src_num(driver):
    if numberOfSrc == 0:    # https://www.coingecko.com/en/coins/cardano/eur
        return
    elif numberOfSrc == 1:  # https://coinmarketcap.com/currencies/cardano/
        return
    elif numberOfSrc == 2:  # https://www.binance.com/en/trade/ada_Eur
        return
    elif numberOfSrc == 3:  # https://markets.businessinsider.com/currencies/ada-eur
        return
    elif numberOfSrc == 4:  # https://www.investing.com/crypto/cardano/ada-eur
        return
    elif numberOfSrc == 5:  # https://pro.coinbase.com/trade/ADA-EUR
        return
    elif numberOfSrc == 6:  # https://digitalcoinprice.com/coins/cardano/eur
        return
    else:
        return "Something went wrong we dont have right Index!"

    return result


call_on_facebook()

while 1:
    try:
        driverino = get_to_harvest(driverino)
        flag_if_run = True
        main_fun(driverino, 2.99)
        # function_harvesting(my_driver, harvesting_mode, units_count)
    except:
        print(sys.exc_info()[0])
        # ak to zlyha moze rovno nastavit ten prepinac na Flase cize povodny stav a musi vyberat inu metodu getu na sumu
        # cize iny source
        flag_if_run = False
        numberOfSrc = numberOfSrc + 1
        if numberOfSrc >= len(source):
            numberOfSrc = 0
        driverino.quit()
        # inac teraz TO raz ide raz nejde lebo raz je true a vypne browser a potom nevie najst a da exception na false a
        # znova ide ale to sa zmeni len ja uz dalej nerobim zatial

