from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
driver = webdriver.Chrome()
driver.get('https://dsm.commercehub.com/')
time.sleep(2)
username = driver.find_element_by_id("username")
username.clear()
username.send_keys("Jegson")
password = driver.find_element_by_id("password")
password.clear()
password.send_keys("Miami2020$!@")
driver.find_element_by_name("submit").click()
time.sleep(4)
external = driver.find_element_by_id("quicksearchCriteria")
external.clear()
external.send_keys("68994753")
external.submit()
time.sleep(1)
# action = Select(driver.find_element_by_id("action"))
# # action.select_by_visible_text('Ship')
# #
# # driver.find_element_by_class_name("chub-button").click()
# #
# # time.sleep(2)
# #
# # ##grab internal comm hub order number
# # url = driver.current_url
# # number = ''.join([letter for letter in url if letter.isdigit()])
# #
# # tracking = driver.find_element_by_name("order("+number+").box(1).trackingnumber")
# # tracking.send_keys("1Z2V351V0323599220")    #variable replacement
# #
# # trackingSelection = Select(driver.find_element_by_id("order("+number+").box(1).shippingmethod"))
# # trackingSelection.select_by_visible_text("UPS Ground")   #varialble replacement to do
# #
# # #find ship quantity field and enter 1, nothing else yet.
# # readQuantity = driver.find_elements(By.CLASS_NAME, 'or_numericdata')
# # qty = readQuantity[15].text
# #
# # inputs = driver.find_elements(By.TAG_NAME, 'input')
# # print(len(inputs))
# # shipQuantity = inputs[25]
# # shipQuantity.send_keys(qty)
# #
# # shipQuantity.submit()
action = Select(driver.find_element_by_id("action"))
action.select_by_visible_text('Invoice')
driver.find_element_by_class_name("chub-button").click()
url = driver.current_url
number = ''.join([letter for letter in url if letter.isdigit()])
time.sleep(2)
inputs = driver.find_element_by_name("order("+number+").invoicenumber")
#invoice = inputs[22]
#print(len(inputs))
#invoice.send_keys('Testeting')
inputs.send_keys('4499431')

inputs = driver.find_elements(By.TAG_NAME, 'input')
print(len(inputs))

invoiceable = driver.find_elements(By.CLASS_NAME, 'or_numericdata')

count = invoiceable[-2].text
qty = inputs[-6]
qty.send_keys(count)

#inputs.submit()