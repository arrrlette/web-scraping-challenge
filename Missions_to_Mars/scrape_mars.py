# Start by converting your Jupyter notebook into a Python script called scrape_mars.py with a function called scrape 
# that will execute all of your scraping code from above and return one Python dictionary containing all of the scraped data.

# Dependencies
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import os
from splinter import Browser
import time

def scrape():

    executable_path = {"executable_path": "chromedriver.exe"}
    browser = Browser("chrome", **executable_path, headless=False)
    title, paragraph = scrape_mars_news(browser)
    return{
        "News_Title": title,
        "Paragraph": paragraph,
        "Featured_Image": scrape_featured_image(browser),
        "Mars_Facts": scrape_mars_facts(browser),
        "Mars_Hemispheres": scrape_mars_hemispheres(browser)
    }

def scrape_mars_news(browser):

    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    time.sleep(3)

    html = browser.html
    soup = bs(html, 'html.parser')
    
    title = soup.find("div", class_="list_text").find("div", class_="content_title").text
    paragraph = soup.find('div', class_='article_teaser_body').text

    return title, paragraph


def scrape_featured_image(browser):

    imageurl = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'    
    browser.visit(imageurl)

    time.sleep(3)

    html = browser.html
    soup = bs(html, "html.parser")

    image = soup.find("a", class_="button fancybox")["data-fancybox-href"]
    featured_image_url = "https://www.jpl.nasa.gov" + image

    return featured_image_url

def scrape_mars_facts(browser):

    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)

    time.sleep(3)

    html = browser.html
    soup = bs(html, "html.parser")

    tables = pd.read_html(facts_url)[0]
    new_table = tables.rename(columns={0: 'Description', 1: "Mars"})
    final_table = new_table.set_index("Description")

    html_table = final_table.to_html(classes = 'table table-striped')
    html_table = html_table.replace('\n','')

    return html_table

def scrape_mars_hemispheres(browser):

    astro_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(astro_url)

    time.sleep(3)

    html = browser.html
    soup = bs(html, "html.parser")

    astro_results = soup.find_all('div', class_='item')

    dict_list = []

    # loop over results to get article data
    for result in astro_results:
        try:
            
            #loop through page and scrape image titles
            title = result.find('h3').text
            
            #click into next page to grab images
            browser.click_link_by_partial_text(title)
            
            html = browser.html
            soup = bs(html, 'html.parser')
            
            image_results = soup.find('div', class_="downloads").find('a')['href']
            
            #add titles and images to dictionary
            hem_dict = {
                'title': title,
                'img_url': image_results
            }
            
            #append dictionary to list
            dict_list.append(hem_dict)

                        
        except Exception as e:
            print(e)
            
        browser.back()

    return dict_list


