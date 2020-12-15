from selenium.common.exceptions import *
import pandas as pd
import time
import chub


orders = pd.read_excel('orders.xlsx', columns=['Order_Number', 'Tracking', 'Invoice', 'Carrier', 'Status'])
writer = pd.ExcelWriter('orders.xlsx', engine='xlsxwriter')

chub.login()

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
            chub.update_tracking_bbb(order_number, order_tracking, order_carrier)
        except (NoSuchElementException, ElementNotInteractableException):
            error_array.append(order_number)
            continue
        time.sleep(3)
    if order_merchant == 'BEDBATH-DS':
        try:
            chub.update_invoice_bbb(order_number, order_invoice)
        except (NoSuchElementException, ElementNotInteractableException):
            error_array.append(order_number)
            continue
        time.sleep(3)

    elif order_merchant == 'MACYS001':
        try:
            chub.update_tracking_macys(order_number, order_tracking, order_carrier)
        except (NoSuchElementException, ElementNotInteractableException):
            error_array.append(order_number)
            continue
        time.sleep(3)
        try:
            chub.update_invoice_macys(order_number, order_invoice)
        except(NoSuchElementException, ElementNotInteractableException):
            error_array.append(order_number)
            continue
        time.sleep(3)
    else:
        print('ERROR: This merchant has not been set up for uploading.')


with open("error file.txt", "w") as error_file:
    error_file.write("\n".join(list(error_array)))

