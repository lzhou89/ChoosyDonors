from bs4 import BeautifulSoup
import urllib2
import time

for i in range(2, 319): 
    link = "http://zipatlas.com/us/zip-code-comparison/population-below-poverty-level."+str(i)+".htm"
    header = {'User-Agent': 'Mozilla/5.0'} #Needed to prevent 403 error on Wikipedia
    req = urllib2.Request(link,headers=header)
    page = urllib2.urlopen(req)
    soup = BeautifulSoup(page)
     
    zip_code = ""
    pov = ""
     
    table = soup.find("table", { "rules" : "all" })
     
    f = open('output.csv', 'a')
     
    for row in table.findAll("tr")[1:]:
        cells = row.findAll("td")
        #For each "tr", assign each "td" to a variable.
        if len(cells) == 7:
            zip_code = cells[1].find(text=True)
            pov = cells[5].find(text=True)
     
            #Strip out the "\n" that seems to be at the start of some postcodes
            write_to_file = zip_code + "," + pov + "\n"
            # print write_to_file
            f.write(write_to_file)
     
    f.close()
    time.sleep(30)

print "Done"