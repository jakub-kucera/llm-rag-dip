import getpass
import os
import json
import datetime
from math import ceil
from time import sleep

from langchain_google_genai import ChatGoogleGenerativeAI
from tqdm import tqdm

# CONTEXXT_MAX_LENGTH = 128000
CONTEXXT_MAX_LENGTH = 900000

def process_nss_documents(input_dir: str, output_file: str):
    # These are now passed as function arguments
    output_dataset = []
    # for c, file in enumerate(os.listdir(input_dir)):
    #     print(f"Opening {file}...")
    #     with open(f"{input_dir}/{file}") as f:
    #         content = f.read()
    #         print(content)

    if "GOOGLE_API_KEY" not in os.environ:
        os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter your Google AI API key: ")

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0.1,
        # max_tokens=2048,
        max_tokens=8192,
        max_retries=2
    )

    prompt_template = """
    Below is a document which is a “rozhodnutí Nejvyššího správního soudu”.

    [START OF DOCUMENT]
    {document_contents}
    [END OF DOCUMENT]

    Carefully analyse it and answer the following questions.
    1. what was the verdict
    2. is there a right to compensation of legal expenses
    3. is there a possibility of appeal
    4. list of referenced paragraphs
    5. list of referenced entities
    Output the answer as a single valid JSON only, do not output any other text or characters. Example of output:
    {{
         "verdict": "žaloba odmítnuta",
         "right_to_compensation": true,
         "possibility_of_appeal": true,
         "referenced_paragraphs": ["§ 23", "§ 248 odst. 2 písm. e) občanského soudního řádu", "§ 46 odst. 1 písm. d) s. ř. s.", "§ 244 odst. 2 o. s. ř."],
         "referenced_entities": ["SPORT WORKS, s. r. o.", "Ing. Jan Prokop", "Krajský soud v Brně"]
    }}
    """

    # input_prompts = []

    print(f"Opening {input_dir}...")

    error_count = 0
    total_count = 0
    print(f"Generating outputs to {output_file}...")
    # TODO change mode to append file?
    with open(output_file, "w", encoding="utf-8") as out_f:
        # for prompt in tqdm(input_prompts):
        previous_iteration_start = datetime.datetime.now()
        # for file in tqdm(os.listdir(input_dir)[(585+1+453+1+376+1+1500):]):
        for file in tqdm(os.listdir(input_dir)):
            print(f"Opening {file}...")
            with open(f"{input_dir}/{file}", encoding="utf-8") as f:
                content = f.read()

            full_prompt = prompt_template.format(document_contents=content.strip())

            if len(full_prompt) > CONTEXXT_MAX_LENGTH:
                print(f"File {file} as it is too long ({len(full_prompt)} characters).")
                content_shortened = content[:CONTEXXT_MAX_LENGTH - len(prompt_template) - 100]
                full_prompt = prompt_template.format(document_contents=content_shortened.strip())
            prompt = full_prompt

            entry = {
                "file": file,
                "prompt": prompt,
            }

            iteration_start = datetime.datetime.now()
            diff = iteration_start - previous_iteration_start
            # print(diff)
            # print(diff.total_seconds())

            if diff.total_seconds() <= 4.5:
                sleep_time = 4.5 - diff.total_seconds()
                # print(f"Sleeping for {sleep_time} seconds...")
                sleep(ceil(sleep_time))

            response = llm.invoke(prompt)

            txt = response.content.strip()
            if '```json' in txt:
                txt = txt.replace('```json', '').replace('```', '')
            try:
                entry["response"] = json.loads(txt)
            except:
                print(f"Error parsing JSON: {txt[:100]}")
                entry["response"] = None
                entry["error"] = txt
                error_count += 1
            out_f.write(json.dumps(entry, ensure_ascii=False) + "\n")
            previous_iteration_start = iteration_start
        total_count += 1

    print(f"Done. {error_count} errors encountered. % of errors: {error_count / total_count * 100:.2f}%")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Process NSS documents using a specified LLM.")
    parser.add_argument("--input_dir", help="Directory containing input documents.")
    parser.add_argument("--output_file", help="Path to the output JSONL file.")
    # parser.add_argument("model_path", help="Path to the LLM model.")

    args = parser.parse_args()

    # process_nss_documents(args.input_dir, args.output_file, args.model_path)
    process_nss_documents(args.input_dir, args.output_file)