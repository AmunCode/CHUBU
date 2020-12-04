from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time

# pull up login page
driver = webdriver.Chrome()
driver.get('https://dsm.commercehub.com/')
time.sleep(2)


def login():
    # enter username
    username = driver.find_element_by_id("username")
    username.clear()
    username.send_keys("Jegson")

    # enter user password
    password = driver.find_element_by_id("password")
    password.clear()
    password.send_keys("Miami2020$!@")

    driver.find_element_by_name("submit").click()
    time.sleep(4)

def update_tracking():
    external = driver.find_element_by_id("quicksearchCriteria")
    external.clear()
    external.send_keys("68994753")  # replace with variable
    external.submit()
    time.sleep(1)

    action = Select(driver.find_element_by_id("action"))
    action.select_by_visible_text('Ship')
    driver.find_element_by_class_name("chub-button").click()
    time.sleep(2)

    ##grab internal comm hub order number
    url = driver.current_url
    number = ''.join([letter for letter in url if letter.isdigit()])
    tracking = driver.find_element_by_name("order("+number+").box(1).trackingnumber")
    tracking.send_keys("1Z2V351V0323599220")    #variable replacement

    trackingSelection = Select(driver.find_element_by_id("order("+number+").box(1).shippingmethod"))
    trackingSelection.select_by_visible_text("UPS Ground")   #varialble replacement to do

    #find ship quantity field and enter 1, nothing else yet.
    readQuantity = driver.find_elements(By.CLASS_NAME, 'or_numericdata')
    qty = readQuantity[15].text

    inputs = driver.find_elements(By.TAG_NAME, 'input')
    print(len(inputs))
    ship_quantity = inputs[25]
    ship_quantity.send_keys(qty)
    ship_quantity.submit()

def update_invoice():
    external = driver.find_element_by_id("quicksearchCriteria")
    external.clear()
    external.send_keys("68994753")  # replace with variable
    external.submit()
    time.sleep(1)

    action = Select(driver.find_element_by_id("action"))
    action.select_by_visible_text('Invoice')
    driver.find_element_by_class_name("chub-button").click()
    url = driver.current_url
    number = ''.join([letter for letter in url if letter.isdigit()])
    time.sleep(2)
    inv_input = driver.find_element_by_name("order("+number+").invoicenumber")
    inv_input.send_keys('4499431')

    inputs = driver.find_elements(By.TAG_NAME, 'input')
    invoiceable = driver.find_elements(By.CLASS_NAME, 'or_numericdata')

    count = invoiceable[-2].text

    #read the quantity to be invoiced and put the value in the next field
    qty_field = inputs[-6]
    qty_field.send_keys(count)

    inv_input.submit()



#inputs.submit()