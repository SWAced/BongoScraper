import subprocess
import sys

subprocess.check_call([sys.executable, '-m', 'pip', 'install', 
'selenium'])

subprocess.check_call([sys.executable, '-m', 'pip', 'install', 
'bs4'])

from selenium import webdriver
import time
import os
from bs4 import BeautifulSoup
import csv
import re
import platform

try:
    delay = int(input("Enter the delay between expanding pages. For a fast setup, use 2. For a mediocre setup, use 4. For a slower setup, use 6. It is not recommended to run this script on a slower machine as it will greatly delay the scraping.\n"))

    url = "https://www.bongo.be/nl/cadeaubonnen.html?sortby=position&page=1&pagesize=24&="

    total_data = []

    plat = platform.system()

    if 'Windows' in plat:
        dp = os.path.join(sys.path[0], 'chromedriver.exe')
        print(sys.path[0])
    else:
        dp = os.path.join(sys.path[0], 'chromedriver')

    #print(dp)

    try:
        wb = webdriver.Chrome(executable_path=dp)
        wb.set_window_size(1100, 700)
    except Exception as e:
        print('Unable to create browser instance because of the following error: ', str(e))
        input('')
        exit()

    wb.get(url)

    amount = int(wb.find_elements_by_css_selector("span.search-result-label__number.qa-search-result-label-number")[0].get_attribute('innerText'))
    #print(amount)

    while True:
        try:
            wb.find_element_by_id("search-more-results").click()
            time.sleep(delay)
        except:
            break

    print("Successfully found all results. Now scanning for useful data iteratively...\n")

    collection = wb.find_elements_by_css_selector("article.thematic")

    def find_attribute(prod, elem, attr):
        try:
            return prod.find_element_by_css_selector(elem).get_attribute(attr).strip()
        except:
            return 'null'

    for product in collection:
        link = find_attribute(product, "a.thematic__wrapper-link", 'href')
        title = find_attribute(product, "h3[data-bind*='box_name']", "innerText")
        amount_of_reviews = find_attribute(product, "span.rating__number-reviews", 'innerText')
        price = find_attribute(product, "span.qa-thematic-price", 'innerText')
        rating = float(float(find_attribute(product, "a.thematic__wrapper-link", 'data-product-reviewrating').replace(",", ".")) / 2)
        testid = re.findall(r"-(\d+)\.html", link)
        if len(testid) > 0:
            _id = testid[0]
        else:
            _id = "null"
        #print(link, title, amount_of_reviews, price, rating, _id)
        #break
        cols = [_id, title, price, rating, amount_of_reviews, link]

        if not (cols in total_data):
            total_data.append(cols)

    print("Successfully extracted all necessary data from the results. Adding it into a csv file named 'data.csv'...\n")

    wb.quit()  
    c = open('data.csv', 'w', newline='')
    final = csv.writer(c)
    final.writerow(['ID', 'Product Title', 'Price', 'Rating (/5)', 'Amount of Reviews', 'URL'])
    for row in total_data:
        final.writerow(row)

    c.close()
    print("Successfully saved the collective data in the same directory as this script.\n")
    input("Press any key to close the window.\n")
    exit()
except Exception as exe:
    print("Could not continue process because of the following exception: ", str(exe))
    input('')
    exit() 