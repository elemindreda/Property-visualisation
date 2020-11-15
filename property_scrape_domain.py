import pandas as pd
import numpy as np
import time
import os
import tabula
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import xlsxwriter


def timesleep(init, final = None):
    # rand100-200  == random time between 100 to 200
    # rand5-20 == random time between 5 to 20
    if not final:
        secs = np.random.randint(init, final)
    else: 
        secs = init

    for t in range(0,secs):
        time.sleep(1)
        print(t+1, end=' -> ')
    print('\n')



def scroll_shim(browser, object):
    ## Shims the browser to location of object we want to click
    x = object.location['x']
    y = object.location['y']
    scroll_by_coord = 'window.scrollTo(%s,%s);' % (
        x,
        y
    )
    scroll_nav_out_of_way = 'window.scrollBy(0, -120);'
    passed_in_driver.execute_script(scroll_by_coord)
    passed_in_driver.execute_script(scroll_nav_out_of_way)
    return browser


def input_search_and_sort(browser, suburb, searchtype):

    ### Set up the Filters ##
    filters = browser.find_element_by_xpath(
        '/html/body/div[2]/div[1]/div[3]/div/div/form/div[2]/div/div/div[1]/div/div/section/div/div/div/div/div[2]/button'
    )
    filters.click()
    timesleep(1)
    ## search only in the suburb we want. ##
    untick_nearby_suburbs = browser.find_element_by_xpath(
    '/html/body/div[2]/div[1]/div[3]/div/div/div/div[1]/div/div[4]/label/div[2]'
    )
    untick_nearby_suburbs.click()


    ## Type of Transaction we want to search ##
    sold_button = browser.find_element_by_xpath(
    '/html/body/div[2]/div[1]/div[3]/div/div/div/div[1]/div/div[2]/div/button[4]'
    )
    rent_button = browser.find_element_by_xpath(
    '/html/body/div[2]/div[1]/div[3]/div/div/div/div[1]/div/div[2]/div/button[2]'
    )
    buy_button = browser.find_element_by_xpath(
    '/html/body/div[2]/div[1]/div[3]/div/div/div/div[1]/div/div[2]/div/button[1]'
    )

    if searchtype == 'sold':
        sold_button.click()
        sort_by_newest = browser.find_element_by_xpath('//*[@id="search-results-sort-by-filter-item-1"]')

    elif searchtype == 'buy':
        buy_button.click()
        sort_by_newest = browser.find_element_by_xpath('//*[@id="search-results-sort-by-filter-item-1"]')

    elif searchtype == 'rent':
        rent_button.click()
        sort_by_newest = browser.find_element_by_xpath('//*[@id="search-results-sort-by-filter-item-0"]')

    timesleep(2)

    ## Find input bar and send the suburb name we want to search ##
    input_bar = browser.find_element_by_xpath(
    '/html/body/div[2]/div[1]/div[3]/div/div/div/div[1]/div/div[3]/div[1]/div/div/section/div/div/div/div/div[1]/div/input'
    )

    input_bar.send_keys(suburb)
    
    ## Find search button and click ##
    search_button = browser.find_element_by_xpath(
    '/html/body/div[2]/div[1]/div[3]/div/div/div/div[1]/div/div[3]/div[2]/button/span[2]/span'
    )
    search_button.click()

    timesleep(2, 5)

    check_if_matches = browser.find_elements_by_tag_name('h3')

    for matches in check_if_matches:
        matches = matches.text.strip().lower()
        if 'no exact matches' in matches:
            nomatches = True
            return browser, nomatches

    ## Sort the results by newest ## 
    sort_by = browser.find_element_by_xpath(
    '/html/body/div[1]/div/div/div[4]/div[2]/div[1]/div[2]/div/div[2]/div[2]/div/div/button'
    )
    sort_by.click()
    print(sort_by.text)

    
    sort_by_newest.click()

    nomatches = False

    ## Check if suburb has any new entries ##
    ## To be added ##
    return browser, nomatches



property_data = {}
postcodes = pd.read_csv('postcode.csv', index_col = 0)
url = 'https://www.domain.com.au'
log = []


extensions = [
    'uBlock0@raymondhill.net.xpi',
    ]

extension_dir = 'C:\\Users\\waghu\\OneDrive\\Python_Projects\\__drivers__\\'





search_type = ['sold','rent','buy']
suburb_nomatches = []


for suburb in postcodes.values.tolist():
    for searchtype in search_type:

        print('loading webpage... Searching for %s homes in %s' % (searchtype, str(suburb).strip())
        browser = webdriver.Firefox()
        browser.get(url)
        timesleep(2, 5)

        print('installing extensions')
        timesleep(2)
        for extension in extensions:
            browser.install_addon(extension_dir + extension)

        print('setting up search & sort')
        browser, nomatches = input_search_and_sort(browser, suburb, searchtype)
        timesleep(5,20)
        

        
        if nomatches:
            suburb_nomatches.append(str(suburb))
            browser.close()
            break

        browser.close()

    delete_nomatches(postcodes.values.tolist(), suburb_nomatches)



def delete_nomatches(postcodes, suburb_nomatches):
    for suburb in suburb_nomatches:
        if suburb in postcodes:
            postcodes.remove(suburb)



