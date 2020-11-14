# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt

def scrape_all():
   # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path="chromedriver", headless=True)
    news_title, news_paragraph = mars_news(browser)
    # Run all scraping functions and store results in dictionary
    data = {
      "news_title": news_title,
      "news_paragraph": news_paragraph,
      "featured_image": featured_image(browser),
      "facts": mars_facts(),
      "last_modified": dt.datetime.now()
    }  
    # Stop webdriver and return data
    browser.quit()
    return data
# Set the executable path and initialize the chrome browser in splinter
#executable_path = {'executable_path': 'chromedriver'}
#browser = Browser('chrome', **executable_path)

def mars_news(browser):
# Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
# Optional delay for loading the page - search for tag ul with attribute item_list and li with attribute slide
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

# set up the html parser
    html = browser.html
    news_soup = soup(html, 'html.parser')

# Add try/except for error handling
    try:
        slide_elem = news_soup.select_one("ul.item_list li.slide")
#        slide_elem.find("div", class_='content_title')

# Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find("div", class_="content_title").get_text()

# Use the parent element to find the paragraph text
# find gets just the first class and attribute.  use find_all() to get all the classes and attributes
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
#    news_p
    except AttributeError:
        return None, None

    return news_title, news_p

def featured_image(browser):  
# Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

# in HTML an id is a completely unique identifier.  so id=full image will be unique
# Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')[0]
    full_image_elem.click()

# splinter can search for HTML elements by text these are built in methods
# Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.links.find_by_partial_text('more info')
    more_info_elem.click()

# Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

# the value of the src will be different every time the page is updated, 
# so we can't simply record the current value
# The most recent image will be in  <figure /> and <a /> tags have the image link nested within them.
# Find the relative image url
# figure.lede references the <figure /> tag and its class, lede. a and then img is the next tag inside the figure tag

# Add try/except for error handling
    try:
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")

# get("src") pulls the image link which is only a partial link because doesn't include base URL
    except AttributeError:
        return None
# Use the base URL to create an absolute URL
# use the f string because they are evaluated at run time which means the variable doesn't exist
# until it is run which is good for web scraping that gets updated
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
    return img_url

# Use pandas to scrape whole table using .read_html()
# Pandas searches for and returns list of tables found in the HTML.
# the index 0 tells it to only pull the first table or the first item in the list
# then it turns it into a dataframe
def mars_facts():
    # Add try/except for error handling
    try:
        df = pd.read_html('http://space-facts.com/mars/')[0]
    except BaseException:
        return None
# assign column names to new dataframe

    df.columns=['Description', 'Mars']

# puts the description column in the DF index.  inplace = true means that the updated index will remain in place without having 
# to reassign the dataframe to a new variable

    df.set_index('Description', inplace=True)

# Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())

