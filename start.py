from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import time
import yaml

from functions.getProxy import *
from functions.getUserAgent import *

#proxy = getProxy()

with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

activity =  config['activity']
speedometer = config['speedometer']
email = config['email']
password = config['password']

#prox_options = {
#    'proxy': {
#        'http': proxy
#    }
#}

def check_rate_limit():
    # check if rate limit alert
    try:
        if driver.find_element(By.CLASS_NAME, 'el-message__content'):
            print('Rate limit alert')
            minutes_cooldown = int(re.sub("\D", "", driver.find_element(By.CLASS_NAME, 'el-message__content').text)) # idk if it's always 1 minute so we just get the number from the error text
            print('Waiting ' + str(minutes_cooldown) + ' minutes')
            time.sleep(minutes_cooldown * 60)
            print('Continuing')
    except Exception as e:
        pass

if speedometer == 'fast':
    time_sleep = 1
    web_driver_wait = 5
    driver_wait = 2
elif speedometer == 'medium':
    time_sleep = 5
    web_driver_wait = 10
    driver_wait = 5
elif speedometer == 'slow':
    time_sleep = 10
    web_driver_wait = 15
    driver_wait = 10

options = Options()
#options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--user-agent=' + GET_UA())
options.add_argument('--incognito')
options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
chrome_drvier_binary = '/opt/homebrew/bin/chromedriver'
driver = webdriver.Chrome(service=Service(chrome_drvier_binary), options=options)

url = 'https://anilist.co/login'

driver.get(url)

try:
    try:
        cookie_agree_btn = driver.find_element(By.CLASS_NAME, 'css-1litn2c')
        driver.implicitly_wait(driver_wait)
        ActionChains(driver).move_to_element(cookie_agree_btn).click(cookie_agree_btn).perform()
    except Exception as e:
        pass

    # if the email variable is defined fill it up
    if email != '':
        email_input = driver.find_element(By.XPATH, '//*[@id="app"]/div[3]/div/div/form/input[1]')
        ActionChains(driver).move_to_element(email_input).click(email_input).send_keys(email).perform()
    
    # if the password variable is defined fill it up
    if password != '':
        password_input = driver.find_element(By.XPATH, '//*[@id="app"]/div[3]/div/div/form/input[2]')
        ActionChains(driver).move_to_element(password_input).click(password_input).send_keys(password).perform()

    # wait till the user has filled up the credentials and made the google recaptcha
    input('Press enter after you have filled up the credentials and made the google recaptcha')

    # click on login
    driver.find_element(By.XPATH, '//*[@id="app"]/div[3]/div/div/form/div[2]').click()

    try:
        time.sleep(10) # need to wait till the dashboard loads
        if activity == 'following':
            tab_btn = driver.find_element(By.XPATH, '/html/body/div[2]/div[3]/div/div/div[1]/h2/div/div[2]/div[1]')
        elif activity == 'global':
            tab_btn = driver.find_element(By.XPATH, '/html/body/div[2]/div[3]/div/div/div[1]/h2/div/div[2]/div[2]')

        WebDriverWait(driver, web_driver_wait).until(EC.element_to_be_clickable(tab_btn))
        tab_btn.click()
    except Exception as e:
        print(e)
        pass # default behavior you're already on the 'following' tab

    start_index = 0

    while True:
        check_rate_limit()
        activity_entries = driver.find_elements(By.CLASS_NAME, 'activity-entry')

        for i in range(start_index, len(activity_entries)):
            entry = activity_entries[i]
            print('Liking activity entry ' + str(i+1))
            try:
                like_btn = entry.find_element(By.XPATH, './/div[@class="like-wrap activity"]/div[@class="button"]')
                WebDriverWait(driver, web_driver_wait).until(EC.element_to_be_clickable(like_btn))
                like_classes = like_btn.get_attribute('class')
                if 'liked' in like_classes: # if already liked skip it
                    print('Skipping activity entry ' + str(i+1) + ' because it is already liked')
                    continue
                like_btn.click()
                check_rate_limit()
                time.sleep(time_sleep)
            except Exception as e:
                print('Skipping activity entry ' + str(i+1) + ' because of some random error (mostly because it is already liked)')
                continue

        start_index = len(activity_entries)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        try:
            if driver.find_element(By.CLASS_NAME, 'load-more'):
                load_more_btn = driver.find_element(By.CLASS_NAME, 'load-more')
                load_more_btn.click()
        except Exception as e:
            pass

        time.sleep(time_sleep)

except Exception as e:
    print(e)
    driver.quit()
    exit()