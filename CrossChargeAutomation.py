#----------------------------------------------------------
# Automates cross charging items. This also is responsible
# for updating the CCitems file. Which updates the CC items
# dropdown on the SmartIT Auatomation GUI.
#
# By Sean Conrad
#----------------------------------------------------------

import time
import collections
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException


# Takes username, password, employee name, ticket number and a dictionary as arguments
def crossCharge(uname, pwd, employee_name, remedyTicket, dictionary):

    # Same shpiel here with selecting a driver
    firefox = webdriver.Firefox()
    # firefox = webdriver.PhantomJS()

    # Window size
    firefox.set_window_size(1080, 1500)

    # Function to wait for elements to appear and then click them
    # Same as the one in CreatingAndClosingTicket.py
    def useElement(xpath):
        try:
            wait = WebDriverWait(firefox, 25)
            wait.until(
                EC.presence_of_element_located((By.XPATH, xpath)))
            element = firefox.find_element_by_xpath(xpath)
            element.click()
        except NoSuchElementException, e:
            print 'No "Create New Element" visible'


    firefox.get('website')

    time.sleep(2)

    #Authenticate to CC page
    try:
        WebDriverWait(firefox, 10).until(EC.alert_is_present(),
                                         'Timed out waiting for PA creation ' +
                                         'confirmation popup to appear.')

        # Use burp and proxies to inspect the request
        # Selenium web element expect

        firefox.switch_to.alert.send_keys(uname + Keys.TAB + pwd)
        firefox.switch_to.alert.send_keys(Keys.TAB)
        firefox.switch_to.alert.send_keys(Keys.TAB)
        firefox.switch_to.alert.send_keys(Keys.ENTER)
        print 'Credentials Worked!'
    except firefox.TimeoutException:
        print "no alert"


    #Do stuff here

    #Type in username
    try:
        wait = WebDriverWait(firefox, 25)
        wait.until(
            EC.presence_of_element_located((By.ID, 'ctl00_ContentPlaceHolder1_RadAutoCompleteBoxUserName_Input')))
        element = firefox.find_element_by_id('ctl00_ContentPlaceHolder1_RadAutoCompleteBoxUserName_Input')
        element.send_keys(employee_name)
    except NoSuchElementException, e:
        print 'No "Create New Element" visible'

    #Waits for username element to appear and hits enter
    try:
        wait = WebDriverWait(firefox, 25)
        wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="form2"]/div[1]/div')))
        element = firefox.find_element_by_xpath('//*[@id="form2"]/div[1]/div')
        element.send_keys(Keys.ENTER)
        time.sleep(3)
    except NoSuchElementException, e:
        print 'No "Create New Element" visible'


    #Type in ticket number
    try:
        wait = WebDriverWait(firefox, 25)
        wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_rtbRemedyTicket"]')))
        element = firefox.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_rtbRemedyTicket"]')
        element.send_keys(remedyTicket)
    except NoSuchElementException, e:
        print 'No "Create New Element" visible'

    #Clicks the dropdown button
    itemDropdown = '//*[@id="ctl00_ContentPlaceHolder1_rcbItem_Input"]'
    useElement(itemDropdown)

    #Writes Item list to a file to be read by MainWindow.py and updates GUI
    ccItems = open('CCitems.txt', 'w+')
    a = []
    html_list = firefox.find_element_by_class_name("rcbList")
    items = html_list.find_elements_by_tag_name("li")
    for item in items:
        text = item.text
        text = text.encode('utf-8')
        a.append(text)
    b = ' \n'.join(a)
    ccItems.write(b)


    orderedCart = collections.OrderedDict(dictionary)  # Creates ordered dict
    for device, quantity in orderedCart.iteritems():
        print device + ' this is working! ' + quantity  # Iterates through dict and creates string with format
        #Selects item
        try:
            itemDropdown = '//*[@id="ctl00_ContentPlaceHolder1_rcbItem_Input"]'
            useElement(itemDropdown)
            html_list = firefox.find_element_by_class_name("rcbList")
            c = html_list.find_elements_by_tag_name("li")
            time.sleep(1)
        except StaleElementReferenceException:
            pass

        for item in c:
            #if item.text == device:
            if item.text == device:
                item.click()
                time.sleep(1)
                break

        quantityDropdown = '//*[@id="ctl00_ContentPlaceHolder1_rcbQuantity_Input"]'
        useElement(quantityDropdown)

        try:
            #Selects quantity
            html_list = firefox.find_element_by_class_name("rcbList")
            c = html_list.find_elements_by_tag_name("li")
            for item in c:
                if item.text == quantity:
                    time.sleep(.5)
                    item.click()
                    time.sleep(.5)
                    add_to_cart = ('//*[@id="ctl00_ContentPlaceHolder1_rbAddToCart"]')
                    useElement(add_to_cart)
                    time.sleep(1)
        except StaleElementReferenceException:
            pass





    #FIXX MEEE!!!!!!!!!!!!!!!!!!!!!
    submit = ('//*[@id="ctl00_ContentPlaceHolder1_rbtSubmitForReview"]')
    useElement(submit)

    #print device + ' cross-charged to ' + employee_name

    firefox.close()


