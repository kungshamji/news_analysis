from bs4 import BeautifulSoup
import requests
import json
import ast

url_aftonbladet = "https://rss.aftonbladet.se/rss2/small/pages/sections/senastenytt/"
url_svt = "https://www.svt.se/nyheter/rss.xml"
url_svd = "https://www.svd.se/?service=rss"
list_url = [url_aftonbladet, url_svt, url_svd]

not_to_include = ["PLUS", "SvD:s liverapport om Rysslands invasion av Ukraina", 
                  "Nyheter från dagen", "Detta har hänt i", 
                  "Detta är några av nyheterna i"
                  , "Här är några nyheter i", "Detta har hänt", 
                  "Utvalda nyheter", "Här är några nyheter i", "Detta är några av nyheterna i"]

def get_data(url):
    xml = requests.get(url)
    soup = BeautifulSoup(xml.content, features="xml")
    items = soup.find_all("item")
    list_news = []
    counter = 0

    for item in items:
        temp_dict = {}
        counter += 1
        if counter > 3:
            break
        description = extract_description(item)
        if should_include_description(description):
            continue
        description = preprocess_description(description, url)
        link = extract_link(item)
        news_paper = get_news_paper(url)
        
        temp_dict[item.find("title").text] = [description, link, news_paper]
        list_news.append(temp_dict)

    return list_news

def extract_description(item):
    try:
        return item.find("description").text
    except:
        print(item.find("title").text)
        return ""

def should_include_description(description):
    return not description or any(exclude_word in description for exclude_word in not_to_include)

def preprocess_description(description, url):
    if "<p>" in description or ("</p>" or "&quot;" or "\n"):
        description = description.replace("<p>", "")
        description = description.replace("</p>", "")
        description = description.replace("&quot;", "")
        description = description.replace("\n;", "")
    if url == url_aftonbladet:
        description = description[2:]
    return description

def extract_link(item):
    return item.find("link").text

def get_news_paper(url):
    if url == url_aftonbladet:
        return "Aftonbladet"
    elif url == url_svd:
        return "SVD"
    elif url == url_svt:
        return "SVT"

def write_file(data):
    with open("data.txt", "a", encoding="utf-8") as file:
        json_data = json.dumps(data, ensure_ascii=False)
        file.write(json_data)
        file.write("\n")    
  
def read_file():
    with open("data.txt", "r", encoding="utf-8") as file:
        file_contents_list =[]
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"): 
                continue
            file_contents  = line
            file_contents = ast.literal_eval(file_contents)
            file_contents_list.append([file_contents])

    with open("data.txt", "w", encoding="utf-8") as file:
        file.write("")
    return file_contents_list

def compare_data(url_list, list_data_file):
    list_rssdata = [get_data(url) for url in url_list]
    list_merged = list_rssdata + list_data_file
    list_merged = [i for n, i in enumerate(list_merged)
               if i not in list_merged[n + 1:]]
    
    for row in list_merged:                                
        if (type(row) == dict):
            write_file(row)
        for data in row:
            if (type(data) == dict):
                write_file(data)    
    return list_merged           

def run(url):
    list_data = read_file()
    list_merged = compare_data(url, list_data)
    return list_merged

def main():
    run(list_url)

if __name__ == "__main__":
    main()
