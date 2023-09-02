from bs4 import BeautifulSoup
import requests
import json
import ast

url_aftonbladet  ="https://rss.aftonbladet.se/rss2/small/pages/sections/senastenytt/"
url_svt = "https://www.svt.se/nyheter/rss.xml"
url_svd = "https://www.svd.se/?service=rss"

def get_data(url):
    xml = requests.get(url)
    soup = BeautifulSoup(xml.content, features="xml")
    items = soup.find_all("item")
    list_news = []
    counter = 0
    for item in items:
        temp_dict = {}
        counter += 1
        if counter == 1:
            break
        try:
            description = item.find("description").text
        except:
            print("FELLL")
            print(url)
            print(item.find("title").text)
        #Vissa premium artiklar ger en tom " " sträng i description, från aftonbladet.
        #Samt somliga direktrapporteringar från svd
        if description ==" " or "PLUS" in description or "SvD:s liverapport om Rysslands invasion av Ukraina" in description or description == "":
            continue
        if "<p>" in description or ("</p>" or "&quot;" or "\n"):
            #Ta bort den där symbolen från aftonbladet
            description = description.replace("<p>", "")
            description = description.replace("</p>", "")
            description = description.replace("&quot;", "")
            description = description.replace("\n;", "")
        if url == url_aftonbladet:
            #Ta bort den där symbolen från aftonbladet
            description = description[2:]
            #slippa råka klicka på länk.
        link = item.find("link").text
        link = "https...."
        if url == url_aftonbladet:
            news_paper = "Aftonbladet"
        elif url == url_svd:
            news_paper = "SVD"
        elif url == url_svt:
            news_paper = "SVT"
        
        temp_dict[item.find("title").text]=[description,link,news_paper]
        list_news.append(temp_dict)
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
        file_contents_list =[]
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"): 
                print("FACJJJ")
                continue
            file_contents  = line
            file_contents = ast.literal_eval(file_contents)
            file_contents_list.append([file_contents])

    # Clear the file by opening it in write mode and truncating its content
    with open("data.txt", "w", encoding="utf-8") as file:
        file.write("")
    return file_contents_list

def compare_data(url_list, list_data_file):
    #Läs in från filen först, list_rss ska jämföras med list_data_file
    
    list_rssdata = [get_data(url) for url in url_list]
    list_merged = list_rssdata + list_data_file
    list_merged = [i for n, i in enumerate(list_merged)
               if i not in list_merged[n + 1:]]

    for row in list_merged:                                 #Detta borde egentligen vara i write_file. Låt funktionen göra en sak
        if (type(row) == dict):
            write_file(row)
        for data in row:
            if (type(data) == dict):
                write_file(data)    
    return list_merged           

def main1(url):
    list_data = read_file()
    list_merged = compare_data(url, list_data)
    return list_merged


list_url = [url_aftonbladet,url_svt, url_svd]
#list_url = [url_aftonbladet]
main1(list_url)

