import sys
import openai
import os


def text2markdown(text, outfile = None):
    """
    Accepts a string of text and converts it to markdown. If outfile is provided, the markdown is written to the file. Otherwise,
    the markdown is returned as a string.
    This function uses the OpenAI API to convert text to markdown.

    @param text: string of text to convert to markdown
    @param outfile: file to write markdown to
    @return: markdown as a string or None if outfile is provided
    """

    # Pass in google credentials "access.json"
    openai.api_key = os.environ["OPENAI_API_KEY"]
    prolog = "Given this text extracted from slides, convert it to markdown. It is important to ensure that none of the information is lost."

    # If the text is too long, we need to split it into chunks
    MAX_LEN = 2000
    if len(text) > MAX_LEN:
        chunks = [text[i:i + MAX_LEN] for i in range(0, len(text), MAX_LEN)]
    else:
        chunks = [text]

    repsonse_texts = []
    for chunk in chunks:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"{prolog}\n\n{chunk}\n\n---",
            temperature=0,
            max_tokens=500,
            top_p=1,
            frequency_penalty=0,
            stop=["---"],
        )
        repsonse_texts.append(response["choices"][0]["text"])

    response_text = "\n".join(repsonse_texts)

    if outfile is None:
        return response_text
    else:
        with open(outfile, "w") as f:
            f.write(response_text)


################### TESTING #########################
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Please provide a file name")
        sys.exit(1)

    filepath = sys.argv[1]
    outfile = sys.argv[2]

    with open(filepath) as f:
        text = f.read()
    text2markdown(text, outfile)