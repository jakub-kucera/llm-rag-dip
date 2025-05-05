#!/usr/bin/env python3

import sys
import json

def add_id_to_jsonl(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as infile, \
         open(output_file, "w", encoding="utf-8") as outfile:
        for i, line in enumerate(infile, start=0):
            line = line.strip()
            if not line:
                # Skip empty lines (if any exist)
                continue
            
            data = json.loads(line)
            data["id"] = i
            json.dump(data, outfile, ensure_ascii=False)
            outfile.write("\n")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <input_jsonl> <output_jsonl>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    add_id_to_jsonl(input_file, output_file)
