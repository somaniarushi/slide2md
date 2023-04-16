import sys
import os
import json
from deprecated import deprecated

@deprecated(version="0.0.1", reason="Collating texts reduces final accuracy, each text should be cleaned invividually")
def collate_texts(folder_name):
    """
    For every json file in folder_name, collate the text into a single file.
    @param folder_name: The folder containing the json files

    WARNING: The function uses every json file in the folder, so make sure there are no other json files in the folder.
    """
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


################## TESTING ##################
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

