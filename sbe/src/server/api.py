# All these libraries will need to be downloaded via pip
from fastapi import FastAPI
from fastapi import Query
from fastapi.middleware.cors import CORSMiddleware
import dataprocessing as dp
import pandas
from models import Paper

app = FastAPI()

# Allow CORS for all origins (for development purposes only)
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["GET"],
    allow_headers = ["*"],
)

data = dp.dataPreProcessing()


def formatDFtoPaper(df: pandas.DataFrame) -> list[Paper]:
    papersList = []
    lenPara1 = 50
    for _ , row in df.iterrows():
        papersList.append(Paper(
            title = row["Title"],
            url = row["Link"],
            paperID = row["id"],

            # Getting the first 200 words of the first paragraph of the content
            contentPara1 = " ".join(row["ContentPara1"].split()[:lenPara1]) + "..."
        ))
    return papersList

# Test root path
@app.get("/hello")
def root_path():
    return {"message": "Hello World"}

@app.get("/papers")
async def root(searchQuery: str = "", searchNum: int = 4):
    if searchNum > 15:
        searchNum = 15
    
    matchedPapers = dp.findSearchMatch(searchQuery, data, searchNum)
    matchedPapers = matchedPapers.drop(columns = ["Embedding", "Similarity"])
    
    matchedPapers["Content"] = matchedPapers["Link"].apply(dp.scrapePaper)

    matchedPapers["ContentPara1"] = matchedPapers["Content"].apply(lambda x: x[0] if len(x) > 0 else "")

    # Line to generate a summary of text
    # matchedPapers["Summary"] = matchedPapers["Content"].apply(dp.summarizeText)

    return formatDFtoPaper(matchedPapers)
    
@app.get("/summary")
async def summarize_paper(link: str = Query(..., description = "URL of the paper to summarize")):
    content = dp.scrapePaper(link)
    fullText = " ".join(content)

    # Using the summarisation function from ChatGPTFunctions class
    summary = dp.ChatGPTFunctions.summarizeText(fullText)

