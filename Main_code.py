import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests 

###Function to get data from The Real Estate Collection for Miami
listings =[]
def get_data(pages,bedrooms,bathrooms):
    url=f"https://www.therealestatecollection.com/miami-ppc.php?reg=&_ppc=condos%20for%20sale%20miami&gclid=CjwKCAjwpKyYBhB7EiwAU2Hn2erKpNUcAin2ORexEKtUGqOD_fKqEWmHjLd6gA-IxpS92829zChwCBoCt98QAvD_BwE&p={pages}&minimum_bedrooms={bedrooms}&minimum_bathrooms={bathrooms}#refine_bar"
    page = requests.get(url)
    soup = BeautifulSoup(page.content,'html.parser')
    all_data = soup.find_all('a',{'class':'teaser teaser__card'})
    for i in all_data:
        data = {
            'Price' : int(i.find('span', {'class' : 'teaser__price__title'}).text.replace('$','').replace(',','')),
            'Address' : i.find('h4', {'class': 'teaser__address'}).text.replace('\n','').replace(' ','').replace(',',''),
            'BedRooms' : int(i.select_one(" div.teaser__content.clear > small > span:nth-child(1) ").get_text().replace('\n','').replace(' ','').replace('s','').replace('Bed','')),
            'BathRooms' : float(i.select_one('div.teaser__content.clear > small > span:nth-child(2)').get_text().replace('\n','').replace(' ','').replace('s','').replace('Bath','')),
            'Size' : int(i.select_one('div.teaser__content.clear > small > span:nth-child(3)').get_text().replace('\n','').replace(' ','').replace('SqFt','').replace(',','')),
            'Type' : i.select_one('div.teaser__content.clear > small > span:nth-child(4)').get_text().replace('\n','').replace(' ','')
        }
        listings.append(data)
    
    return

for a in range(1,150):
    get_data(a,'any','any')

#converting to Pandas DF
the_collection_miami = pd.DataFrame(listings)
##Writing to CSV file
the_collection_miami.to_csv('listings_1.csv')