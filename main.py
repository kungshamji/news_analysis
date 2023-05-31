from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer("KBLab/sentence-bert-swedish-cased")



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

