
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

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())