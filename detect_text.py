import os
import sys
import json
from google.cloud import vision

def detect_text(filename, outfile):
    """
    Uses the google vision api to detect text in a png file. The text is written to a json file. The input must be
    a png file.
    @param filename: path to png file
    @param outfile: path to json file
    @returns None
    """
    if not os.path.exists(filepath):
        print("File does not exist")
        sys.exit(1)

    # if filepath is not png, exit
    if not filepath.endswith(".png"):
        print("File must be a png")
        sys.exit(1)

    try:
        client = vision.ImageAnnotatorClient()
        with open(filename, "rb") as image_file:
            content = image_file.read()
        image = vision.Image(content=content)
        response = client.text_detection(image=image)
        # convert response to json
        texts = response.text_annotations
        data = {"responses": [{"fullTextAnnotation": {"text": texts[0].description}}]}
        with open(outfile, "w") as f:
            json.dump(data, f, indent=4)

    except Exception as e:
        print("Error running gcloud command", e)
        sys.exit(1)


################## TESTING ##################
if __name__ == "__main__":
    # set command line argument file path
    if len(sys.argv) < 3:
        print("Please provide a file path")
        sys.exit(1)

    filepath = sys.argv[1]
    outfile = sys.argv[2]

    detect_text(filepath, outfile)

