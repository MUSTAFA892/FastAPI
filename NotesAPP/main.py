from typing import Union

from fastapi import FastAPI , Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles  import StaticFiles
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"),name="static")
templates = Jinja2Templates(directory="templates") 

# mongo db connection string
conn = MongoClient("mongodb+srv://mustafatinwala6:mustafa5253TINWALA@learningmongo.lof7x.mongodb.net/?retryWrites=true&w=majority&appName=LearningMongo")

@app.get("/",response_class=HTMLResponse)
async def read_root(request: Request):
    docs = conn.notes.notes.find({})
    newDocs = []
    for doc in docs:
        newDocs.append({
            "id":doc['_id'],
            "note":doc['note']
        })
    return templates.TemplateResponse("index.html", {'request':request, 'newDocs':newDocs})


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}