from multiprocessing.dummy import Pool as ThreadPool
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import csv
import requests
import json
import time
filename = "asin2.csv"
f = open(filename, "w",encoding="utf-8")
similar_items = []



#####################################################


def getDriver():
    mypath = "C:\webdrivers\chromedriver.exe"
    options = Options()
    options.add_argument("--headless")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('start-maximized')
    options.add_argument('disable-infobars')
    options.add_argument("--disable-extensions")

    driver = webdriver.Chrome(executable_path = mypath, chrome_options = options)

    return driver



def getSimilar( product_urls):

    try:
        driver = getDriver()
        driver.get(product_urls)

        if driver.find_element_by_id("productTitle") is None:
            raise ValueError('Product not available')

        # similar_asin_list = getSimilar(driver)

        for li_item in driver.find_elements_by_class_name("a-carousel-card"):
            try:
                similar_div = li_item.find_element_by_tag_name("div")
                similar_asin = similar_div.get_attribute('data-asin')
                if (similar_asin != None):
                    similar_items.append(similar_asin)
            except:
                return 1+1

        similar_csv(similar_items)

    except:
        return 1+2




def similar_csv(similar_asin_list):
    print(similar_asin_list)
    with open('asin2.csv', 'w', newline = '') as output_write:
        csvout = csv.writer(output_write)
        for asin in similar_asin_list:
             csvout.writerow((asin, ))


def main():
    with open('asin1.csv') as csvfile:
        reader = csv.reader(csvfile)
        asin_list = list(reader)
        product_urls = []

    for i in range(5555):
        # print(i)
        productUrl = "http://www.amazon.com/dp/" + asin_list[i][0]
        product_urls.append(productUrl)

    # print(product_urls)


    pool = ThreadPool(10)
    pool.map(getSimilar, product_urls)
    pool.close()
    pool.join()



if __name__ == "__main__":
    main()
