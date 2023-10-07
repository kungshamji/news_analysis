#!/usr/bin/env python
import json
from sentence_transformers import SentenceTransformer, util
from analys import run, list_url

# Load the SentenceTransformer model
model = SentenceTransformer("KBLab/sentence-bert-swedish-cased")
list_not_to_include = ["Detta har hänt", "Utvalda nyheter", "Här är några nyheter i", "Detta är några av nyheterna i"]
def remove_duplicate_dicts(input_list):
    seen_dicts = set()
    filtered_list = []
    for sublist in input_list:
        filtered_sublist = []
        for dictionary in sublist:
            dict_json = json.dumps(dictionary, sort_keys=True)
            if dict_json not in seen_dicts:
                seen_dicts.add(dict_json)
                filtered_sublist.append(dictionary)
        filtered_list.append(filtered_sublist)
    return filtered_list

def extract_sentences_info(list_merged):
    sentences_info = []
    for sublist in list_merged:
        for news_dict in sublist:
            for sentence, link, newspaper in news_dict.values():
                # Exclude sentences containing "Detta har hänt"
                if (not any(not_to_include in sentence for not_to_include in list_not_to_include)): 
                    sentences_info.append((sentence, link, newspaper))
    return sentences_info

def compute_cosine_similarities(sentences_info):
    embeddings = model.encode([info[0] for info in sentences_info], convert_to_tensor=True)
    cosine_scores = util.pytorch_cos_sim(embeddings, embeddings)
    return cosine_scores

def find_similar_sentences(cosine_scores, sentences_info):
    similar_sentences = []
    num_sentences = len(sentences_info)
    for i in range(num_sentences):
        for j in range(i + 1, num_sentences):
            similarity = cosine_scores[i][j].item()
            sentence1, link1, newspaper1 = sentences_info[i]
            sentence2, link2, newspaper2 = sentences_info[j]

            if similarity >= 0.5 and (sentence1.strip() != "" or sentence2.strip() != ""):
                similar_sentences.append((similarity, (sentence1, link1, newspaper1), (sentence2, link2, newspaper2)))
    return similar_sentences

def print_and_save_similar_sentences(similar_sentences, output_file):
    with open(output_file, "w", encoding="utf-8") as file:
        for similarity, (sentence1, link1, newspaper1), (sentence2, link2, newspaper2) in similar_sentences:
            print((sentence1, link1, newspaper1))
            print("helo world ")
            print((sentence2, link2, newspaper2))
            print(similar_sentences)
            file.write(f"Similarity Score: {similarity:.2f}\n")
            file.write(f"Sentence 1 ({newspaper1}): {sentence1}\n")
            file.write(f"Link 1: {link1}\n")
            file.write(f"Sentence 2 ({newspaper2}): {sentence2}\n")
            file.write(f"Link 2: {link2}\n")
            file.write("\n")

def clear_file(file_name):
    with open(file_name, "w", encoding="utf-8") as file:
        file.write("")


def main():
    # Get the list of news articles from the main1 function
    list_merged = run(list_url)

    # Remove duplicate dictionaries from the list_merged
    list_merged = remove_duplicate_dicts(list_merged)

    # Extract sentences and related information
    sentences_info = extract_sentences_info(list_merged)

    # Compute cosine similarities between pairs of sentences
    cosine_scores = compute_cosine_similarities(sentences_info)

    # Find and sort similar sentences
    similar_sentences = find_similar_sentences(cosine_scores, sentences_info)
    similar_sentences.sort(reverse=True, key=lambda x: x[0])

    # Print and save the most similar sentences to a text file
    print_and_save_similar_sentences(similar_sentences, "similar_sentences.txt")

    clear_file("data.txt")

if __name__ == "__main__":
    main()
