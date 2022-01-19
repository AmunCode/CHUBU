from selenium.common.exceptions import *
import pandas as pd
import time
import chub

input_id = ""
input_password = ""

launch_driver = False

while input_id == "":
    input_id = input("enter login ID: ")
    input_password = input("enter password: ")
    if input_id != "" and input_password != "":
        launch_driver = True
        site = chub.launch_driver()
        chub.login(login_id=input_id, login_password=input_password, driver=site)

orders = pd.read_excel('orders.xlsx', columns=['Order_Number', 'Tracking', 'Invoice', 'Carrier', 'Status'])
writer = pd.ExcelWriter('orders.xlsx', engine='xlsxwriter')

while launch_driver:
    error_array = []
    for order in range(0, len(orders)):
        current_order = orders.loc[order, :]
        order_merchant = str(current_order[0])
        order_number = str(current_order[1])
        order_tracking = str(current_order[2])
        try:
            order_invoice = str(''.join([letter for letter in (current_order[3]) if letter.isdigit()])) # filter out non-numeric characters
        except:
            order_invoice = str(current_order[3])
        order_carrier = str(current_order[4])

        if order_merchant == 'BEDBATH-DS':
            try:
                chub.update_tracking_bbb(order_number, order_tracking, order_carrier, site)
            except (NoSuchElementException, ElementNotInteractableException):
                error_array.append(order_number)
                continue
            time.sleep(3)
        if order_merchant == 'BEDBATH-DS':
            try:
                chub.update_invoice_bbb(order_number, order_invoice, site)
            except (NoSuchElementException, ElementNotInteractableException):
                error_array.append(order_number)
                continue
            time.sleep(3)

        elif order_merchant == 'MACYS001':
            try:
                chub.update_tracking_macys(order_number, order_tracking, order_carrier, site)
            except (NoSuchElementException, ElementNotInteractableException):
                error_array.append(order_number)
                continue
            time.sleep(3)
            try:
                chub.update_invoice_macys(order_number, order_invoice, site)
            except(NoSuchElementException, ElementNotInteractableException):
                error_array.append(order_number)
                continue
            time.sleep(3)
        elif order_merchant == 'STAPLESADV' or 'QUILL':
            try:
                chub.update_tracking_staples(order_number, order_tracking, order_invoice, order_carrier, site)
            except (NoSuchElementException, ElementNotInteractableException, TypeError):
                error_array.append(order_number)
                continue
            time.sleep(3)
        else:
            print('ERROR: This merchant has not been set up for uploading.')

    with open("error file.txt", "w") as error_file:
        error_file.write("\n".join(list(error_array)))

    launch_driver = False
site.close()

