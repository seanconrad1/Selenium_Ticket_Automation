# -----------------------------------------------------
# Creates and closes ticket automatically in SmartIT
#
# by Sean Conrad
# -----------------------------------------------------

import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
import ldapLookUp
import logging



# Main file function. Passing manually typed-in data from the GUI
def create_and_close_ticket(uname, pwd, employeeName, ticketInfo, resolutionNotes, site):
    try:
        # Loads the webdriver and places it in a variable called 'firefox'
        # Comment out wichever one you are not using.
        # PhantomJS is not working at the moment because I haven't figured out a
        # way to authenticate through Basic HTTP Authentication popups yet.
        # PhantomJS does not handle them the same was as the firefox driver
        firefox = webdriver.Firefox()
        # firefox = webdriver.PhantomJS()

        # Sets the window size
        firefox.set_window_size(1080, 1500)


        # Performs the ldap search to find the users full name.
        # File is called ldapLookup.py
        # Arguments passed are the user's username and password
        # This is also used to authenticate the user, if this fails,
        # user most likely used bad creds. Exception has been made for this
        # But, exception should print out to the GUI.
        fullName = ldapLookUp.findFullName(uname, pwd)

        # Opens website
        firefox.get('website')

    except Exception as e:
        logging.basicConfig(filename='log.log', level=logging.error("error:{}".format(e)))

    # Notes to self
    # For PhantomJS, use burp and proxies to
    # inspect the request being sent for basic HTTP authentication popups

    # Wait for authentication popup and type in credentials
    try:
        # WebDriverWait is a Selenium function where it
        # checks for the element every 500ms.
        # If the element is found, next line of code is executed.
        # You can set a timeout time as well if the element is not found.
        WebDriverWait(firefox, 10).until(EC.alert_is_present(),
                                         'Timed out waiting for PA creation ' +
                                         'confirmation popup to appear.')

        # switch_to.alert.send_keys finds the popup and sends
        # keys to it.
        firefox.switch_to.alert.send_keys(uname + Keys.TAB + pwd)
        firefox.switch_to.alert.send_keys(Keys.TAB)
        firefox.switch_to.alert.send_keys(Keys.TAB)
        firefox.switch_to.alert.send_keys(Keys.ENTER)
        print 'Credentials Worked!'



    # Exception is added if timeout happens
    except:
        pass


    # This function used throughout code to wait for elements to appear and then click them
    def useElement(xpath):
        try:
            wait = WebDriverWait(firefox, 25)
            wait.until(
                EC.presence_of_element_located((By.XPATH, xpath)))
            element = firefox.find_element_by_xpath(xpath)
            element.click()
        except NoSuchElementException, e:
            print 'No ' + xpath + ' visible.'

    # Storing elements in variables to be used with function 'useElement'
    # Same idea is used later in code as well
    console_button_xpath = '/html/body/div[2]/div/div[1]/div[1]/div[2]/div[4]/div/a'
    incident_element_xpath = '/html/body/div[2]/div/div[1]/div[1]/div[2]/div[4]/div/ul/li[3]/a/span[2]'
    searchbox_element_path = '/html/body/div[2]/div/div[1]/div[3]/div[2]/div/form/label/input'
    username_element_xpath = '//*[@id="typeahead-9891-8081-option-1"]/a/div/div[1]/div'
    impact_element_xpath = '//*[@id="main"]/div/div[1]/div[2]/form/div[4]/div/div[1]/div[2]/div[1]/label/div/div/button'
    localized_element_xpath = '//*[@id="main"]/div/div[1]/div[2]/form/div[4]/div/div[1]/div[2]/div[1]/label/div/div/ul/li[4]/a'
    urgancy_element_xpath = '//*[@id="main"]/div/div[1]/div[2]/form/div[4]/div/div[1]/div[2]/div[2]/label/div/div/button'
    low_urgency_xpath = '//*[@id="main"]/div/div[1]/div[2]/form/div[4]/div/div[1]/div[2]/div[2]/label/div/div/ul/li[4]/a'
    first_categorie = '//*[@id="category-dropdown-product"]'
    hardware_element = '//*[@id="category"]/div/div[1]/ul/li[3]'
    peripheral_element = '//*[@id="category"]/div/div[2]/ul/li[4]/div'
    none_element = '//*[@id="category"]/div/div[3]/ul/li[1]/div'
    save_button_xpath = '//*[@id="main"]/div/div[2]/div/button[1]'

    # Passing variables to 'useElement' function
    # Basically just clicking elements on the screen
    useElement(console_button_xpath)
    useElement(incident_element_xpath)



    # FIX MEEEEEEEEE!!!!!!!!!!!!!!!!
    # Select 'Affected Employee' text box and type in employee name
    # This breaks sometimes because I have had a hard time with selecting the
    # Element that appears when you type in the employees name
    # So right now, a static time is in place. So if the element takes too long to load, it fails.
    try:
        wait = WebDriverWait(firefox, 25)
        wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="main"]/div/div[1]/div[2]/form/div[2]/div/div[1]/label/div/input')))
        element = firefox.find_element_by_xpath(
            '//*[@id="main"]/div/div[1]/div[2]/form/div[2]/div/div[1]/label/div/input')
        element.send_keys(employeeName)
        time.sleep(4)
        element.send_keys(Keys.ARROW_DOWN)
        element.send_keys(Keys.ENTER)
    except NoSuchElementException, e:
        print 'No "Create New Element" visible'



    # Select Site Specific Walkup Ticket Template
    # Each site has their own template they use for walkups.
    # This is nice because it auto assigns the ticket to the correct site.
    # What's passed is the site location.
    try:
        wait = WebDriverWait(firefox, 25)
        wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="template"]')))
        element = firefox.find_element_by_xpath('//*[@id="template"]')
        element.send_keys(site)
        time.sleep(2)
        element.send_keys(Keys.ENTER)
        time.sleep(1)
    except NoSuchElementException, e:
        print 'No "Create New Element" visible'

    # Clicking more elements on the screen
    useElement(impact_element_xpath)
    useElement(localized_element_xpath)
    useElement(urgancy_element_xpath)
    useElement(low_urgency_xpath)

    # Move focus to description text box and type in ticket description
    descriptionElement = firefox.find_element_by_xpath('//*[@id="edit-summary-content-text"]')
    descriptionElement.send_keys(ticketInfo)

    # This scrolls the screen down to the correct location
    movepagedown = firefox.find_element_by_xpath('//*[@id="main"]/div/div[1]/div[2]/form/div[2]/div')
    movepagedown.click()
    movepagedown.send_keys(Keys.PAGE_DOWN)
    b = firefox.find_elements_by_tag_name('button')
    for item in b:
        if item.get_attribute('title') == 'Product Categorization Tier 2 ':
            item.click()


    # Move focus to CLI's
    # Find correct 'Browse Categories' button as there are three with the same XPATH.
    # Finds the xpath of the button, then finds a certain attribute of that element.
    # If the attribute matches what we are comparing it to, next code is executed.
    print 'Looking for CLIs'

    a = firefox.find_elements_by_xpath('//*[@id="category"]/div/div[2]/button[1]')
    for item in a:
        if item.get_attribute('aria-label') == 'Browse Categories Product Category':
            item.click()
    useElement(first_categorie)
    useElement(hardware_element)
    b = firefox.find_elements_by_tag_name('button')
    for item in b:
        if item.get_attribute('title') == 'Product Categorization Tier 2 ':
            item.click()
            useElement(peripheral_element)
        if item.get_attribute('title') == 'Product Categorization Tier 3 ':
            item.click()
            useElement(none_element)
    print 'Done!'

    # Clicks Save Button
    useElement(save_button_xpath)

    # EXTRACTS TICKET NUMBER
    # ***IF AN ERROR HAPPENS HERE, THEN TICKET DIDN'T GET CREATED***
    try:
        wait = WebDriverWait(firefox, 25)
        wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="ticket-header"]/div[3]/div/div/div[2]/div[2]/div[1]')))
        ticketNumberElement = firefox.find_elements_by_xpath(
            '//*[@id="ticket-header"]/div[3]/div/div/div[2]/div[2]/div[1]')
    except NoSuchElementException, e:
        print 'No ticket number visible'
        # Loops through whatever is in 'ticketnumberElement'
    for ticketNumberContent in ticketNumberElement:
        # Changes what was found in 'ticketnumberElement' to a string
        # And slices off the non-needed parts of the string
        ticketNumberNew = str(ticketNumberContent.text)[11:26]


    # CLOSING A TICKET---------------------------------------------------------------------------------------------------

    # Assigning HTML element xpaths to variables
    assign_to_me_button = '//*[@id="main"]/div/div[2]/div/div/div[2]/div[2]/div[3]/div[2]/div[3]'
    ticket_status_xpath = '//*[@id="main"]/div/div[2]/div/div/div[2]/div[1]/div[2]/div[1]/div'
    incident_status_xpath = '/html/body/div[4]/div/div/div/form/div[2]/div[2]/div[1]/div/div/label/div/button'
    in_progress_xpath = '/html/body/div[4]/div/div/div/form/div[2]/div[2]/div[1]/div/div/label/div/ul/li[2]/a'
    save_button3_xpath = '/html/body/div[4]/div/div/div/div/div/button[1]'
    incident_status_xpath2 = '/html/body/div[4]/div/div/div/form/div[2]/div[2]/div[1]/div/div/label/div/button'
    resolved_status = '/html/body/div[4]/div/div/div/form/div[2]/div[2]/div[1]/div/div/label/div/ul/li[4]/a'
    status_reason = '/html/body/div[4]/div/div/div/form/div[2]/div[2]/div[2]/div/label/div/button'
    no_further_action_required_selection = '/html/body/div[4]/div/div/div/form/div[2]/div[2]/div[2]/div/label/div/ul/li[5]/a'

    # Clicking things
    useElement(assign_to_me_button)
    time.sleep(2)

    # Bunch of clicking. Changes the ticket to 'in progress' and then to 'resolved'
    useElement(ticket_status_xpath)
    useElement(incident_status_xpath)
    useElement(in_progress_xpath)
    useElement(save_button3_xpath)
    time.sleep(7)
    useElement(ticket_status_xpath)
    useElement(incident_status_xpath)
    useElement(resolved_status)
    useElement(status_reason)
    useElement(no_further_action_required_selection)

    # Focuses on resolution notes text box and fills it out with the resolution notes.
    try:
        wait = WebDriverWait(firefox, 25)
        wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '/html/body/div[4]/div/div/div/form/div[2]/div[2]/div[4]/div[1]/label/textarea')))
        resolutionNotesElement = firefox.find_element_by_xpath(
            '/html/body/div[4]/div/div/div/form/div[2]/div[2]/div[4]/div[1]/label/textarea')
        resolutionNotesElement.click()
        resolutionNotesElement.send_keys(resolutionNotes)
    except NoSuchElementException, e:
        print 'No "Create New Element" visible'

    # Clicks save button
    saveButton3 = firefox.find_element_by_xpath('/html/body/div[4]/div/div/div/div/div/button[1]')
    saveButton3.click()

    print 'Ticket Resolved!'

    # Returns output to GUI
    firefox.close()
    return ticketNumberNew

