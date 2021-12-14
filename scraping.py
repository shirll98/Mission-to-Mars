
# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

# initiate the browser, create a data dictionary, end the webdriver and return the scraped
def scrape_all(): 
    # initiate headless driver for deployment 
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    # browser variable is set to Browser, name of parameter 
    news_title, news_paragraph = mars_news(browser)

    # run all scraping functions and store results in dictionary 
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
        "hemisphere_image_links": hemisphere_image_links(browser)
    }

# stop webdriver and return data 
broswer.quit()
return data 

### SCRAPING NEW TITLE AND PARAGRAPH 

def mars_news(browser): 
    # adding argument browser to the function tells python that 
    # Visit the Mars news site  
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # telling python to look for these elements, if there is an error Python will continue 
        # to run the remainder of the code, it will return nothing if there is an error 
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    except AttributeError: 
        return None, None 

    return news_title, news_p

### SCRAPING FOR IMAGES 

def featured_image(browser): 
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)
    
    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        # find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    
    return img_url

### Mars Facts
def mars_facts(): 
    try:
      # use 'read_html" to scrape the facts table into a dataframe
      df = pd.read_html('https://galaxyfacts-mars.com')[0]
   except BaseException:
      return None
    
    #assign columns and set index of dataframe 
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)
    
    # convert dataframe into HTML format, add bootstrap 
    return df.to_html()

# scrape for hemisphere data 
def hemis_information(browser): 
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    # 2. Create a list to hold the images and titles.
    hemisphere_image_links = []
    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    html = browser.html 
    images_soup = soup(html, 'html.parser')

    try: # handle errors 
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
    except BaseException: 
        return None
    # 4. Print the list that holds the dictionary of each image url and title.
    return hemisphere_image_links


if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())