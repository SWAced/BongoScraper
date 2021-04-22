import subprocess
import sys

subprocess.check_call([sys.executable, '-m', 'pip', 'install', 
'selenium'])

subprocess.check_call([sys.executable, '-m', 'pip', 'install', 
'bs4'])

from selenium import webdriver
import time
import os
import csv
import re
import platform
from datetime import datetime

try:

    review_limit = int(input("\nEnter the minimum amount of reviews you'd like to consider for the scraper: "))
    date_limit = datetime.strptime(datetime.strptime(input("\nEnter the oldest date you'd like to consider for the scraper (for example: 15/11/2001 => dd/mm/yyyy): "), '%d/%m/%Y').strftime("%d/%m/%Y"), '%d/%m/%Y')


    total_data = []

    csvinput = os.path.join(sys.path[0], 'data.csv')
    csvoutput = os.path.join(sys.path[0], 'reviews.csv')

    plat = platform.system()

    if 'Windows' in plat:
        dp = os.path.join(sys.path[0], 'chromedriver.exe')
        print(sys.path[0])
    else:
        dp = os.path.join(sys.path[0], 'chromedriver')

    urls = []

    with open(csvinput) as input_file:
        data = csv.reader(input_file)
        for row in data:
            try:
                if int(row[4]) > review_limit: 
                    urls.append(row[5])
            except:
                pass
    
    try:
        urls.remove('URL')
    except:
        pass
    #print(urls)

    testurl = "https://www.bongo.be/nl/cadeaubonnen/weekendje-weg-overnachten/magisch-weekend-in-een-4-sterrenhotel-in-brugge-1358243.html"

    def find_attribute(rev, elem, attr):
        try:
            return rev.find_element_by_css_selector(elem).get_attribute(attr).strip()
        except:
            return 'null'

    print("\nCreating browser instance & going through all the comments for each link...\n")
    for url in urls:
        try:
            wb = webdriver.Chrome(executable_path=dp)
            wb.set_window_size(1300, 1000)
        except Exception as e:
            print('Unable to create browser instance because of the following error: ', str(e))
            input('')
            exit()

        wb.get(url)

        try:
            wb.find_element_by_id("onetrust-accept-btn-handler").click()
        except:
            pass

        while True:
            try:
                time.sleep(2)
                wb.find_element_by_class_name("button.button--ghost.reviews__see-more__button").click()
            except:
                break
        #reviews__body__review
        collection = wb.find_elements_by_css_selector("article.reviews__body__review")
     
        for rev in collection:
            title = find_attribute(rev, "h4[class*='review__title']", "innerText")
            date = find_attribute(rev, "p[class*='review__date']", "innerText")
            realdate = datetime.strptime(datetime.strptime(date, '%d/%m/%Y').strftime("%d/%m/%Y"), '%d/%m/%Y')
            if find_attribute(rev, "meta[itemprop*='ratingValue']", "content") == 'null' or find_attribute(rev, "meta[itemprop*='ratingValue']", "content") == '0':
                rating = float(0)
            else:
                rating = float(float(find_attribute(rev, "meta[itemprop*='ratingValue']", "content")) / 2)

            testid = re.findall(r"-(\d+)\.html", url)
            if len(testid) > 0:
                _id = testid[0]
            else:
                _id = "null"
            if realdate >= date_limit: 
                cols = [_id, datetime.strftime(realdate, "%d/%m/%Y"), title, rating]
                total_data.append(cols)
                #print(cols)
        wb.quit()
        #Remove this break statement to unleash the full power of the scraper, but it's very intensive.
        break
    
    print("\nWriting all data to a csv file called reviews.csv...\n")

    c = open('reviews.csv', 'w', newline='')
    final = csv.writer(c)
    final.writerow(['ID', 'Review Date', 'Activity Name', 'Star Rating (/5)'])
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