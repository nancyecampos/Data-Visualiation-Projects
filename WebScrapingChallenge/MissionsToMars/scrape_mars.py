from bs4 import BeautifulSoup 
from splinter import Browser
import pandas as pd 
import requests 

# Initialize browser
def int_browser(): 
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

# Create Mission to Mars dictionary to import to Mongo
mars_info = {}

# MARS NEWS
def mars_news():
    try: 
        browser = int_browser()

        # Visit Nasa news url through splinter module
        url = 'https://mars.nasa.gov/news/'
        browser.visit(url)

        # HTML Object
        html = browser.html

        # Parse HTML 
        soup = BeautifulSoup(html, 'html.parser')


        # Retrieve the latest element that contains news title and news paragraph
        news_title = soup.find('div', class_='content_title').find('a').text
        news_p = soup.find('div', class_='article_teaser_body').text

        # Dictionary entry from MARS NEWS
        mars_info['news_title'] = news_title
        mars_info['news_paragraph'] = news_p

        return mars_info

    finally:

        browser.quit()

# FEATURED IMAGE
def mars_image():
    try: 

        # Initialize browser 
        browser = int_browser()

        # Visit Mars Space Images
        find_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(find_image_url)
        
        # Create HTML Object 
        html_image = browser.html

        # Parse through HTML
        soup = BeautifulSoup(html_image, 'html.parser')

        # Retrieve background-image url from style tag 
        featured_image_url  = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]

        # Website Url 
        site_url = 'https://www.jpl.nasa.gov'

        # Concatenate website url with scrapped route
        featured_image_url = site_url + featured_image_url

        # Display full link to featured image
        featured_image_url 

        # Dictionary entry from FEATURED IMAGE
        mars_info['featured_image_url'] = featured_image_url 
        
        return mars_info
    finally:

        browser.quit()

        

# Mars Weather 
def mars_weather():
    try: 

        # Initialize browser 
        browser = int_browser()

        # go to Mars Weather Twitter
        mars_weather = 'https://twitter.com/marswxreport?lang=en'
        browser.visit(mars_weather)

        # HTML Object 
        html_weather = browser.html

        # Parse HTML with Beautiful Soup
        soup = BeautifulSoup(html_weather, 'html.parser')

        # Find all elements that contain tweets
        recent_tweets = soup.find_all('div', class_='js-tweet-text-container')

        for tweet in recent_tweets: 
            weather_tweet = tweet.find('p').text
            if 'InSight' and 'gusting' in weather_tweet:
                print(weather_tweet)
                break
            else: 
                pass

        # Dictionary entry
        mars_info['weather_tweet'] = weather_tweet
        
        return mars_info
    finally:

        browser.quit()


# Mars Facts
def mars_facts():

    # Visit Mars facts url 
    mars_facts = 'http://space-facts.com/mars/'

    read_facts = pd.read_html(mars_facts)

    mars_df = read_facts[0]

    # Assign the columns `['Description', 'Value']`
    mars_df.columns = ['Category','Values']

    # Set the index 
    mars_df.set_index('Category', inplace=True)

    data = mars_df.to_html()

    # Dictionary entry from MARS FACTS
    mars_info['mars_facts'] = data

    return mars_info


# MARS HEMISPHERES


def mars_hemispheres():

    try: 

        # Initialize browser 
        browser = int_browser()

        # Visit hemispheres 
        mars_hem = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(mars_hem)

        # HTML Object + parse
        html_hem = browser.html

        soup = BeautifulSoup(html_hem, 'html.parser')

        # Retreive all items that contain mars hemispheres information
        items = soup.find_all('div', class_='item')

        # Create empty list for hemisphere urls 
        hem_img_urls = []

        # Store the main_ul 
        hem_main_url = 'https://astrogeology.usgs.gov' 

        # Loop through the items previously stored
        for i in items: 
            # Store title
            name = i.find('h3').text
            
            # Store link that leads to full image website
            img_url = i.find('a', class_='itemLink product-item')['href']
            
            # Visit the link that contains the full image website 
            browser.visit(hem_main_url + img_url)
            
            # HTML Object of individual hemisphere information website 
            img_html = browser.html
            
            # Parse HTML with Beautiful Soup for every individual hemisphere information website 
            soup = BeautifulSoup( img_html, 'html.parser')
            
            # Retrieve full image source 
            full_img_url = hem_main_url + soup.find('img', class_='wide-image')['src']
            
            # Append the retreived information into a list of dictionaries 
            hem_img_urls.append({"name" : name, "full_img_url" : full_img_url})

        mars_info['hem_img_urls'] = hem_img_urls

        
        # Return mars_data dictionary 

        return mars_info
    finally:

        browser.quit()