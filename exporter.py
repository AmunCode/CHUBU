from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pandas as pd
import time
import os

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
    time.sleep(6)


def update_tracking(order_num, tracking_num, service):
    external = driver.find_element_by_id("quicksearchCriteria")
    external.clear()
    external.send_keys(order_num)  # replaced with variable
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
    tracking.send_keys(tracking_num)                                                       #variable replacement

    tracking_selection = Select(driver.find_element_by_id("order("+number+").box(1).shippingmethod"))
    if service == 'GROUND':
        tracking_selection.select_by_visible_text("UPS Ground")                            #varialble replacement to do
    elif service == '2ND DAY AIR':
        tracking_selection.select_by_visible_text("UPS 2nd Day Air")
    elif service == 'NEXT DAY AIR':
        tracking_selection.select_by_visible_text("UPS Next Day Air")

    #find ship quantity field and enter 1, nothing else yet.
    read_quantity = driver.find_elements(By.CLASS_NAME, 'or_numericdata')
    qty = read_quantity[15].text

    inputs = driver.find_elements(By.TAG_NAME, 'input')
    ship_quantity = inputs[25]
    ship_quantity.send_keys(qty)
    ship_quantity.submit()

def update_invoice(order_num, invoice_num):
    external = driver.find_element_by_id("quicksearchCriteria")
    external.clear()
    external.send_keys(order_num)  # replaced with variable
    external.submit()
    time.sleep(1)

    action = Select(driver.find_element_by_id("action"))
    action.select_by_visible_text('Invoice')
    driver.find_element_by_class_name("chub-button").click()
    url = driver.current_url
    number = ''.join([letter for letter in url if letter.isdigit()])
    time.sleep(2)
    inv_input = driver.find_element_by_name("order("+number+").invoicenumber")
    inv_input.send_keys(invoice_num)

    inputs = driver.find_elements(By.TAG_NAME, 'input')
    invoiceable = driver.find_elements(By.CLASS_NAME, 'or_numericdata')

    count = invoiceable[-2].text

    #read the quantity to be invoiced and put the value in the next field
    qty_field = inputs[-6]
    qty_field.send_keys(count)

    outs = driver.find_elements_by_class_name("chub-button")
    outs[1].click()

def make_dropbox():
    path = os.getcwd()
    dropbox = "/dropbox"
    try:
        if not os.path.exists(path+dropbox):
            os.mkdir(path+dropbox)
    except OSError:
        print("Error: unable to create drop box folder")


orders = pd.read_excel('orders.xlsx', columns=['Order_Number', 'Tracking', 'Invoice', 'Carrier'])

#print(df)

# current1 = df.loc[0,:]
# current2 = df.loc[1,:]
# current3 = df.loc[2,:]
#
# print(current1[0])
# print(current2[0])
# print(current3[0])

login()


for order in range(0, len(orders)):
    current_order = orders.loc[order, :]
    order_number = str(current_order[0])
    order_tracking = str(current_order[1])
    order_invoice = str(''.join([letter for letter in (current_order[2]) if letter.isdigit()]))
    order_carrier = str(current_order[3])
    try:
        update_tracking(order_number, order_tracking, order_carrier)
    except EOFError:
        pass
    time.sleep(3)
    try:
        update_invoice(order_number, order_invoice)
    except EOFError:
        pass
    time.sleep(3)
