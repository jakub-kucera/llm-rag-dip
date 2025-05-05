#!/usr/bin/env python3

import sys
import json

def replace_text_with_contents(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as infile, \
         open(output_file, "w", encoding="utf-8") as outfile:
        for line in infile:
            line = line.strip()
            if not line:
                # Skip empty lines if any
                continue

            data = json.loads(line)

            if "text" in data:
                data["contents"] = data.pop("text")

            # Write the updated record to the output file
            json.dump(data, outfile, ensure_ascii=False)
            outfile.write("\n")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <input_jsonl> <output_jsonl>")
        sys.exit(1)

    input_jsonl = sys.argv[1]
    output_jsonl = sys.argv[2]
    replace_text_with_contents(input_jsonl, output_jsonl)
