import pandas as pd 
from bs4 import BeautifulSoup 
from splinter import Browser
import os
import time
from selenium import webdriver



def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless = False)

def scrape():
    browser=init_browser()
    mars_data={}
    
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url) 
    html = browser.html
    soup = BeautifulSoup(html,"html.parser")
    title = soup.find('div', class_="content_title").text
    subtitle=soup.find('div', class_="article_teaser_body").text
    mars_data["News_Title"]=title
    mars_data["News_Paragraph"]=subtitle


    image_url="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)
    html=browser.html
    soup = BeautifulSoup(html,"html.parser")
    browser.find_by_id('full_image').first.click()
    time.sleep(10)
    html=browser.html
    soup = BeautifulSoup(html,"html.parser")
    featured_img_url = soup.find("img", class_="fancybox-image")['src']
    mars_data["Featured_Image"]=featured_img_url

    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twitter_url)
    time.sleep(5)
    browser.reload()
    time.sleep(5)
    html = browser.html
    time.sleep(5)
    soup = BeautifulSoup(html, 'html.parser')
    time.sleep(5)
    results = soup.find('div', class_= 'css-1dbjc4n').find_all('span', class_ ="css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0")
    weather_tweets=[]
    for tweet in results: 
        if "sol" in tweet.text:
            weather_tweets.append(tweet.text)
    mars_data["Weather"]=weather_tweets[0]

    url_table = "https://space-facts.com/mars/"
    tables = pd.read_html(url_table)
    df = tables[0]
    df.columns = ["measure", "value"]
    df.set_index('measure', inplace = True)
    html_table = df.to_html()
    html_table = html_table.replace("\n", "")
    mars_data["Mars_Facts"]=html_table
    
    
    high_res_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(high_res_url)
    html = browser.html
    soup = BeautifulSoup(html,"html.parser")
    hemispheres=["Cerberus", "Schiaparelli", "Schiaparelli", "Valles"]
    dictionaries=[]
    for hemisphere in hemispheres:
        browser.links.find_by_partial_text(hemisphere).click()
        browser.links.find_by_partial_text('Open').click()
        time.sleep(5)
        html = browser.html
        image = BeautifulSoup(html, "html.parser")
        img_url = image.find('img', class_="wide-image")['src']
        full_img_url="https://astrogeology.usgs.gov/" + img_url
        title=image.find('h2', class_="title").text
        dictionary={"title": title, "url": full_img_url}
        dictionaries.append(dictionary)
        browser.visit(high_res_url)
        html = browser.html
    mars_data["Hemispheres"]=dictionaries

    return mars_data




