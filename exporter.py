from selenium import webdriver
import time

driver = webdriver.Chrome()
driver.get('https://dsm.commercehub.com/')

username = driver.find_element_by_id("username")
username.clear()
username.send_keys("Jegson")

password = driver.find_element_by_id("password")
password.clear()
password.send_keys("Miami2020$!@")

driver.find_element_by_name("submit").click()

time.sleep(10)


external = driver.find_element_by_name("quicksearchCriteria")
#external.clear()
#external.send_keys("0000001111")
print(external)