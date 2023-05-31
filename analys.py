from bs4 import BeautifulSoup
import requests
import io
import json
import codecs
import ast
import time
url_aftonbladet  ="https://rss.aftonbladet.se/rss2/small/pages/sections/senastenytt/"
url_svt = "https://www.svt.se/nyheter/rss.xml"
url_svd = "https://www.svd.se/?service=rss"



def get_data(url):
    xml = requests.get(url)
    soup = BeautifulSoup(xml.content, features="xml")
    items = soup.find_all("item")
    list_news = {}
    counter =0
    for item in items:
        counter += 1
        if counter == 3:
            break
        description = item.find("description").text
        #Vissa premium artiklar ger en tom " " sträng i description, från aftonbladet.
        #Samt somliga direktrapporteringar från svd
        if description ==" " or "PLUS" in description or "SvD:s liverapport om Rysslands invasion av Ukraina" in description or description == "":
            continue
        if "<p>" in description or "</p>":
            #Ta bort den där symbolen från aftonbladet
            description = description.replace("<p>", "")
            description = description.replace("</p>", "")
        if url == url_aftonbladet:
            #Ta bort den där symbolen från aftonbladet
            description = description[2:]
        list_news[item.find("title").text]=([description,item.find("link").text])
    return list_news

def write_file(data):
    with open("data.txt", "a", encoding="utf-8") as file:
        # Convert the dictionary to a JSON string
        json_data = json.dumps(data, ensure_ascii=False)
        file.write(json_data)
        file.write("\n")
  
def read_file():
    # Open the file in read mode with UTF-8 encoding
    with open("data.txt", "r", encoding="utf-8") as file:
        # Read the contents of the file into list
        file_contents = file.read().splitlines()


    # Clear the file by opening it in write mode and truncating its content
    with open("data.txt", "w", encoding="utf-8") as file:
        file.write("")
    return file_contents

def compare_data(url_list):
    #Läs in från filen först
    list_data_file = read_file()
    #Dessa tre ska jämföras med filen. 
    list_rssdata=[get_data(url) for url in url_list ]
    
    for data in list_rssdata:
        write_file(data)
    time.sleep(3)
    
    print(list_rssdata)
    print(list_data_file)

def main(url):
    compare_data(url)



list_url = [url_aftonbladet,url_svt, url_svd]
main(list_url)

