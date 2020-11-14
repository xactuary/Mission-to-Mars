# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd

# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': 'chromedriver'}
browser = Browser('chrome', **executable_path)

# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)
# Optional delay for loading the page - search for tag ul with attribute item_list and li with attribute slide
#  For example, ul.item_list would be found in HTML as <ul class=”item_list”>.
# tells is to wait a second to let the browser load
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

# set up the html parser
html = browser.html
news_soup = soup(html, 'html.parser')
# set up the variable to look for in the ul tag - this is the parent element . is for selecting classes
# CSS works from right to left - so will find li slide first and all elements inside that
slide_elem = news_soup.select_one('ul.item_list li.slide')
slide_elem.find("div", class_='content_title')

# Use the parent element to find the first `a` tag and save it as `news_title`
# the get_text chained to find pulls just the text and not the other html stuff. chained to find
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title

# Use the parent element to find the paragraph text
# find gets just the first class and attribute.  use find_all() to get all the classes and attributes
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p

#browser.quit()

# Visit URL
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)

# in HTML an id is a completely unique identifier.  so id=full image will be unique
# Find and click the full image button
full_image_elem = browser.find_by_id('full_image')
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
img_url_rel = img_soup.select_one('figure.lede a img').get("src")
img_url_rel
# get("src") pulls the image link which is only a partial link because doesn't include base URL

# Use the base URL to create an absolute URL
# use the f string because they are evaluated at run time which means the variable doesn't exist
# until it is run which is good for web scraping that gets updated
img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
img_url

# Use pandas to scrape whole table using .read_html()
# Pandas searches for and returns list of tables found in the HTML.
# the index 0 tells it to only pull the first table or the first item in the list
# then it turns it into a dataframe

df = pd.read_html('http://space-facts.com/mars/')[0]

# assign column names to new dataframe

df.columns=['description', 'value']

# puts the description column in the DF index.  inplace = true means that the updated index will remain in place without having 
# to reassign the dataframe to a new variable

df.set_index('description', inplace=True)
df

# pandas also has a way to convert the DF back into HTML with the .to_html() function
# this code can be copied into the HTML for a website and will produce the table. 
df.to_html()

browser.quit()

