import json
import os

# input_dir = "files20232024"
input_dir = "/home/kucerj56/llm-rag-dip/files_nss"
# output_file = "nss.jsonl"



def preprocess_nss(content) -> tuple[str, str]:
            # content = content.replace("\n", " ")
            # content = content.replace("\t", " ")
            # content = content.replace("\r", " ")
            content = content.strip()
            try:
                name, content = content.split("\n", maxsplit=1)
                if name.startswith("Ej"):
                    name, content = content.split("\n", maxsplit=1)
            except ValueError:
                print(f"Document with missing title or text: {content}")
                return None, content
            return name, content


output_dataset = []
for c, file in enumerate(os.listdir(input_dir)):
    print(f"Opening {file}...")
    with open(f"{input_dir}/{file}") as f:
        content = f.read()
        # print(content)
    # break
    name, preprocessed_content = preprocess_nss(content)
    output_dataset.append({
        "id": c,
        "file": file,
        "name": name,
        # "title": name, # TODO?
        "contents": preprocessed_content
    })
    # print(F"Processed NAME: {name}")
    # print(f"Processed {preprocessed_content}")
    # break





import stanza

# Download Czech models if not already downloaded
# stanza.download("cs")  # Only need to run this once

nlp = stanza.Pipeline(lang='cs', processors='tokenize,lemma,pos')


from tqdm import tqdm

stanza_chunked_output_dataset = []
global_counter = 0
# for c, item in tqdm(enumerate(output_dataset)):
for item in tqdm(output_dataset):
    content = item['contents']
    # print(f"content: {content}")
    doc = nlp(content)
    sentences = []
    for sentence in doc.sentences:
        sentences.append(sentence.text)
    # sentences = [sentence for sentence in sentences if sentence.strip()]
    for sentence in sentences:
        stanza_chunked_output_dataset.append({
            "id": global_counter,
            "file": item['file'],
            "name": item['name'],
            "contents": sentence
        })
        global_counter += 1
    # print("sentences")
    # for sentence in sentences:
    #     print(sentence)
    # break


with open("/home/kucerj56/datasets/nss/nss_stanza_chunked.jsonl", "w", encoding="utf-8") as f:
    for item in stanza_chunked_output_dataset:
        f.write(json.dumps(item) + "\n")
