# declare dependencies
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import requests
import pymongo

def init_browser():
    executable_path = {"executable_path": "C:\chrometest\chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)
    
def scrape():
    browser = init_browser()
    # pass the url
    browser = init_browser()
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    step1 = soup.find("ul", class_="item_list")
    step2 = step1.find("li", class_="slide")

    # find news title
    news_title = step2.find("div", class_="content_title").text
    news_title
    # find news paragraph
    news_paragraph = step2.find("div", class_="article_teaser_body").text
    news_paragraph

    # JPL Mars Space Images - Featured Image
    # declare chrome driver excecutable path
    browser = init_browser()
    # Scrape first jpl Nasa page
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    # this will make the browser scrape page
    html = browser.html
    soup = bs(html, 'html.parser')
    # This makes the browser click button or link
    browser.click_link_by_partial_text('FULL IMAGE')
    # Scrape second NASA page
    browser = init_browser()
    html = browser.html
    soup2 = bs(html, 'html.parser')
    browser.click_link_by_partial_text('more info')

    findimg = soup2.find('img', class_='fancybox-image')['src']
    findimg

    featured_image_url = "https://www.jpl.nasa.gov" + findimg
    featured_image_url


    # Mars Facts
    url = "https://space-facts.com/mars/"
    tables = pd.read_html(url)
    tables

    # Data type
    type(tables)

    MarsPlanetProfile = tables[0]
    MarsPlanetProfile

    # Rename columns
    MarsPlanetProfile.columns = ['Description', 'Value']

    # Convert DF to html
    MarsPlanetProfile.to_html('mars_facts.html', index=False)

    # Convert DF to HTML string.
    MarsPlanet = MarsPlanetProfile.to_html(header=True, index=True)
    print(MarsPlanet)

    # Mars Hemispheres

    # declare chrome driver excecutable path
    browser = init_browser()
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    html = browser.html
    soup = bs(response.text, 'html.parser')
    results = soup.find_all("a", class_="itemLink product-item")
    partialurl = "https://astrogeology.usgs.gov"

    # Locate all hemispheres and add to list
    hemisphere_url = soup.find_all("div", class_="item")

    # Create empty list for each Hemisphere URL.
    hems_url = []
    for hems in hemisphere_url:
        hemi_url = hems.find('a')['href']
        hems_url.append(hemi_url)
    browser.quit()
 
    hemisphere_image_urls = []
    for hem in hems_url:
        hem_isphere_url = partialurl + hem
        print(hem_isphere_url)

        # Initialize browser
        browser = init_browser()
        browser.visit(hem_isphere_url)
        html = browser.html
        soup3 = bs(html, "html.parser")

        # Locate each title and save for modification
        each_title = soup3.find("h2", class_="title").text

        # Remove Enhanced.
        title = each_title.split('Enhanced')[0]

        # Locate all full images in 4 Hemisphere URLs.
        img_url = soup3.find("li").a['href']

        # Append both title and img_url to 'hemisphere_image_url'.
        hemisphere_image_urls.append({'title': title, 'img_url': img_url})
        browser.quit()

    print(hemisphere_image_urls)

    # Mars Data Dictionary  MongoDB
    # Create empty dictionary for all Mars Data.

    mars_dict = {}
    # Append mars related data to dictionary.
    mars_dict['news_title'] = news_title
    mars_dict['news_paragraph'] = news_paragraph
    mars_dict['featured_image_url'] = featured_image_url
    mars_dict['MarsPlanet'] = MarsPlanet
    mars_dict['hemisphere_image_urls'] = hemisphere_image_urls
    mars_dict