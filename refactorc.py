from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import selenium.webdriver.support.ui as ui

driver = webdriver.Firefox()
driver.get("https://twitter.com/")
inputElements = driver.find_elements_by_css_selector("input")
for inputElement in inputElements:
	if inputElement.get_attribute('type') == 'password':
		inputElement.send_keys(password)