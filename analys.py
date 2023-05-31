from sentence_transformers import SentenceTransformer, util
from bs4 import BeautifulSoup
import requests
import io
import json
import codecs
url_aftonbladet  ="https://rss.aftonbladet.se/rss2/small/pages/sections/senastenytt/"
url_svt = "https://www.svt.se/nyheter/rss.xml"
url_svd = "https://www.svd.se/?service=rss"


model = SentenceTransformer("KBLab/sentence-bert-swedish-cased")

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
        if description ==" " or "PLUS" in description or "SvD:s liverapport om Rysslands invasion av Ukraina" in description:
            continue
        if "<p>" in description or "</p>":
            #Ta bort den där symbolen från aftonbladet
            description = description.replace("<p>", "")
            description = description.replace("</p>", "")
        if url == url_aftonbladet:
            #Ta bort den där symbolen från aftonbladet
            description = description[2:]
        list_news[item.find("title").text]=([description,item.find("link").text])
    write_file(list_news)
    return list_news

def write_file(data):
    with open("data.txt", "a", encoding="utf-8") as file:
        # Convert the dictionary to a JSON string
        json_data = json.dumps(data, ensure_ascii=False)
        # Write the JSON string to the file
        file.write(json_data)
        file.write("\n")

    #read_file()

def read_file():
    # Open the file in read mode with UTF-8 encoding
    with open("data.txt", "r", encoding="utf-8") as file:
        # Read the contents of the file
        file_contents = file.read()
    
    # Clear the file by opening it in write mode and truncating its content
    with open("data.txt", "w", encoding="utf-8") as file:
        file.write("")

def compare_data(url_list):
    aftonbladet_data = get_data(url_list[0])
    svt_data = get_data(url_list[1])
    svd_data = get_data(url_list[2])

def main(url):
    compare_data(url)



list_url = [url_aftonbladet,url_svt, url_svd]
main(list_url)


# sentences1 = ["spelar du någon sport  p p p"]
# sentences2 = ["Hockey är min favorit p p p hobby."]

# #Compute embedding for both lists
# embeddings1 = model.encode(sentences1, convert_to_tensor=True)
# embeddings2 = model.encode(sentences2, convert_to_tensor=True)

# #Compute cosine-similarities
# cosine_scores = util.cos_sim(embeddings1, embeddings2)

# #Output the pairs with their score
# for i in range(len(sentences1)):
#     print("{} \t\t {} \t\t Score: {:.4f}".format(sentences1[i], sentences2[i], cosine_scores[i][i]))

