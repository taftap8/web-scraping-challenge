    
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import time

def scrape():
    #set up executable path and initiate browser
    executable_path = {"executable_path": "chromedriver.exe"}
    browser = Browser("chrome", **executable_path, headless=False)

    #mars article data
    #mars site to visit
    mars_url = "https://mars.nasa.gov/news/"
    browser.visit(mars_url)
    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    #bring back variables
    #first article title
    news_title = soup.find('ul', class_="item_list").find('li', class_="slide").find('div', class_='content_title').text

    #first article text
    news_p = soup.find('ul', class_="item_list").find('li', class_="slide").find('div', class_='article_teaser_body').text
    
    #Grab Mars Data
    #set up executable path and visit url - click through to full image
    images_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(images_url)
    browser.click_link_by_partial_text('FULL IMAGE')
    browser.click_link_by_partial_text('more info')

    #scrape page details
    html = browser.html
    soup = BeautifulSoup(html, 'lxml')
    results = soup.find('section',class_='content_page module').find('figure',class_='lede').find('a')['href']
    featured_image_url = {'url' : 'https://www.jpl.nasa.gov' + results}

    #Mars Facts
    #facts site to visit
    facts_url = "https://space-facts.com/mars/"
    #scrap all facts
    fact_table = pd.read_html(facts_url)
    fact_df = fact_table[0]
    table_html = fact_df.to_html(header=False, index=False)

    #Mars Hemisphere
    

    mars_data ={
        "News_Title": news_title,
        "News_Paragraph": news_p,
        "Featured_Image": featured_image_url,
        "Mars_Facts": table_html
            }

    browser.quit()
    return mars_data




    # Store data in a dictionary
    costa_data = {
        "sloth_img": sloth_img,
        "min_temp": min_temp,
        "max_temp": max_temp
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return costa_data
