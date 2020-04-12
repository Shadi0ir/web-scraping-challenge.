#!/usr/bin/env python
# coding: utf-8

# In[63]:


# Import Splinter, BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup
#if the elements dosenot exist
from splinter.exceptions import ElementDoesNotExist 
import requests
import pandas as pd


# In[64]:


#spliter call out Chromedriver to open the link
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)


# In[73]:


# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)
html = browser.html
soup = BeautifulSoup(html, 'html.parser')
soup


# NASA Mars News

# In[80]:


results=soup.find_all('div', class_='list_text')
results


# In[81]:


#results = soup.find_all('li', class_="slide")

for result in results:
    try:
        news_Title =result.find('div', class_='content_title').get_text()
        paragraph = result.find("div", class_='article_teaser_body').get_text()
                
        if (news_Title and paragraph):
            print('-'*12)
            print(news_Title)
            print(paragraph)
        
    except AttributeError as e:
        print(e)


# JPL Mars Space Images - Featured Image

# In[82]:


url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)


# In[83]:


# Find and click the full image button
image_element = browser.find_by_id('full_image')
image_element.click()


# In[84]:


# Find the more info button and click that
browser.is_element_present_by_text('more info', wait_time=1)
more_info_elem = browser.find_link_by_partial_text('more info')
more_info_elem.click()


# In[85]:


html = browser.html
soup = BeautifulSoup(html, 'html.parser')
soup


# In[26]:


# find the relative image url
img_url_rel = soup.select_one('figure.lede a img').get("src")
img_url_rel


# In[27]:


# Use the base url to create an absolute url
img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
img_url


# Mars Weather

# In[28]:


url = 'https://twitter.com/MarsWxReport/with_replies?lang=en'
browser.visit(url)


# In[29]:


html = browser.html
soup = BeautifulSoup(html, 'html.parser')
soup


# In[30]:


weather=soup.find_all("span", class_='tweet')

weather=soup.find_all("span", class_='css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0')

weather


# Mars Facts

# In[31]:


url = 'https://space-facts.com/mars/'
browser.visit(url)


# In[32]:


tables = pd.read_html(url)
tables


# In[33]:


#Slice the table
df = tables[0]
df


# In[34]:


rename_df= df.rename(columns={
    0: "Description" , 
    1: "Value",
})

rename_df


# In[35]:


rename_df.set_index('Description', inplace=True)
rename_df.head()


# DataFrames as HTML

# In[36]:


html_table = rename_df.to_html()
html_table


# In[37]:


html_table.replace('\n', '')


# In[38]:


df.to_html('table.html')


# Mars Hemispheres

# In[39]:


url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)


# In[40]:


hemisphere_image_urls = []

# First, get a list of all of the hemispheres
links = browser.find_by_css("a.product-item h3")

# Next, loop through those links, click the link, find the sample anchor, return the href
for i in range(len(links)):
    hemisphere = {}
    
    # We have to find the elements on each loop to avoid a stale element exception
    browser.find_by_css("a.product-item h3")[i].click()
    
    # Next, we find the Sample image anchor tag and extract the href
    sample_elem = browser.find_link_by_text('Sample').first
    hemisphere['img_url'] = sample_elem['href']
    
    # Get Hemisphere title
    hemisphere['title'] = browser.find_by_css("h2.title").text
    
    # Append hemisphere object to list
    hemisphere_image_urls.append(hemisphere)
    
    # Finally, we navigate backwards
    browser.back()


# In[41]:


hemisphere_image_urls


# In[ ]:




