from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import os


# pull up login page
def launch_driver():
    driver = webdriver.Chrome()
    driver.get('https://dsm.commercehub.com/')
    return driver


def login(login_id: str, login_password: str, driver: object):
    """
    Login with username and password.

    Parameters:
        login_id: string with the username
        login_password: string with the password
        driver: the instance of chrome drive to be used

    """
    time.sleep(2)
    username = driver.find_element_by_id("username")
    username.clear()
    username.send_keys(login_id)
    driver.find_element_by_name("action").click()
    time.sleep(2)

    # enter user password
    password = driver.find_element_by_id("password")
    password.clear()
    password.send_keys(login_password)
    driver.find_element_by_name("action").click()
    time.sleep(6)


def update_tracking_macys(order_num: str, tracking_num: str, service: str, driver: object):
    """updates the Macy's orders

    The tracking number, carrier service type are updated to a Macy's orders.

    Parameters:
        order_num: string with the order number
        tracking_num: string with the tracking number for the package
        service: string with the type of shipping service used
        driver: instance of chrome driver to be used

    Return:
        No return generated

    """
    external = driver.find_element_by_id("quicksearchCriteria")
    external.clear()
    external.send_keys(order_num)  # replaced with variable
    external.submit()
    time.sleep(1)

    action = Select(driver.find_element_by_id("action"))
    action.select_by_visible_text('Ship')
    driver.find_element_by_class_name("chub-button").click()
    time.sleep(2)

    # grab internal comm hub order number
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

    # find ship quantity field and enter 1, nothing else yet.
    read_quantity = driver.find_elements(By.CLASS_NAME, 'or_numericdata')
    qty = read_quantity[15].text

    inputs = driver.find_elements(By.TAG_NAME, 'input')
    ship_quantity = inputs[25]
    ship_quantity.send_keys(qty)
    ship_quantity.submit()


def update_tracking_staples(order_num: str, tracking_num: str, invoice_num: str, service: str, driver: any):
    """updates Staples or Quill orders

    The tracking number and carrier service are updated on a Staples or Quill order

     Parameters:
        order_num: string containing the Staples order number
        tracking_num: string containing the tracking number for the order
        invoice_num: string containing the invoice number of the order
        service: string containing the type of carrier service used
        driver: instance of the Chrome driver to be used

     Return:
        No return generated

    """
    external = driver.find_element_by_id("quicksearchCriteria")
    external.clear()
    external.send_keys(order_num)  # replaced with variable
    external.submit()
    time.sleep(1)

    action = Select(driver.find_element_by_id("action"))
    action.select_by_visible_text('Ship')
    driver.find_element_by_class_name("chub-button").click()
    time.sleep(2)

    # grab internal comm hub order number
    url = driver.current_url
    number = ''.join([letter for letter in url if letter.isdigit()])

    inv_input = driver.find_element_by_name("order(" + number + ").invoicenumber")
    print(type(invoice_num))
    invoice_num2 = invoice_num.split(".")[0]
    print(invoice_num2)
    inv_input.send_keys(invoice_num)
    print(invoice_num)

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

    # find ship quantity field and enter 1, nothing else yet.

    read_quantity = driver.find_elements(By.CLASS_NAME, 'or_numericdata')

    ship_status = read_quantity[9].text

    print(read_quantity[7].id)
    print(ship_status)
    print(len(read_quantity))

    advantage_size_of_single_line = 20
    quill_size_of_single_line = 22

    if (len(read_quantity) == advantage_size_of_single_line) or (len(read_quantity) == quill_size_of_single_line):
        inputs = driver.find_elements(By.TAG_NAME, 'input')
        if len(read_quantity) == advantage_size_of_single_line:
            qty = read_quantity[7].text
            print(qty)
            ship_quantity = inputs[30]
        else:
            qty = read_quantity[8].text
            print(qty)
            ship_quantity = inputs[30]
        ship_quantity.send_keys(qty)
        #ship_quantity.submit()
        # print("single")
    else:
        # print("multi")
        raise TypeError("NoSuchElementException")


def update_tracking_bbb(order_num: str, tracking_num: str, service: str, driver: any):
    """updates Bed Bath and Beyond (BBB) orders

        The tracking number and carrier service are updated on a BBB order

         Parameters:
            order_num: string containing the BBB order number
            tracking_num: string containing the tracking number for the order
            service: string containing the type of carrier service used
            driver: instance of the Chrome driver to be used

         Return:
            No return generated

        """
    external = driver.find_element_by_id("quicksearchCriteria")
    external.clear()
    external.send_keys(order_num)  # replaced with variable
    external.submit()
    time.sleep(1)

    action = Select(driver.find_element_by_id("action"))
    action.select_by_visible_text('Ship')
    driver.find_element_by_class_name("chub-button").click()
    time.sleep(2)

    # grab internal comm hub order number
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

    # find ship quantity field and enter 1, nothing else yet.
    read_quantity = driver.find_elements(By.CLASS_NAME, 'or_numericdata')
    qty = read_quantity[17].text

    inputs = driver.find_elements(By.TAG_NAME, 'input')
    ship_quantity = inputs[30]
    ship_quantity.send_keys(qty)
    ship_quantity.submit()


def update_invoice_macys(order_num, invoice_num, driver):
    """updates the Macy's orders

        The invoice number is updated to a Macy's order.

        Parameters:
            order_num: string with the order number
            invoice_num: string containing the invoice number of the Macy's order
            driver: instance of chrome driver to be used

        Return:
            No return generated

        """

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

    # read the quantity to be invoiced and put the value in the next field
    qty_field = inputs[-6]
    qty_field.send_keys(count)

    submission_fields = driver.find_elements_by_class_name("chub-button")
    submission_fields[1].click()


def update_invoice_bbb(order_num, invoice_num, driver):
    """updates the Bed Bath and Beyond orders

            The invoice number is updated to a BBB order.

            Parameters:
                order_num: string with the order number
                invoice_num: string containing the invoice number of the BBB order
                driver: instance of chrome driver to be used

            Return:
                No return generated

            """
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
    """create a folder for error file."""
    path = os.getcwd()
    dropbox = "/dropbox"
    try:
        if not os.path.exists(path+dropbox):
            os.mkdir(path+dropbox)
    except OSError:
        print("Error: unable to create drop box folder")
