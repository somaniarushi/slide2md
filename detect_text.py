import os
import sys

from google.cloud import vision

if __name__ == "__main__":
    # set command line argument file path
    if len(sys.argv) < 3:
        print("Please provide a file path")
        sys.exit(1)

    filepath = sys.argv[1]
    outfile = sys.argv[2]

    if not os.path.exists(filepath):
        print("File does not exist")
        sys.exit(1)

    # if filepath is not png, exit
    if not filepath.endswith(".png"):
        print("File must be a png")
        sys.exit(1)

    # run the following command in the terminal to set the environment variable
    # gcloud ml vision detect-text
    os.system(f"gcloud ml vision detect-text {filepath} > {outfile}")
