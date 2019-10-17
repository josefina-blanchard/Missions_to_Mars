#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def scrape_all():


    # In[1]:


    #Set dependencies
    from bs4 import BeautifulSoup as bs
    import requests
    import pymongo
    from pymongo import MongoClient
    from splinter import Browser
    import pandas as pd


    # # NASA Mars News

    # In[6]:


    #Set the URL that will be scrapped
    url = "https://mars.nasa.gov/news"


    # In[7]:


    #Retrieve results
    results = requests.get(url)
    results


    # In[ ]:


    #To look at the tags used in the site
    #results.text  


    # In[8]:


    #Create the BeautifulSoup object and parse it
    soup = bs(results.text, "html.parser")


    # In[9]:


    #Look at the pretty print to see indented tags
    print(soup.prettify())


    # In[10]:


    #Collect the latest news and paragraph text from each article -- Use the Inspect tool for easy identification
    #Drilling down into tags
    title_tags = soup.find_all("div", class_="content_title")
    #title_tags


    # In[11]:


    #Keep drilling down in one item to find the correct query
    title_check = title_tags[0]
    title_check


    # In[12]:


    #setting variable syntax
    title_check.text.strip()


    # In[13]:


    #drilling down on elements to find article description
    body_tags = soup.find_all("div", class_="rollover_description_inner")
    body_tags[0].text.strip()


    # # JPL Mars Space Images - Featured Image

    # In[2]:


    #Declaring the executable path and browser
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)


    # In[14]:


    #Setting the URL for the next page and the execution/connection
    url2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url2)


    # In[15]:


    #This html is for the original website, the browser updates, not the soup
    html = browser.html
    soup2 = bs(html, "html.parser")
    browser.is_text_not_present("FULL IMAGE", wait_time=10)
    browser.click_link_by_partial_text("FULL IMAGE")


    # In[16]:


    browser.is_text_not_present("more info", wait_time=10)
    browser.click_link_by_partial_text("more info")


    # In[17]:


    #Updating the soup to get the latest html where I can look for the tags related to that page. 
    soup3 = bs(browser.html, "lxml")
    soup3.find("img", class_="main_image")['src']


    # In[18]:


    image = soup3.find("img", class_="main_image")['src']
    featured_image_url = "https://www.jpl.nasa.gov" + image
    print(featured_image_url)


    # # Mars Weather

    # In[19]:


    #Setting URL for next item on project
    url3 = "https://twitter.com/marswxreport?lang=en"


    # In[20]:


    results2 = requests.get(url3)
    soup4 = bs(results2.text, "html.parser")
    print(soup4.prettify())


    # In[21]:


    soup4.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text


    # In[22]:


    mars_weather = soup4.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    mars_weather


    # # Mars Facts

    # In[23]:


    #Use the read_html function in Pandas to automatically scrape any tabular data from a page
    url4 = "https://space-facts.com/mars/"


    # In[24]:


    tables = pd.read_html(url4)
    tables


    # In[25]:


    type(tables)


    # In[26]:


    df = tables[0]
    df.columns = ["Mars - Earth Comparison", "Mars", "Earth"]
    df.head()


    # In[27]:


    #Generate HTML tables from the DataFrame
    html_table = df.to_html()
    html_table


    # In[28]:


    #Cleaning up the table
    html_table.replace('\n', '')


    # In[29]:


    #Saving the table to a file for practice
    df.to_html("table.html")


    # # Mars Hemispheres

    # In[3]:


    url5 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"


    # In[4]:


    results3 = requests.get(url5)
    soup5 = bs(results3.text, "html.parser")
    #Print results to start digging into the tabs/html
    print(soup5.prettify())


    # In[30]:


    #Looking into tags to extract the title.
    hemispheres = soup5.find_all("div", class_="description")
    cerberus = hemispheres[0].text.strip()
    schiaparelli = hemispheres[1].text.strip()
    syrtis_major = hemispheres[2].text.strip()
    valles_marineris = hemispheres[3].text.strip()
    valles_marineris


    # In[31]:


    #Extracting the image for each hemisphere
    hemispheres_img = soup5.find_all("img", class_="thumb")
    hemispheres_img[0]["src"]


    # In[32]:


    #Setting the URL for each image
    himg0 = "https://astrogeology.usgs.gov" + hemispheres_img[0]["src"]
    print(himg0)


    # In[33]:


    himg1 = "https://astrogeology.usgs.gov" + hemispheres_img[1]["src"]
    himg2 = "https://astrogeology.usgs.gov" + hemispheres_img[2]["src"]
    himg3 = "https://astrogeology.usgs.gov" + hemispheres_img[3]["src"]


    # In[34]:


    #Creating dictionary for hemisphere titles and images
    hemisphere_image_urls = [
        {"title": cerberus, "image_url": himg0},
        {"title": schiaparelli, "image_url": himg1},
        {"title": syrtis_major, "image_url": himg2},
        {"title": valles_marineris, "image_url": himg3}]
    print(hemisphere_image_urls)


    # In[40]:


    t1 = title_check.text.strip()
    t2 = body_tags[0].text.strip()
    t3 = featured_image_url
    t4 = mars_weather
    t5 = html_table
    t6 = hemisphere_image_urls

    all_dict = {
        "NASA_Mars_News":[t1,t2],
        "Mars_Space_Images":t3,
        "Mars_Weather":t4,
        "Mars facts":t5,
        "Mars Hemispheres":t6
    }   
    # In[41]:
    return all_dict

