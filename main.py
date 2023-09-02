from sentence_transformers import SentenceTransformer, util
from analys import main1, list_url
model = SentenceTransformer("KBLab/sentence-bert-swedish-cased")


def main():
    list_merged = main1(list_url)
    print(list_merged)
    sentences2 = ""
    for i,lists in enumerate(list_merged):
        for dict in lists:
            for value in dict.values():
                sentences1 = value[0]
                for iter in range(len(value)):
                sentences2 = 
            

    sentences1 = ["plugga"]
    sentences2 = ["dugga"]


    #Compute embedding for both lists
    embeddings1 = model.encode(sentences1, convert_to_tensor=True)
    embeddings2 = model.encode(sentences2, convert_to_tensor=True)

    #Compute cosine-similarities
    cosine_scores = util.cos_sim(embeddings1, embeddings2)

    #Output the pairs with their score
    for i in range(len(sentences1)):
        print("{} \t\t {} \t\t Score: {:.2f}".format(sentences1[i], sentences2[i], cosine_scores[i][i]))


main()