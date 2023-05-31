from sentence_transformers import SentenceTransformer, util
from bs4 import BeautifulSoup
import requests
import json

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
        if counter == 10:
            break
        description = item.find("description").text
        #Vissa premium artiklar ger en tom " " sträng i description, från aftonbladet.
        if description ==" " or "PLUS" in description:
            continue
        if "<p>" in description or "</p>":
            #Ta bort den där symbolen från aftonbladet
            description = description.replace("<p>", "")
            description = description.replace("</p>", "")
        if url == url_aftonbladet:
            #Ta bort den där symbolen från aftonbladet
            description = description[2:]
        list_news[item.find("title").text]=([description,item.find("link").text])
    write_txt(list_news)
    return list_news

def write_txt(data):
    with open('data.txt', 'w') as convert_file:
        convert_file.write(json.dumps(data) + "\n")

    

def compare_data(url_list):
    aftonbladet_data = get_data(url_list[0])
    svt_data = get_data(url_list[1])
    svd_data = get_data(url_list[2])
    print(aftonbladet_data)
    print("\n")
    print(svt_data)
    print("\n")
    print(svd_data)

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

