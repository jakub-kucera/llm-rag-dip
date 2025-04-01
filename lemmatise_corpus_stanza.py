input_file = "/home/kucerj56/datasets/nss/nss_chunked.jsonl"
output_file = "/home/kucerj56/datasets/nss/nss_chunked_lemmatised.jsonl"

import json

import stanza
from tqdm import tqdm

fields_to_lemmatize = ["contents", "name"]

stanza.download("cs")  # Only need to run this once
nlp = stanza.Pipeline(lang='cs', processors='tokenize,lemma,pos')

name_lemmatised_cache = {}

with open(input_file, "r", encoding="utf-8") as f:
    with open(output_file, "w", encoding="utf-8") as out_f:
        for line in tqdm(f):
            item = json.loads(line)
            for field in fields_to_lemmatize:
                if field in item:
                    if field == "name":
                        if item[field] in name_lemmatised_cache:
                            item[f"{field}_lemmatized"] = name_lemmatised_cache[item[field]]
                        else:
                            doc = nlp(item[field])
                            lemmatized_tokens = [word.lemma for sentence in doc.sentences for word in sentence.words]
                            item[f"{field}_lemmatized"] = " ".join(lemmatized_tokens)
                            name_lemmatised_cache[item[field]] = item[f"{field}_lemmatized"]
                    else:
                        doc = nlp(item[field])
                        lemmatized_tokens = [word.lemma for sentence in doc.sentences for word in sentence.words]
                        item[f"{field}_lemmatized"] = " ".join(lemmatized_tokens)
                else:
                    print(f"Field '{field}' not found in item: {item.get('id', 'unknown')}")
            out_f.write(json.dumps(item) + "\n")
