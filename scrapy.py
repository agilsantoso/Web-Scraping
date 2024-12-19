import tqdm 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException  
import pandas as pd
import time

output = []
url = "https://www.sizeofficial.es/"

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
# options.headless = True
driver = webdriver.Chrome(options=options)
driver.get(url)
driver.minimize_window()
time.sleep(2)
cookies = driver.find_element(By.XPATH, "/html/body/div[6]/div[2]/div/div[2]/button[2]").click()

categories_list = []
categories = driver.find_elements(By.CSS_SELECTOR, 'a[class=" wChild"]')
for category in categories:
    obj_find = category.get_attribute("href")
    categories_list.append(obj_find)

# def scraper(target, data):
open = categories_list[1]
next_button_enabled = True
while next_button_enabled:
    driver.get(open)
    time.sleep(1)
    for i in range(24):
        try:
            driver.find_element(By.XPATH, '//*[@id="productListMain"]/li['+str(i+1)+']/span').click()
            time.sleep(1)
            # href scrape
            product_href = ""
            try:
                target = driver.find_element(By.CSS_SELECTOR, 'link[rel="canonical"]')
                product_href = target.get_attribute("href")
            except NoSuchElementException:
                pass
            print("product_href: ", product_href)

            #name scrape
            name = ""
            try:
                name = driver.find_element(By.CSS_SELECTOR, 'h1[itemprop="name"]').text
            except NoSuchElementException:
                pass
            print("name: ", name)

            #sizes scrape
            size_list = driver.find_elements(By.CSS_SELECTOR, 'button[data-e2e="pdp-productDetails-size"]')
            size_data = []
            try:
                for size in size_list:
                    result = size.get_attribute("data-size")
                    size_data.append(result)
            except NoSuchElementException:
                pass
            def list_to_string(size_data):
                str1 = ""
                for i in size_data:
                    str1 += i + " | "
                return str1
            sizes = list_to_string(size_data)
            print("sizes: ", sizes)

            #images source scrape 
            img_list = driver.find_elements(By.CSS_SELECTOR, 'img[class="imgMed  "]')
            img_data = []
            try:
                for img in img_list:
                    result = img.get_attribute("src")
                    img_data.append(result)
            except NoSuchElementException:
                pass
            images_src = list_to_string(img_data)
            print("images_src: ", images_src)

            #prices scrape
            current_price = ""
            try:
                current_price = driver.find_element(By.CLASS_NAME, 'pri').text
                print("current price: ", current_price)
            except NoSuchElementException:
                pass
            old_price = ""
            try:
                old_price = driver.find_element(By.CLASS_NAME, 'was').text
                print("old prices: ", old_price)
            except NoSuchElementException:
                old_price = current_price
                print("old prices: ", current_price)

            #brand scrape
            brand = ""
            try:
                brand = driver.find_element(By.CLASS_NAME, "brand-title").text
                print("brand: ", brand)
            except NoSuchElementException:
                pass

            #description
            description_ = ""
            try:
                description_ = driver.find_element(By.CLASS_NAME, "acitem").text.split("\n")
            except NoSuchElementException:
                pass
            descriptions = ""
            try:
                descriptions = description_[0] + ": " + description_[1] + " | " + description_[2] + ": " + description_[3] + " | " + description_[4]
            except IndexError:
                pass
            print(descriptions)

            #gender
            gender = ""
            try:
                gender = driver.find_element(By.XPATH, '//*[@id="breads"]/div/span[2]/a').text
            except NoSuchElementException:
                pass
            print("Gender", gender)

            dict = {"web-scraper-start-url": product_href + " / " + gender,
                    "Product href": product_href,
                    "Name": name,
                    "Sizes": sizes,
                    "Images Sources": images_src,
                    "Old Price": old_price,
                    "Current Price": current_price,
                    "Brand": brand,
                    "Description": descriptions,
                    "Gender": gender}
            output.append(dict)
            new_df = pd.DataFrame(output)
            df = pd.read_csv("Data.csv")
            df = pd.concat([df, new_df], ignore_index=False)
            df.to_csv("Data.csv", index=False, encoding="utf-8-sig")
            output = []
            driver.back()
            time.sleep(1)
        except NoSuchElementException:
            break
    try:
        driver.find_element(By.CSS_SELECTOR, 'a[rel="next"]').click()
        time.sleep(2)
    except NoSuchElementException:
        next_button_enabled = False
    open = driver.find_element(By.CSS_SELECTOR, 'link[rel="canonical"]').get_attribute("href")
    open = str(open)
#     return df.to_csv("Data.csv", index=False, encoding="utf-8-sig")

# data = "Data.csv"
# for obj in categories_list[1:]:
#     scraper(obj, data)