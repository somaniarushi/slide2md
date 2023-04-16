import openai
import numpy as np

def compare_texts(text1, text2):
    """
    Acccepts two strings of text and returns the cosine similarity between them.
    Uses the text-embedding-ada-002 model from OpenAI.
    @param text1: string of text
    @param text2: string of text
    @return: cosine similarity between text1 and text2
    """
    # Create embeddings of text and last_text
    # If they are similar, do not convert to markdown
    text1_embed = np.array(openai.Embedding.create(
        input = text1,
        model="text-embedding-ada-002"
    )['data'][0]['embedding'])
    text2_embed = np.array(openai.Embedding.create(
        input = text2,
        model="text-embedding-ada-002"
    )['data'][0]['embedding'])
    # Compute cosine similarity
    cos_sim = np.dot(text1_embed, text2_embed) / (np.linalg.norm(text1_embed) * np.linalg.norm(text2_embed))
    return cos_sim