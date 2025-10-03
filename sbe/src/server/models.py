from pydantic import BaseModel
from typing import List

class Paper(BaseModel):
    title: str
    url: str
    paperID: int
    contentPara1: str = ""
    

    