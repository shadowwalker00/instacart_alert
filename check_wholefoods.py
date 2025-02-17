import sys, os, re, time, json
from utils import *

chromedriver = "./chromedriver"

# amazon credentials
with open('./credential.json') as f:
    credential = json.load(f)
username = credential['wholefoods']['username']
password = credential['wholefoods']['passwd']
assert('username' in credential['wholefoods'])
assert('passwd' in credential['wholefoods'])

# hyper parameter
time_lapse = 3.0

def check_slots():
    print('Creating Chrome Driver ...')
    driver = create_driver()

    print('Logging into Amazon ...')
    driver.get('https://www.amazon.com/gp/sign-in.html')
    email_field = driver.find_element_by_css_selector('#ap_email')
    email_field.send_keys(username)
    driver.find_element_by_css_selector('#continue').click()
    time.sleep(time_lapse)
    password_field = driver.find_element_by_css_selector('#ap_password')
    password_field.send_keys(password)
    driver.find_element_by_css_selector('#signInSubmit').click()
    time.sleep(time_lapse)

    print('Redirecting to AmazonFresh ...')
    driver.get('https://www.amazon.com/alm/storefront?almBrandId=QW1hem9uIEZyZXNo')
    time.sleep(time_lapse)
    print('Step 1: Go to cart .....')
    driver.find_element_by_id('nav-cart').click()
    time.sleep(time_lapse)
    
    print('Step 2: Review cart for Amazon Fresh .....')
    driver.find_element_by_name('proceedToALMCheckout-VUZHIFdob2xlIEZvb2Rz').click()    
    time.sleep(time_lapse)
    
    
    print('Step 3: Check out page.....')
    driver.find_element_by_name('proceedToCheckout').click()    
    time.sleep(time_lapse)

    print('Step 4: Collecting delivery availability .....')
    substitution_but = driver.find_element_by_css_selector('input.a-button-input')
    if(substitution_but!=None):
        substitution_but.click()
        time.sleep(time_lapse)


    slots_available = False

    while not slots_available:
        dates = driver.find_elements_by_css_selector('div.ufss-date-select-toggle-text-month-day')
        time.sleep(time_lapse)

        availabilities = driver.find_elements_by_css_selector('div.ufss-date-select-toggle-text-availability')
        time.sleep(time_lapse)
        
        date_avail_map = list(zip(dates, availabilities))
        if(len(date_avail_map)==0):
            error_alert()

        for date, avbl in date_avail_map:
            print('date: {}, available: {}'.format(date.text, avbl.text))
            if(avbl.text!='Not available'):
                slots_available = True                
                break
        if slots_available: 
            print('Slots Available!')
            sound_alert_macos('say "WholeFoods Find Slot GO GET IT"')
            break
        else:
            print('Cur time: {}, No slots available. Sleeping ...'.format(display_time()))
            time.sleep(150)
            driver.refresh()
    
    time.sleep(300)
    terminate(driver)

if __name__ == "__main__":
    print('------ Check  Whole Foods -------')
    check_slots()