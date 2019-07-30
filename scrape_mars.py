from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd

def init_browser():
    executable_path = {'executable_path':'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape_mars():
    browser = init_browser()
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    news_title = soup.find_all('div', class_='content_title')[0].text
    news_p = soup.find_all('div', class_='article_teaser_body')[0].text

    url = 'https://photojournal.jpl.nasa.gov/targetFamily/Mars'
    browser.visit(url)
    browser.click_link_by_partial_text('JPEG')
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    featured_image_url = soup.find_all('img')[0]['src']

    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    mars_weather = soup.find_all('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')[0].text.strip()

    url = 'https://space-facts.com/mars/'
    browser.visit(url)
    table = pd.read_html(url)
    df = table[1]
    df.columns = ['Attribute','Value']
    df.set_index('Attribute', inplace=True)
    mars_attributes = df.to_html(buf="mars_attributes.html")

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    browser.click_link_by_partial_text('Cerberus Hemisphere Enhanced')
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    cerberus = soup.find_all('img', class_='wide-image')[0]['src']
    cerberus_url = 'https://astrogeology.usgs.gov' + cerberus

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    browser.click_link_by_partial_text('Schiaparelli Hemisphere Enhanced')
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    schiaparelli = soup.find_all('img', class_='wide-image')[0]['src']
    schiaparelli_url = 'https://astrogeology.usgs.gov' + schiaparelli

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    browser.click_link_by_partial_text('Syrtis Major Hemisphere Enhanced')
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    srytis = soup.find_all('img', class_='wide-image')[0]['src']
    srytis_url = 'https://astrogeology.usgs.gov' + srytis

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    browser.click_link_by_partial_text('Valles Marineris Hemisphere Enhanced')
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    valles = soup.find_all('img', class_='wide-image')[0]['src']
    valles_url = 'https://astrogeology.usgs.gov' + valles

    hemisphere_image_urls=[
    {"title":"Valles Marineris Hemisphere","img_url":valles_url},
    {"title":"Cerberus Hemisphere","img_url":cerberus_url},
    {"title":"Schiaparelli Hemisphere","img_url":schiaparelli_url},
    {"title":"Syrtis Major Hemisphere","img_url":srytis_url}
    ]

    mars_data = {
        "News_Title":news_title,
        "News_Para": news_p,
        "Image": featured_image_url,
        "Weather":mars_weather,
        "Attributes":mars_attributes,
        "Valles":hemisphere_image_urls[0]['img_url'],
        "Cerberus":hemisphere_image_urls[1]['img_url'],
        "Schia":hemisphere_image_urls[2]['img_url'],
        "Syrtis":hemisphere_image_urls[3]['img_url']
    }

    return mars_data