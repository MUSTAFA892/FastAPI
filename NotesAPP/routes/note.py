from fastapi import APIRouter
from fastapi import FastAPI , Request
from fastapi.responses import HTMLResponse
from Models.note import Note
from fastapi.staticfiles  import StaticFiles
from fastapi.templating import Jinja2Templates
from config.db import conn
from schemas.note import noteEntity, notesEntity

note = APIRouter()
templates = Jinja2Templates(directory="templates") 



@note.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    docs = conn.notes.notes.find({})
    newDocs = []
    for doc in docs:
        newDocs.append({
            "id": str(doc.get('_id')),  # cast ObjectId to str
            "title": doc.get('title', 'No Title'),
            "desc": doc.get("desc", ''),
            "important": doc.get("important", False),
        })
    return templates.TemplateResponse("index.html", {'request': request, 'newDocs': newDocs})


@note.post("/")
async def added_item(request : Request):
    form = await request.form()
    formDict = dict(form)
    formDict["important"] = True if formDict.get("important") == "on" else False 
    note = conn.notes.notes.insert_one(formDict)
    return {"success" : True}


    