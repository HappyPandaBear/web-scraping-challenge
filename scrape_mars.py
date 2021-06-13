from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import requests
import time
from webdriver_manager.chrome import ChromeDriverManager


def init_browser():

    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)
mars_dict = {}

def news():

        browser = init_browser()
        news_url = 'https://redplanetscience.com/'
        browser.visit(news_url)
        html = browser.html
        soup = bs(html, 'html.parser')
        title = soup.find("div", class_ = "content_title").text
        paragraph = soup.find("div", class_ = "article_teaser_body").text
        mars_dict['news_title'] = title
        mars_dict['news_paragraph'] = paragraph

        return mars_dict

def image():

        browser = init_browser()
        space_url = 'https://spaceimages-mars.com/'
        browser.visit(space_url)
        image_html = browser.html
        soup = bs(image_html, 'html.parser') 
        image_url  = soup.find_all('img')[1]["src"]
        featured_image_url = space_url + image_url
        mars_dict['featured_image_url'] = featured_image_url 

        return mars_dict

def facts():

        browser = init_browser()
        facts_url = 'https://galaxyfacts-mars.com/'
        browser.visit(facts_url)
        tables = pd.read_html(facts_url)
        mars_df = tables[1]
        mars_df.columns = ['Description', 'Value']
        html_table = mars_df.to_html(table_id="html_tbl_css",justify='left',index=False)
        mars_dict['tables'] = html_table

        return mars_dict

def hemispheres():

        browser = init_browser()
        hemispheres_url = 'https://marshemispheres.com/'
        browser.visit(hemispheres_url)
        html_hemispheres = browser.html
        soup = bs(html_hemispheres, 'html.parser')
        items = soup.find_all('div', class_='item')
        hemispheres_image_urls = []
        hemispheres_main_url = 'https://marshemispheres.com/' 

        for i in items: 

            title = i.find('h3').text
            partial_img_url = i.find('a', class_='itemLink product-item')['href']
            browser.visit(hemispheres_main_url + partial_img_url)
            partial_img_html = browser.html
            soup = bs( partial_img_html, 'html.parser')
            img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
            hemispheres_image_urls.append({"title" : title, "img_url" : img_url})
        mars_dict['hemisphere_image_urls'] = hemispheres_image_urls

        return mars_dict