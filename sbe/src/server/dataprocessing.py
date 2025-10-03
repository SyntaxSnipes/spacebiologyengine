# All these libraries will need to be installed via pip
from dotenv import load_dotenv
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
from openai import OpenAI
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("Missing OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

# Function to create word embeddings (Vectors used to represent words as numerical values) using OpenAI API
def makeWordEmbeddings(text: str):
    response = client.embeddings.create(
        input = text,
        model = "text-embedding-3-small"
    )
    return response.data[0].embedding

class ChatGPTFunctions:
    # Summarise text using ChatGPT
    def summarizeText(text: str):
        response = client.chat.completions.create(
            model = "gpt-3.5-turbo",
            messages = [{"role": "user", "content": f"Summarize the following text into 5 bullet points in a concise, precise manner:\n{text}"}]
        )
        return response.choices[0].message.content

    #def answerQuery(text: str, query: str)



# Funtcion to check how similar to words are using their embeddings
def wordSimilarity(wordEmbedding1: list[float], wordEmbedding2: list[float]) -> float:
    return np.dot(wordEmbedding1, wordEmbedding2) / (np.linalg.norm(wordEmbedding1) * np.linalg.norm(wordEmbedding2))


# Function to get all the text from a paper given its URL
def scrapePaper(paperUrl: str, sectionFilter: str = ""):
    headerData = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(paperUrl, headers = headerData)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')

    # Possible section id's, that could contain paper content in the HTML of the website
    possibleSections = [f"abstract{i}"
                        for i in range(11)]
    
    possibleSections.extend([f"Abs{i}"
                             for i in range(11)])

    possibleSections.extend([f"Sec{i}"
                             for i in range(100)])
    
    possibleSections.extend([f"sec{i}"
                             for i in range(100)])

    possibleSections.extend([f"s{i}"
                             for i in range(100)])
    

    textContent = []
    
    tags = soup.find_all(id = possibleSections)
    for tag in tags:
        paragraphs = tag.find_all("p")

        for para in paragraphs:
            textContent.append(para.get_text())
    
    return textContent


# Search through the database for the most relevant papers given a query
# Using embeddings and cosine similarity
def findSearchMatch(query, paperDF, topMatches = 4) -> pd.DataFrame:
    queryEmbedding = makeWordEmbeddings(query)
    paperDF["Similarity"] = paperDF["Embedding"].apply(lambda x: wordSimilarity(eval(x), queryEmbedding))

    paperDF.sort_values("Similarity", ascending = False, inplace = True)
    return paperDF.head(topMatches)

# Function to set up the database with all the embeddings for the titles
def dataPreProcessing() -> pd.DataFrame:
    data = pd.read_csv("SB_publication_PMC.csv")

    # Load the file for word embeddings and add it to the dataframe
    try:
        with open("title_embeddings.csv", "r") as embeddingsFile:
            embeddingsData = pd.read_csv(embeddingsFile)
            data["Embedding"] = embeddingsData["Embedding"]

    
    # If file with embeddings for titles doesn't exist, create it
    except:
        data["Embedding"] = data["Title"].apply(makeWordEmbeddings)
        with open("title_embeddings.csv", "w") as embeddingsFile:
            embeddingsFile.write(data.to_csv(index = False))

    data["id"] = data.index

    return data
