# File that runs the entire pdf -> markdown pipeline

import sys
import os
import json
import tqdm
import openai
import argparse
import numpy as np
from converter import convert_to_images
from text2markdown import text2markdown


if __name__ == "__main__" :
    if len(sys.argv) < 2:
        print("Please provide a file name")
        sys.exit(1)

    # use argparse to parse arguments
    parser = argparse.ArgumentParser()
    # check if the following flags exist --skip-convert, --skip-detect, --skip-markdown, all default false
    parser.add_argument("filename")
    parser.add_argument("--skip-convert", action="store_true", default=False)
    parser.add_argument("--skip-detect", action="store_true", default=False)
    parser.add_argument("--skip-markdown", action="store_true", default=False)

    args = parser.parse_args()

    filename = args.filename
    skip_convert = args.skip_convert
    skip_detect = args.skip_detect
    skip_markdown = args.skip_markdown

    # if filename is not pdf, exit
    if not filename.endswith(".pdf"):
        print("File must be a pdf")
        sys.exit(1)

    # if file does not exist, exit
    if not os.path.exists(filename):
        print("File does not exist")
        sys.exit(1)

    # convert pdf to images
    if not skip_convert:
        print("Converting pdf to images...")
        convert_to_images(filename)

    # get all files in tmp folder
    if not skip_detect:
        print("Detecting text...")
        files = os.listdir("tmp")
        for file in files:
            # if file is not png, continue
            if not file.endswith(".png"):
                continue
            # run gcloud command
            filename_no_ext = file.split(".")[0]
            os.system(f"gcloud ml vision detect-text tmp/{file} > tmp/{filename_no_ext}.json")

    # get all files in tmp folder
    all_texts = []
    files = os.listdir("tmp")
    # sort files by name
    files.sort()
    markdowns = []
    last_text = None
    print("Converting text to markdown...")
    for file in files:
        # if file is not json, continue
        if not file.endswith(".json"):
            continue
        # read file
        with open(f"tmp/{file}") as f:
            data = json.load(f)
            try:
                text = data["responses"][0]['fullTextAnnotation']['text']
                if last_text is not None:
                    # Create embeddings of text and last_text
                    # If they are similar, do not convert to markdown
                    text_embed = np.array(openai.Embedding.create(
                        input = text,
                        model="text-embedding-ada-002"
                    )['data'][0]['embedding'])
                    last_text_embed = np.array(openai.Embedding.create(
                        input = last_text,
                        model="text-embedding-ada-002"
                    )['data'][0]['embedding'])
                    # Compute cosine similarity
                    cos_sim = np.dot(text_embed, last_text_embed) / (np.linalg.norm(text_embed) * np.linalg.norm(last_text_embed))
                    if cos_sim > 0.9:
                        last_text = None
                        continue
                last_text = None
                markdown = text2markdown(text)
                markdowns.append(markdown)
            except:
                continue

    # write markdowns to file
    print("Writing markdowns to file...")
    combined_markdowns = "\n".join(markdowns)
    with open(f"{filename.split('.')[0]}.md", "w") as f:
        f.write(combined_markdowns)

