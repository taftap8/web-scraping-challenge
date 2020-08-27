
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import os
import time


def scrape():
    # set up executable path and initiate browser
    executable_path = {"executable_path": "chromedriver.exe"}
    browser = Browser("chrome", **executable_path, headless=False)

    # START mars article data ----------------------------------------------------------------------------
    # mars site to visit
    mars_url = "https://mars.nasa.gov/news/"
    browser.visit(mars_url)
    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # bring back variables
    # first article title
    news_title = soup.find('ul', class_="item_list").find(
        'li', class_="slide").find('div', class_='content_title').text

    # first article text
    news_p = soup.find('ul', class_="item_list").find(
        'li', class_="slide").find('div', class_='article_teaser_body').text
    #END Mars Articles ------------------------------------------------------------------------------------

    # Grab Mars Featured Image ---------------------------------------------------------------------------
    # set up executable path and visit url - click through to full image
    images_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(images_url)
    browser.click_link_by_partial_text('FULL IMAGE')
    browser.click_link_by_partial_text('more info')

    # scrape page details
    html = browser.html
    soup = BeautifulSoup(html, 'lxml')
    results = soup.find('section', class_='content_page module').find(
        'figure', class_='lede').find('a')['href']
    featured_image_url = {'url': 'https://www.jpl.nasa.gov' + results}
    #END featured image ----------------------------------------------------------------------------------

    # START Mars Fact table -----------------------------------------------------------------------------
    # facts site to visit
    facts_url = "https://space-facts.com/mars/"
    # scrap all facts
    fact_table = pd.read_html(facts_url)
    fact_df = fact_table[0]
    table_html = fact_df.to_html(header=False, index=False)
    #END fact table -------------------------------------------------------------------------------------

    #START Mars Hemisphere ------------------------------------------------------------------------------
    # URL
    hemi_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemi_url)
    time.sleep(1)
    # scrape page details
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    # results from page for images
    mars_results = soup.find_all('div', class_='description')


    # create list to store hemisphere details
    hemisphere_list = []

    # loop through results to add to list
    for result in mars_results:
        try:

            # scrape title
            title = result.find('h3').text
            browser.click_link_by_partial_text(title)
            # browser.click_link_by_partial_text('Sample')

            time.sleep(3)
            new_browser = browser.html
            soup = BeautifulSoup(new_browser, 'html.parser')

            # scrape page details
            #image_results = soup.find('img')
            mars_hemisphere_image = soup.find('div', class_="downloads").find('a')
            url = mars_hemisphere_image['href']

            # create dictionary
            hemisphere_dict = {
                "Title": title,
                "URL": url
                }

            hemisphere_list.append(hemisphere_dict)

            # for title in hemisphere_dict:
            # print(title)
            browser.back()
        except Exception as e:
            print(e)
    #END MARS Hemispheres -----------------------------------------------------------------

    #Store data in a dictionary
    mars_data = {
        "News_Title": news_title,
        "News_Paragraph": news_p,
        "Featured_Image": featured_image_url,
        "Mars_Facts": table_html,
        "Hemispheres": hemisphere_list}

    browser.quit()
    return mars_data

    # Close the browser after scraping
    browser.quit()

