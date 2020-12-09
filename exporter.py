from selenium import webdriver
from selenium.common.exceptions import *
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


def update_tracking_macys(order_num, tracking_num, service):
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
    elif service == 'HOME DELIVERY':
        tracking_selection.select_by_visible_text("FedEx Home Delivery")
    elif service == 'GROUND SERVICE':
        tracking_selection.select_by_visible_text("FedEx Ground")


    #find ship quantity field and enter 1, nothing else yet.
    read_quantity = driver.find_elements(By.CLASS_NAME, 'or_numericdata')
    qty = read_quantity[15].text

    inputs = driver.find_elements(By.TAG_NAME, 'input')
    ship_quantity = inputs[25]
    ship_quantity.send_keys(qty)
    ship_quantity.submit()


def update_tracking_bbb(order_num, tracking_num, service):
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
    elif service == 'HOME DELIVERY':
        tracking_selection.select_by_visible_text("FedEx Home Delivery")
    elif service == 'GROUND SERVICE':
        tracking_selection.select_by_visible_text("FedEx Ground")


    #find ship quantity field and enter 1, nothing else yet.
    read_quantity = driver.find_elements(By.CLASS_NAME, 'or_numericdata')
    qty = read_quantity[17].text
    print(qty)

    inputs = driver.find_elements(By.TAG_NAME, 'input')
    ship_quantity = inputs[30]
    ship_quantity.send_keys(qty)
    ship_quantity.submit()

def update_invoice_macys(order_num, invoice_num):
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

    submission_fields = driver.find_elements_by_class_name("chub-button")
    submission_fields[1].click()


def update_invoice_bbb(order_num, invoice_num):
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
    count = invoiceable[1].text

    # read the quantity to be invoiced and put the value in the next field
    qty_field = inputs[-4]
    qty_field.send_keys(count)

    submission_fields = driver.find_elements_by_class_name("chub-button")
    submission_fields[1].click()


def make_dropbox():
    path = os.getcwd()
    dropbox = "/dropbox"
    try:
        if not os.path.exists(path+dropbox):
            os.mkdir(path+dropbox)
    except OSError:
        print("Error: unable to create drop box folder")


orders = pd.read_excel('orders.xlsx', columns=['Order_Number', 'Tracking', 'Invoice', 'Carrier', 'Status'])
writer = pd.ExcelWriter('orders.xlsx', engine='xlsxwriter')
#print(df)

# current1 = df.loc[0,:]
# current2 = df.loc[1,:]
# current3 = df.loc[2,:]
#
# print(current1[0])
# print(current2[0])
# print(current3[0])

login()

error_array = []

for order in range(0, len(orders)):
    current_order = orders.loc[order, :]
    order_merchant = str(current_order[0])
    order_number = str(current_order[1])
    order_tracking = str(current_order[2])
    try:
        order_invoice = str(''.join([letter for letter in (current_order[3]) if letter.isdigit()]))
    except:
        order_invoice = str(current_order[3])
    order_carrier = str(current_order[4])

    if order_merchant == 'BEDBATH-DS':
        try:
            update_tracking_bbb(order_number, order_tracking, order_carrier)
        except (NoSuchElementException, ElementNotInteractableException):
            continue
        time.sleep(3)
    if order_merchant == 'BEDBATH-DS':
        try:
            update_invoice_bbb(order_number, order_invoice)
        except (NoSuchElementException, ElementNotInteractableException):
            continue
        time.sleep(3)

    elif order_merchant == 'MACYS001':
        try:
            update_tracking_macys(order_number, order_tracking, order_carrier)
        except (NoSuchElementException, ElementNotInteractableException):
            error_array.append(order_number)
            continue
        time.sleep(3)
        try:
            update_invoice_macys(order_number, order_invoice)
        except(NoSuchElementException, ElementNotInteractableException):
            error_array.append(order_number)
            continue
        time.sleep(3)
    else:
        print('ERROR: This merchant has not been set up for uploading.')

print(len(error_array))
with open("error file.txt", "w") as error_file:
    error_file.write("\n".join(list(error_array)))

