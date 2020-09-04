def scrape():
#declare dependencies
    from splinter import Browser
    from bs4 import BeautifulSoup as bs
    import time
    import pandas as pd
    import requests
    import pymongo

    #declare chrome driver excecutable path
   
    executable_path = {'executable_path': "C:/chrometest/chromedriver.exe"}
    browser = Browser('chrome', **executable_path, headless=False)
    mars_dict = {}
    #pass the url 
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    try:
        step1 = soup.select_one('ul.item_list li.slide')
        #find news title
        news_title = step1.find("div", class_="content_title").text
        #find news paragraph
        news_paragraph= step1.find("div", class_="article_teaser_body").text
    except:
        return None, None


    # JPL Mars Space Images - Featured Image

    #declare chrome driver excecutable path
    # executable_path = {'executable_path': '/Users/hello/Downloads/chromedriver_win32/chromedriver'}
    #     # executable_path = {'executable_path': "C:/chrometest/chromedriver.exe"}
    # browser = Browser('chrome', **executable_path, headless=False)

# Featured Image URL

#     #Scrape first jpl Nasa page
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    #this will make the browser scrape page
    html = browser.html
    soup = bs(html, 'html.parser')

#     #This makes the browser click button or link
    browser.click_link_by_partial_text('FULL IMAGE')
    
    time.sleep(3)
    #Scrape second NASA page
    browser.click_link_by_partial_text('more info')
    time.sleep(3)

  
    html = browser.html
    soup2 =  bs(html, 'html.parser')

    # findimg= soup2.find('img', class_='fancybox-image')['src']
    image_url = soup2.find('figure', class_='lede')
    findimg = image_url.a["href"]
       
    featured_image_url= "https://www.jpl.nasa.gov"+ findimg
      
#  # # Mars Facts
#     import pandas as pd
    url = "https://space-facts.com/mars/"

    tables = pd.read_html(url)
    MarsPlanetProfile =  tables[0]
   
    # Rename columns
    renamed_marsfacts_df = MarsPlanetProfile.rename(columns={0:"Description", 1:"Value"})
    # MarsPlanetProfile.columns = ['Description', 'Value']
    # Convert DF to html
    MarsPlanet = renamed_marsfacts_df.to_html()
    # Convert DF to HTML string.
    # MarsPlanet = MarsPlanetProfile.to_html(header=True, index=True)
   


    # # # Mars Hemispheres

    # #declare chrome driver excecutable path

    # # executable_path = {"executable_path": "C:\chrometest\chromedriver.exe"}
    # # browser = Browser("chrome", **executable_path, headless=False)
    # url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    # browser.visit(url)
    # html = browser.html
    # soup = bs(html,'html.parser')
    # # results = soup.find_all("a", class_= "itemLink product-item")
    # partialurl= "https://astrogeology.usgs.gov"

    # # Locate all hemisphers and add to a list.
    # hemisphere_url = soup.find_all("div", class_="item")

    # # Create empty list for each Hemisphere URL.
    # hems_url = []

    # for hems in hemisphere_url:
    # #browser.visit(partialurl + x['href'])
    # #time.sleep(10)
    # #browser.links.find_by_partial_text('Sample')
    #     hemi_url = hems.find('a')['href']
    #     hems_url.append(hemi_url)

    # # browser.quit()

    # hemisphere_image_urls = []

    # for hem in hems_url:
    #     hem_isphere_url = partialurl + hem
    #     print(hem_isphere_url)
        
    #     #Initialize browser
    #     browser.visit(hem_isphere_url)
        
    #     html = browser.html
    #     soup3 = bs(html, "html.parser")

    #     # Locate each title and save for modification
    #     each_title = soup3.find("h2", class_="title").text
        
    #     # Remove Enhanced.
    #     title = each_title.split('Enhanced')[0]
        
    #     # Locate all full images in 4 Hemisphere URLs.
    #     img_url = soup3.find("li").a['href']
        
    #     # Append both title and img_url to 'hemisphere_image_url'.
    #     hemisphere_image_urls.append({'title': title, 'img_url': img_url})
        
    #     # browser.quit()

   
    # # Mars Data Dictionary  MongoDB
    # Create empty dictionary for all Mars Data.
       
# Mars Hemispheres
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    response = requests.get(url)
    soup = bs(response.text, 'html.parser').find_all("a",class_ = "itemLink product-item")
    hemi_titles = []
    for i in soup:
        title = i.find("h3").text
        # link= i["href"]
        hemi_titles.append(title)
    

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    hemisphere_image_urls = []
    for x in range(len(hemi_titles)):
        try:
            browser.click_link_by_partial_text(hemi_titles[x])
        except:
            browser.find_link_by_text('2').first.click()
            browser.click_link_by_partial_text(hemi_titles[x])
        html = browser.html
        soup2 = bs(html, 'html.parser')
        hemi_soup = soup2.find('div', 'downloads')
        hemi_url = hemi_soup.a['href']
        hemisphere_image_urls.append(hemi_url)
        browser.back()

    # Append news_title and news_paragraph to mars_data.
    mars_dict['news_title'] = news_title
    mars_dict['news_paragraph'] = news_paragraph
    # Append featured_image_url to mars_data.
    mars_dict['featured_image_url'] = featured_image_url
    # # Append mars_facts to mars_data.
    mars_dict['MarsPlanet'] = MarsPlanet
    # Append hemisphere_image_urls to mars_data.
    mars_dict['hemisphere_image_urls'] = hemisphere_image_urls

    return mars_dict



