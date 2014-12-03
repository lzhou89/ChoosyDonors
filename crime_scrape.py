from bs4 import BeautifulSoup
import urllib2
import time
import random

BASE_LINK = "http://www.city-data.com/crime/"
def setup(link):
    header = {'User-Agent': 'Mozilla/5.0'} 
    req = urllib2.Request(link,headers=header)
    page = urllib2.urlopen(req)
    return BeautifulSoup(page)

def get_state_links(link):
    """Gets the urls for all states on city-data.com"""
    soup = setup(link)
    table = soup.find("table", { "cellpadding" : "5"})
    state_links = [BASE_LINK + td.a["href"] for td in table.findAll("td")[:-1]]
    return state_links

def get_city_links(state_link):
    """Gets the urls for all cities in specified state."""
    soup = setup(state_link)
    table = soup.find("table", { "cellpadding" : "5"})
    city_links = [BASE_LINK + a["href"] for a in table.findAll("a")]
    for city in city_links:
        print city
        scrape_crime(city)
    return

def scrape_crime(link):
    """Scrapes zip code and crime rate for a city."""
    zip_code = ""
    crime = ""
    
    soup = setup(link) 
    table = soup.find("table", { "id" : "crimeTab" })
    foot = table.find("tfoot")
     
    f = open('crime.csv', 'a')
     
    row = foot.find("tr")
    cells = row.findAll("td")
    crime = cells[-1].find(text=True)

    div = soup.find("div", { "class" : "style1"})
    links = div.findAll("a")
    zip_code = links[-1].find(text=True)

    write_to_file = zip_code + "," + crime + "\n"
    # print write_to_file
    f.write(write_to_file)

    f.close()
    x = random.randint(3,7)
    time.sleep(10*x)
    return


if __name__ == '__main__':
    states = get_state_links(BASE_LINK)
    # test = get_city_links(states[0])
    for state in states:
        get_city_links(state)
    print "Done"