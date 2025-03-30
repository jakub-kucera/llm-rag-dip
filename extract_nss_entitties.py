import json
import os
from vllm import LLM, SamplingParams

# input_dir = "files20232024"
input_dir = "/home/kucerj56/llm-rag-dip/files_nss"
output_file = "/home/kucerj56/llm-rag-dip/preprocessed_nss.jsonl"

output_dataset = []
# for c, file in enumerate(os.listdir(input_dir)):
#     print(f"Opening {file}...")
#     with open(f"{input_dir}/{file}") as f:
#         content = f.read()
        # print(content)

# llm = LLM(model="/home/kucerj56/models/mistralai/Ministral-8B-Instruct-2410")  # Replace with your actual model path
llm = LLM(
    # model="/home/kucerj56/models/microsoft/Phi-4-mini-instruct",
    # model="/home/kucerj56/models/meta-llama/Llama-3.1-8B-Instruct",
    model="/home/kucerj56/models/meta-llama/Llama-3.3-70B-Instruct-bnb-4bit",
    quantization="bitsandbytes",
    load_format="bitsandbytes",
    max_logprobs = 32016,
    # max_model_len = 128000,
    max_model_len = 80000,
    trust_remote_code=True
)
sampling_params = SamplingParams(
    temperature=0.0,
    max_tokens=2048,
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

input_prompts = []

print(f"Opening {input_dir}...")
for c, file in enumerate(os.listdir(input_dir)):
    # print(f"Opening {file}...")
    with open(f"{input_dir}/{file}", encoding="utf-8") as f:
        content = f.read()

    full_prompt = prompt_template.format(document_contents=content.strip())
    input_prompts.append(full_prompt)

# get a subset of 10 prompts
input_prompts = input_prompts[:10]

print(f"Generating outputs for {len(input_prompts)} prompts...")
outputs = llm.generate(input_prompts, sampling_params, use_tqdm=True)
print(f"Generated {len(outputs)} outputs.")

print(f"Writing outputs to {output_file}...")
with open(output_file, "w", encoding="utf-8") as out_f:
    for output in outputs:
        txt = output.outputs[0].text.strip()
        try:
            entry = json.loads(txt)
        except:
            print(f"Error parsing JSON: {txt}")
            # wrap string in JSON
            entry = {"error": txt}
        out_f.write(json.dumps(entry, ensure_ascii=False) + "\n")
