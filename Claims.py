import bs4
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import requests

FedEx_url = 'https://www.fedex.com/apps/onlineclaims/?locale=en_US'

res = requests.get(FedEx_url)
bs = bs4.BeautifulSoup(res.text, "html.parser")

driver = webdriver.Chrome

driver.get(FedEx_url)

tracking_number = driver.find_element_by_id("trackinNumber")
tracking_number.send_keys("01010101010101")