from bs4 import BeautifulSoup
import urllib2
import time
import random

BASE_LINK = "http://www.city-data.com/crime/"
def setup(link):
    header = {'User-Agent': 'Mozilla/5.0'} #Needed to prevent 403 error on Wikipedia
    req = urllib2.Request(link,headers=header)
    page = urllib2.urlopen(req)
    return BeautifulSoup(page)

def get_state_links(link):
    soup = setup(link)
    table = soup.find("table", { "cellpadding" : "5"})
    state_links = [BASE_LINK + td.a["href"] for td in table.findAll("td")]
    return state_links

def get_city_links(state_link):
    soup = setup(state_link)
    table = soup.find("table", { "cellpadding" : "5"})
    city_links = [BASE_LINK + td.a["href"] for td in table.findAll("td")]
    for city in city_links:
        print city
        scrape_crime(city)
    return

def scrape_crime(link):
    zip_code = ""
    crime = ""
    
    soup = setup(link) 
    table = soup.find("table", { "id" : "crimeTab" })
    foot = table.find("tfoot")
     
    f = open('crime.csv', 'w')
     
    row = foot.find("tr")
    cells = row.findAll("td")
    #For each "tr", assign each "td" to a variable.
    crime = cells[-1].find(text=True)

    div = soup.find("div", { "class" : "style1"})
    links = div.findAll("a")
    zip_code = links[-1].find(text=True)

    #Strip out the "\n" that seems to be at the start of some postcodes
    write_to_file = zip_code + "," + crime + "\n"
    # print write_to_file
    f.write(write_to_file)

    f.close()
    x = random.randint(3,7)
    time.sleep(10*x)
    return


if __name__ == '__main__':
    states = get_state_links(BASE_LINK)

    for state in states:
        print state
        get_city_links(state)
    print "Done"