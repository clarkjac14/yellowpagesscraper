""",------------------------------,
  /	 Yellow Pages Scraper        /
 /	Author: Jacob Clark			/
/______________________________/
"""
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from sys import stdout
import os

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

#Load uBlock Origin to decrease load times from ads.
ublock_path = "/Users/Jacob/Library/Application Support/Google/Chrome/Default/Extensions/cjpalhdlnbpafiamejdnhcphjbkeiagm/1.16.10_0"
options = Options()
options.add_argument('load-extension=' + ublock_path)
driver = webdriver.Chrome('/Users/Jacob/chromedriver/chromedriver', chrome_options=options)
driver.create_options()

#Complete URL of YellowPages search results.
print("Enter a complete YellowBooks search result URL to scrape.")
url = input()
driver.get(url);
    
businesses = []    
more = True

cls()
print("\n\n\n\nScraping YellowBooks")
pagenumber = 1
while(more):
    print("Scraping page " + str(pagenumber) + "...")
    try:
        search_results = driver.find_element_by_xpath('//*[@id="main-content"]/div[2]/div[2]')
        #print(search_results.text)
        
        biz_list = search_results.find_elements_by_class_name("result")
        for result in biz_list:
            div = result.find_element_by_tag_name("div")
            vcard = div.find_element_by_class_name("v-card")
            info = vcard.find_element_by_class_name("info")
            name = info.find_element_by_class_name("n").text.replace(',','')
            info_section_primary = info.find_element_by_class_name("info-primary")
            info_section_secondary = info.find_element_by_class_name("info-secondary")
            adr = info_section_primary.find_element_by_class_name("adr")
            address = adr.find_elements_by_tag_name("span")
            try:
                street = address[0].text.replace(',','')
                city = address[1].text.replace(',','')
                state = address[2].text.replace(',','')
                code = address[3].text.replace(',','')
            except:
                #print("No address for: " + name)
                street = ""
                city = ""
                state = ""
                code = ""
                pass
            phone = info_section_primary.find_element_by_class_name("phones").text
            categoriesDiv = info_section_secondary.find_element_by_class_name("categories")
            
            categoriesList = categoriesDiv.find_elements_by_tag_name("a")
            
            categories = " ".join(s.text for s in categoriesList)
                            
            links = info_section_secondary.find_element_by_class_name("links")
            try:
                link = links.find_element_by_class_name("track-visit-website")
                website = link.get_attribute("href")
            except:
                #print("No website for: " + name)
                website = ""
                pass
            
            #index all information into a dictionary
            biz_dict = {}
            biz_dict["name"] = name.split(" ", 1)[1]
            biz_dict["street"] = street
            biz_dict["city"] = city
            biz_dict["state"] = state
            biz_dict["code"] = code
            biz_dict["phone"] = phone
            biz_dict["website"] = website
            biz_dict["categories"] = categories
            
            #append each dictionary to a list
            businesses.append(biz_dict)
            
        next = driver.find_element_by_class_name('next')
        next.click()
        time.sleep(1) #Give the next button time to load correctly!
        more = True
        pagenumber = pagenumber + 1
    except Exception as e:
        more = False
        print(str(e))
driver.quit()
print("Web scraping complete.")

cls()

csv_columns = "Company Name, Phone, Address, City, State, Zip, Website, Categories \n"

print("Enter a name for your csv file.")
ofile = input() + ".csv"
with open(ofile, "w") as of:
    of.write(csv_columns)
    for b in businesses:
        of.write(   b["name"] + ',' +
                    b["phone"] + ',' +
                    b["street"] + ',' +
                    b["city"] + ',' +
                    b["state"] + ',' + 
                    b["code"] + ',' +
                    b["website"] + ','+
                    b["categories"] + '\n')

print("File saved successfully.")