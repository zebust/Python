from selenium import webdriver

import time

browser = webdriver.Firefox()
browser.get('http://gmail.com')

elm_user = browser.find_element_by_id('Email')
elm_user.send_keys('salman.khan@gmail.com')

browser.find_element_by_name('signIn').click()

time.sleep(1)
elm_pass = browser.find_element_by_id('Passwd')
elm_pass.send_keys('12345')

elm_pass.submit()



