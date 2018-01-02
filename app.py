from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time,sys,pickle

ec=0
chrome_options = Options()  
chrome_options.binary_location = r"/app/.apt/usr/bin/google-chrome"

print("App STARTED! KIRSH!")
print ("\n>> Opening Browser")

# driver = webdriver.Chrome(executable_path="chromedriver.exe", chrome_options=chrome_options)
driver = webdriver.Chrome(chrome_options=chrome_options)

while True:
    try:

        driver.get("https://exfaucet.com/")

        cookies = pickle.load(open("cookies.pkl", "rb"))
        for cookie in cookies:
            driver.add_cookie(cookie)

        total = 0
        while True:
            fauc = driver.find_element_by_xpath('//*[@id="site-navigation"]/div/ul/li[1]/a')
            fauc.click()

            try:
                driver.find_element_by_xpath('//*[@id="sticky_bar_logo"]/div[2]/button').click()
            except Exception as err:
                print("err " + str(err))

            driver.switch_to_frame(driver.find_element_by_xpath('//*[@id="post-6"]/div/div/strong/form/div[1]/div/iframe'))
            captcha = driver.find_element_by_class_name('verify-me-progress')
            captcha.click()
            tt=0
            while True:

                bar = driver.find_element_by_xpath('//*[@id="verify-me-progress"]')
                style = bar.get_attribute("style")
                style = style.replace("width: ","")[:3]
                style = style.replace(";","")
                if "100" in style:
                    print("\n>> Captcha Verified in " + str(tt) + " seconds. Claiming...")
                    driver.switch_to_default_content()
                    break
                time.sleep(1)
                tt+=1
                if tt >= 1000:
                    print("\n>> Taking tooo much time! Retrying...")
                    crash_program
            
            add=driver.find_element_by_xpath('//*[@id="post-6"]/div/div[2]/strong/form/div[1]/div/iframe')
            add.send_keys(Keys.TAB + Keys.TAB + " ")
            
            amnt = driver.find_element_by_xpath('//*[@id="post-6"]/div/div[2]/strong/form/div[1]')
            amnt = amnt.get_attribute("textContent")

            print(amnt)

            time.sleep(1)
    except Exception as err:
        print(">> ERROR : " + str(err))
        ec += 1
        if ec == 10:
            crash_program
        continue
