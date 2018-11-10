import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
from datetime import datetime


# Initialize browser
def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    #executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)


# Function to scrape Mars information
def scrape():
    # initiate a dictionary to store all scraped data
    mars_data = {}
    # Initialize browser
    browser = init_browser()

    # Visit the nasa mars site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Scrape page into soup
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # Find the latest news title and content
    # NASA Mars News
    title = soup.find_all('div', class_='content_title')
    news_title = title[0].a.text
    content = soup.find_all('div', class_='article_teaser_body')
    news_p = content[0].text

    #add key:value pair to dictionary
    mars_data['news_title'] = news_title
    mars_data['news_content'] = news_p

    
    # JPL Mars Space Images - Featured Image
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    article = soup.find('article', class_='carousel_item')
    href = article['style'].replace("background-image: url('","").replace("');","").strip()
    url = 'https://www.jpl.nasa.gov'
    featured_image_url  = url +  href

    #add key:value pair to dictionary
    mars_data['featured_image_url'] = featured_image_url

    # Mars Weather
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    div = soup.find_all('div', class_='js-tweet-text-container')
    para = div[0].find('p')
    mars_weather = para.text

    #add key:value pair to dictionary
    mars_data['mars_weather'] = mars_weather


    # Mars Facts

    url = "http://space-facts.com/mars/"
    tables = pd.read_html(url)

    df = tables[0]

    df.columns = ['Profile', 'Value']
    df['Profile'] = df['Profile'].str.replace(":", "")

    i = 0
    dataset = []

    while i < len(df):
        datarow = {}
        datarow['Profile'] = df['Profile'][i]
        datarow['Value'] = df['Value'][i]
        dataset.append(datarow)
        i += 1

# add key:value [list of dictionary of 2 columns of data]
    mars_data['table'] = dataset


    # Mars Hemispheres

    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    div = soup.find_all('div', class_='description')
    links = []
    targeturl = 'https://astrogeology.usgs.gov'
    for d in div:
        h = d.find('a')
        link = targeturl + h['href']
        links.append(link)
    #print(link)

    hemisphere_image_urls = []

    img_url = {}

    for x in range(4):
        dict = {}
    #print(links[x])
        browser.visit(links[x])
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
    
        h2 = soup.find('h2', class_='title')
        div = soup.find('div', class_='downloads')
        img_urls = div.find_all('a')
    #print(h2.text.replace('Enhanced', ''))
    #print(img_urls[2]['href'])
        dict['title']= h2.text.replace('Enhanced', '')
        dict['img_url'] = img_urls[0]['href']
        hemisphere_image_urls.append(dict)

#add key:value pair to dictionary
    mars_data['hemisphere_image_urls'] = hemisphere_image_urls


    # Return results
    return mars_data



