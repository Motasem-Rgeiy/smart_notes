from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import chromedriver_binary
from selenium.webdriver.common.by import By
import trafilatura

def getNews():
    
    # Automatically fetches and uses matching ChromeDriver for Chrome 151
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))


    driver.get('https://news.ycombinator.com/')

    try:

        big_box = driver.find_element(By.ID, 'bigbox')
        table = big_box.find_element(By.TAG_NAME , 'table')
        rows = table.find_elements(By.CLASS_NAME , 'titleline')[:5]
    

        news_titles = []
     

        for title_obj in  rows:
                
                title = title_obj.find_element(By.TAG_NAME , 'a')
                link = title_obj.find_element(By.TAG_NAME , 'a').get_attribute('href')

                news_titles.append([title.text, link])

    #   print(len(elements))
    #  for ele in elements:
    #      print(ele.text)
        return news_titles
    except:
        print('Not able to find an element with that name.')

    finally:
         driver.quit()




def get_data(link):


    # Download and extract web page content
    downloaded = trafilatura.fetch_url(link)
    content = trafilatura.extract(downloaded)
    return content


