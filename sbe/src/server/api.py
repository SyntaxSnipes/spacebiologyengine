# All these libraries will need to be downloaded via pip
from fastapi import FastAPI
import dataprocessing as dp

app = FastAPI()

data = dp.dataPreProcessing()

# The Fast API "get" function will work on path /papers
@app.get("/papers")
async def root(searchQuery: str, searchNum: int = 1):
    papers = dp.findSearchMatch(searchQuery, data, searchNum)
    for papersLink in papers.loc[:, "Link"]:
        papersContent = dp.scrapePaper(papersLink)
    return papersContent

