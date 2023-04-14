import sys
import os
import json

def collate_texts(folder_name):
    # get all files in folder
    files = os.listdir(folder_name)

    # open output file
    with open("collated.txt", "w") as output_file:
        # loop through files
        for file in files:
            if not file.endswith(".json"):
                continue
            # open file
            with open(os.path.join(folder_name, file)) as json_file:
                # load json
                data = json.load(json_file)
                # loop through text annotations
                output_file.write(data["responses"][0]['fullTextAnnotation']['text'])

if __name__ == "__main__":
    # get folder name from command line
    if len(sys.argv) < 2:
        print("Please provide a folder name")
        sys.exit(1)

    folder_name = sys.argv[1]

    # throw error if folder does not exist
    if not os.path.exists(folder_name):
        print("Folder does not exist")
        sys.exit(1)

    collate_texts(folder_name)

