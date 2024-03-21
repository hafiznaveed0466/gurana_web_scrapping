import requests
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re
import time
import random
import pandas as pd


s = Service("C:/Users/Muhammad Naveed/Desktop/webDriver/chromedriver-win32/chromedriver.exe")
driver = webdriver.Chrome(service=s)

driver.get("https://www.graana.com/")
time.sleep(5)
driver.maximize_window()
time.sleep(10)

driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div/div[2]/div[2]/a/button').click()
time.sleep(5)
driver.find_element(By.XPATH, '//*[@id="xperience-header-desk"]/div/div/div/section/div/div[1]/div/div/div/a').click()
time.sleep(2)
search = driver.find_element(By.XPATH, '//*[@id=":r0:"]')
search.send_keys("islamabad")
time.sleep(3)
driver.find_element(By.XPATH, '//*[@id="__next"]/div[3]/div[2]/div[2]/div/div[2]/ul/div[2]').click()
time.sleep(2)
driver.find_element(By.XPATH, '//*[@id="__next"]/div[3]/div[2]/div[2]/div/button').click()
time.sleep(15)
page_source = driver.page_source
soup = BeautifulSoup(page_source, "lxml")

df = pd.DataFrame({'address': [''],'area':[''], 'city':[''], 'property_type': [''], 'prices':[''], 'currency':[''], 'contact': ['']})
data = []
c = 0
while c < 3:
    div_tag = soup.find("div", class_="MuiBox-root mui-style-1osduea")
    posts = div_tag.find_all("div", class_="MuiBox-root mui-style-17zbhp0")
    print(len(posts))
    for post in posts:
        if(c>0):
            print(post)
        link = post.find("a").get("href")
        source = "https://www.graana.com"
        com_link = source+link

        driver.get(com_link)
        time.sleep(5)
        link_page_source = driver.page_source
        soup1 = BeautifulSoup(link_page_source, "lxml")
        try:
            address = soup1.find("h1", class_="MuiTypography-root MuiTypography-h3New mui-style-s6x0cd").text
            property_type = soup1.find("div", class_="MuiTypography-root MuiTypography-subtitle2New mui-style-1d3e9wz").text
            price = soup1.find("span", class_="MuiTypography-root MuiTypography-h2New mui-style-1k6ms13").text
            currency = soup1.find("div", class_="MuiTypography-root MuiTypography-h6New MuiTypography-gutterBottom mui-style-1atyhfr").text
            # city = address.split(",")[-1].strip()
            # Splitting the address based on commas
            address_parts = address.split(",")
            if len(address_parts) == 2:  # If there's only one comma
                if "Sale" in address_parts[0]:
                    area = address_parts[0].split("Sale")[1].strip()
                elif "sale" in address_parts[0]:
                    area = address_parts[0].split("sale")[1].strip()
                else:
                    area = address_parts[0].strip()
                city = address_parts[1].strip()
            elif len(address_parts) >= 3:  # If there are two or more commas
                area = address_parts[1].strip()  # First comma is area
                city = address_parts[2].strip()  # Second comma is city
            else:  # If address format is unexpected
                area = "Unknown"
                city = "Unknown"
            # print(address, ' ', property_type, ' ', price, ' ',currency,' ', city, '', area)
            driver.find_element(By.XPATH, '//*[@id="__next"]/div[3]/div[2]/div[2]/div/button[1]').click()
            time.sleep(2)
            page_source2 = driver.page_source
            soup2 = BeautifulSoup(page_source2, "lxml")
            number = soup2.find("a", style = "text-decoration: none;").get("href")
            print(number)
            data.append({'address': address,'area':area, 'city':city, 'property_type': property_type, 'prices': price, 'currency': currency, 'contact': number})
        except Exception as e:
            print("An exception occurred:", e)
            pass

    url = "https://www.graana.com/sale/residential-properties-sale-islamabad-1/?pageSize=30&page="+str(c+2)
    driver.get(url)
    time.sleep(5)
    source_page1 = driver.page_source
    soup = BeautifulSoup(source_page1,"lxml")
    print(c)
    c = c+1

df = pd.DataFrame(data)
df.to_csv("Downloaded1.csv", index=False)










    # price = post.find("div", class_="MuiTypography-root MuiTypography-h4New mui-style-gz23my").text.strip()
    # currency = post.find("div", class_="MuiTypography-root MuiTypography-subtitle1New mui-style-1cbbqe9").text.strip()
    # address = post.find("h5", class_="MuiTypography-root MuiTypography-subtitle2New mui-style-3bzwbl").text
    #
    # print(com_link, ' ',price, ' ', currency, ' ', address)

    # break






# posts = div_tag.find_all("div", class_ = "MuiBox-root mui-style-17zbhp0")
# print(len(posts))
# time.sleep(100)
# for post in posts:
#     link = post.find("a", style = "text-decoration: none;").get("href")
#     print('link of post','  ',link)
#     break






# driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div/div[2]/div[2]/a/button').click()
# time.sleep(50)
# driver.find_element_by_xpath("""/html/body/div[1]/div[1]/header/div/section[1]/div/div/div/section/div/div[1]/div/div/div/a""").click()

#
# /html/body/div[1]/div[2]/div/div[2]/div[2]/a/button


#
#


# time.sleep(10)
# search = driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[2]/div[2]/div/div[1]/div/div/input")
# time.sleep(3)
# search.send_keys('islamabad')
# time.sleep(2)
# driver.find_element_by_xpath("""/html/body/div[1]/div[3]/div[2]/div[2]/div/div[2]/ul/div[3]""").click()
# time.sleep(30)
# driver.find_element_by_xpath("""/html/body/div[1]/div[3]/div[2]/div[2]/div/button""").click()
#
#
# time.sleep(10)
# # Now, get the page source and create a BeautifulSoup object
# page_source = driver.page_source
# soup = BeautifulSoup(page_source, 'lxml')
#
# names = soup.find("div", class_ = "MuiTypography-root MuiTypography-h4New mui-style-gz23my").text
# print(names)


