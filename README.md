# Slide2MD
**Automatic Documentation Generation for Class Lectures** — An AI-powered slide-to-markdown file converter. 

## Running Locally
1. Run the following command:
```
pip install -r requirements.txt
```

2. Make a [service account](https://cloud.google.com/docs/authentication/application-default-credentials) for a GCloud project. You will get a `json` file as a key for the account. Set the environment variable `GOOGLE_APPLICATION_CREDENTIALS` to the path to that key. Here's how you do that on the command line:
```
export GOOGLE_APPLICATION_CREDENTIALS='path/to/access/creds.json'
```

3. Get an OpenAI API key. This should be a string. Set the environment variable `OPENAI_API_KEY` to that string. Here's how you do that on the command line:
```
export OPENAI_API_KEY="some_string_api"
```

4. Run the conversion process through `runner.py`. The process will create a `tmp` folder to host your temporary files, and create a markdown file with the same name as the input file.
```
python3 runner.py [filename]
```
More instructions about how to run the program can be found through
```
python3 runner.py --help
```

If you want your tmp to be auto-deleted after the run, use the `--clean-up` flag.

## Warning
This project is a work-in-progress. In all honesty, it **does not work very well**. I would not recommend anyone use this for production or commercial purposes.
