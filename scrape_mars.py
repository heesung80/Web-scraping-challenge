import pandas as pd
from bs4 import BeautifulSoup
import requests
import pymongo
from splinter import Browser
from bs4 import BeautifulSoup
import time

def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    # NASA Mars News #
    browser = init_browser()
    news_url="https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(news_url)
    time.sleep(5)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    
    
    t_results = soup.find_all('div', class_='content_title')
    title = t_results[0].text
    p_results = soup.find_all('div', class_='article_teaser_body')
    p_text = p_results[0].text

   
    
    #JPL Mars Space Images -Featured Image#
    
    browser = init_browser()
    url="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    results = soup.find_all('div', class_='carousel_items')
    for result in results:
        image_url = result.a['data-fancybox-href']
        featured_image_url = f"https://www.jpl.nasa.gov{image_url}"
        
        
    #Mars Weather#
    
    browser = init_browser()
    mars_url="https://twitter.com/marswxreport?lang=en"
    browser.visit(mars_url)
    time.sleep(5)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    tweet=soup.find_all('div', attrs={'data-testid':'tweet'})
    tweet_list_text = [x.text for x in tweet]
    df=pd.DataFrame({'tweet':tweet_list_text})
    text_df =df[df['tweet'].str.contains('InSight')]
    text_list =text_df['tweet'].tolist()
    text_new = ' '.join(text_list[0].split()[3:])
    #print(f"Mars_weather = {text_new}")
    
    #Mars Fact#
    
    browser = init_browser()
    mars_facts_url="https://space-facts.com/mars/"
    browser.visit(mars_facts_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    facts_tables = pd.read_html(mars_facts_url)
    mars_facts_tables=facts_tables[0]
    mars_facts_tables.columns=['Description', 'Value']
    mars_facts_tables
    html_table = mars_facts_tables.to_html()


    #Mars Hemisphere#
    
    browser = init_browser()
    url_hemisphere="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url_hemisphere)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    hemispheres = soup.find_all('div', class_="item")
    link_list =[]
    for h in hemispheres:
        link=h.a['href']
        full_link = ("https://astrogeology.usgs.gov/"+link)
        link_list.append(full_link)
        
    Total_list=[]
    hemisphere_title_list =[]
    img_list =[]
    for link in link_list:
        response = requests.get(link)
        #print(response)
        soup = BeautifulSoup(response.text, 'html.parser')
        #print(soup.prettify())
        new_link = soup.find('li').\
        find('a', attrs={'target':'_blank'})['href']
        title=soup.find('h2',class_='title').text
        hemisphere_title_list.append(title)
        img_list.append(new_link)
        hemisphere_dic={}
        hemisphere_dic['Title'] = title
        hemisphere_dic['Image_url'] = new_link
        Total_list.append(hemisphere_dic)

    #Make a dictionary to load to Mongodb
    mars_data = {
        "Mars_news_title":title,
        "Mars_news_text":p_text,
        "Mars_feature_image_url":featured_image_url,
        "Mars_weather":text_new,
        "Mars_fact":html_table,
        "Mars_hemisphere":Total_list
        }
    print(mars_data)
    browser.quit()
    
    return mars_data
    
    


