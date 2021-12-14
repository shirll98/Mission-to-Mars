
# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# ### Visit the NASA Mars News Site

# Visit the mars nasa news site
url = 'https://redplanetscience.com/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')



slide_elem.find('div', class_='content_title')



# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title



# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### JPL Space Images Featured Image


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)



# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()



# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup




# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel



# Use the base url to create an absolute url
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### Mars Facts



df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.head()




df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df



df.to_html()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres



# 1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

browser.visit(url)



# 2. Create a list to hold the images and titles.
hemisphere_image_links = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
html = browser.html 
images_soup = soup(html, 'html.parser')

#loop through the full resolution image URL, click the link, find the sample image anchor tag, get the href 
images = len(images_soup.select("div.item"))

for i in range(images): 
    results = {} 
    link = images_soup.select("div.description a")[i].get('href') 
    browser.visit(f'https://astrogeology.usgs.gov{link}')
    
    # parse the html page with soup 
    html = browser.html 
    image_soup_1 = soup(html, 'html.parser') 
    #get full image link 
    image_link = image_soup_1.select_one("h2.title").get_text()
    
    results = {
        'image_link' : image_link, 
        'title': image_title
    }
    hemisphere_image_links.append(results) # append results to hemisphere url list 
    
    browser.back() # goes back to main page 




# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_links




# 5. Quit the browser
browser.quit()






