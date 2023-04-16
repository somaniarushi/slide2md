# File that runs the entire pdf -> markdown pipeline

import sys
import os
import json
import argparse

from converter import convert_to_images
from text2markdown import text2markdown
from compare_texts import compare_texts
from detect_text import detect_text


if __name__ == "__main__" :
    if os.environ.get("OPENAI_API_KEY") is None:
        print("Please set OpenAI API environment variable as 'API'")
        sys.exit(1)

    if os.environ.get("GOOGLE_APPLICATION_CREDENTIALS") is None:
        print("Please set Google Cloud credentials environment variable (a file) as 'GOOGLE_APPLICATION_CREDENTIALS'")
        sys.exit(1)

    # use argparse to parse arguments
    parser = argparse.ArgumentParser()
    # check if the following flags exist --skip-convert, --skip-detect, --skip-markdown, all default false
    parser.add_argument("filename", help="File to convert to markdown")
    parser.add_argument("--skip-convert", action="store_true", default=False, help="Skip converting pdf to images")
    parser.add_argument("--skip-detect", action="store_true", default=False, help="Skip detecting text")
    parser.add_argument("--skip-markdown", action="store_true", default=False, help="Skip converting text to markdown")
    parser.add_argument("--skip-compare", action="store_true", default=True, help="Skip comparing text to last text")

    args = parser.parse_args()

    filename = args.filename
    skip_convert = args.skip_convert
    skip_detect = args.skip_detect
    skip_markdown = args.skip_markdown
    skip_compare = args.skip_compare

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
            detect_text(f"tmp/{file}", f"tmp/{filename_no_ext}.json")


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
                if not skip_compare:
                    if last_text is not None:
                        cos_sim = compare_texts(last_text, text)
                        if cos_sim > 0.9:
                            last_text = text
                            continue
                    last_text = text
                markdown = text2markdown(text)
                markdowns.append(markdown)
            except:
                continue

    # write markdowns to file
    print("Writing markdowns to file...")
    combined_markdowns = "\n".join(markdowns)
    with open(f"{filename.split('.')[0]}.md", "w") as f:
        f.write(combined_markdowns)

