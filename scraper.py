from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import csv
import requests
import json
import time
from multiprocessing.dummy import Pool as ThreadPool
import elastic


# outfilename = "out.json"
# f2 = open(outfilename, "w",encoding="utf-8")

jsonarray = []

def getAsin(gist):
    gist_data = requests.get(gist)
    asins = gist_data.text
    f.write(asins)
    with open('ASIN.csv') as csvfile:
        reader = csv.reader(csvfile)
        asin_list = list(reader)
    return asin_list



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


def getPrice(driver):
    
    try:
        if (driver.find_element_by_id("priceblock_ourprice")== None):
            # print("1")
            price_div = driver.find_elements_by_class_name("a-color-price")
            price_inDollar = price_div[1].text.strip()
            try:
                price_inCent = float(price_inDollar.strip('$').strip("'")) * 100
                return price_inCent
            except:
                return price_inDollar

        elif(driver.find_element_by_id("price_inside_buybox") != None):
            # print("2")
            price_span = driver.find_element_by_id("price_inside_buybox")
            price_inDollar = price_span.text.strip()
            try:
                price_inCent= float(price_inDollar.strip('$').strip("'")) * 100
                return price_inCent
            except:
                return price_inDollar

        else:
            price_inDollar= driver.find_element_by_id("priceblock_ourprice").text.strip()
            # print("3")
            try:
                price_inCent = float(price_inDollar.strip('$').strip("'")) * 100
                return price_inCent
            except:
                return price_inDollar
    except:
        return "None"


def getImages(driver):
    images = []
    try:
        img_div = driver.find_element_by_id("imageBlock")
    except:
        try:
            img_div = driver.find_element_by_id("imageBlockThumbs")
        except:
            try:
                img_div = driver.find_element_by_id("altImages")
            except:
                return images

    for img in img_div.find_elements_by_tag_name("img"):
        if img.get_attribute('src').endswith(".jpg"):
            img_src = img.get_attribute('src').split(".")
            img_src[3] = "_UL900_"
            images.append(".".join(img_src))

    return images


def makeDict(driver):
    data = {

        'title': driver.find_element_by_id("title").text.strip(),
        'price': getPrice(driver),
        'images': getImages(driver)

        }
    return data



def foreachURL(product_urls):
    try:
        driver = getDriver()
        driver.get(product_urls)

        if driver.find_element_by_id("productTitle") is None:
            raise ValueError('Product not available')

        dict_data = makeDict(driver)
        jsonarray.append(dict_data)
        # jsonarray.append(dict_data)
        # print(dict_data)
    except:
        return 1+2

    return jsonarray




def main():

    with open('asin.csv') as csvfile:
        reader = csv.reader(csvfile)
        asin_list = list(reader)
        product_urls = []


    for i in range(50):
        productUrl = "http://www.amazon.com/dp/" + asin_list[i][0]
        product_urls.append(productUrl)


    pool = ThreadPool(8)
    json_out = pool.map(foreachURL, product_urls)
    pool.close()
    pool.join()


    # print(json_out[0])
    count  = 1
    for i in json_out[0]:
        json_output = json.dumps(i, indent=4)
        elastic_search.index(index="amazon", doc_type="product-title",id = count, body= json_output)
        count = count +1


    # elastic_search.get(index='amazon', doc_type='product-title', id=3)


if __name__ == "__main__":
    elastic_search = elastic.connect_elasticsearch()
    main()
