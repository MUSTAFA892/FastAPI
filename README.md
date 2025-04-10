### FastAPI Overview

FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.8+ based on standard Python type hints. It’s built on top of Starlette for the web parts and Pydantic for the data parts.

#### Key Features of FastAPI:
- **Fast**: Very high performance, on par with NodeJS and Go (thanks to Starlette and Pydantic).
- **Easy**: It’s easy to use and learn, with automatic interactive API documentation provided via Swagger UI and ReDoc.
- **Type Hints**: It uses Python type hints, making it easier to work with and reducing errors.

### Example of How FastAPI Works:

Here’s a simple example of how FastAPI works using type hints.

```python
from typing import Union
from fastapi import FastAPI

# Create an instance of the FastAPI class
app = FastAPI()

# Basic route that returns a simple dictionary
@app.get("/")
def read_root():
    return {"Hello": "World"}

# Route with path parameter and optional query parameter
@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
```

### Explanation of Code:

1. **Create an app instance**:
   - `app = FastAPI()` creates an instance of the FastAPI application.

2. **Path Operations**:
   - `@app.get("/")` defines a route for HTTP GET requests to the root path `/`.
   - `@app.get("/items/{item_id}")` defines a route for HTTP GET requests with a path parameter `item_id`. It can also accept an optional query parameter `q` (which could either be a string or `None`).

3. **Path Parameters**:
   - In the second route, `item_id` is a **path parameter**. It's specified inside curly braces `{}` in the URL, and FastAPI automatically maps it to the function's argument.
   
4. **Query Parameters**:
   - `q` is a **query parameter**, which is optional (`Union[str, None]` means it can either be a string or `None`). You can pass it like `/items/42?q=test`.

5. **Return Value**:
   - FastAPI automatically converts the return values into JSON. In this case, it returns a dictionary, which FastAPI will convert into a JSON object when the response is sent.

### Your FastAPI Notes App

Now, let's break down your Notes app based on FastAPI and MongoDB.

#### Basic Structure of the Notes App (How FastAPI Integrates):

1. **Create the FastAPI instance**:
   - We initialize `FastAPI()` just like in the example above, which is the core of the application.

2. **Define Routes for Note Operations**:
   - **Adding Notes**: A route that allows users to add a new note with title, description, and an "important" checkbox.
   - **Viewing Notes**: A route to display all notes stored in the MongoDB database.

#### FastAPI Notes App with MongoDB and Bootstrap: (Basic Flow)

```python
from typing import List, Union
from fastapi import FastAPI, Form, Request
from pymongo import MongoClient
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
from dotenv import load_dotenv

# Load environment variables (for MongoDB URI)
load_dotenv()

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client.notes_db
notes_collection = db.notes

# FastAPI app instance
app = FastAPI()

# Serve static files (like CSS, images)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Template renderer
templates = Jinja2Templates(directory="templates")

# Define Pydantic model for notes
class Note(BaseModel):
    title: str
    description: str
    important: bool

# Route to display all notes
@app.get("/", response_class=HTMLResponse)
async def get_notes(request: Request):
    notes = list(notes_collection.find())  # Fetch notes from MongoDB
    return templates.TemplateResponse("index.html", {"request": request, "notes": notes})

# Route to add a note
@app.post("/add_note/")
async def add_note(request: Request, title: str = Form(...), description: str = Form(...), important: bool = Form(False)):
    note = {"title": title, "description": description, "important": important}
    notes_collection.insert_one(note)
    return templates.TemplateResponse("index.html", {"request": request, "notes": list(notes_collection.find())})
```

### Key Concepts and Implementation:

1. **MongoDB Integration**:
   - MongoDB is used to store the notes. We connect to MongoDB using `MongoClient` and fetch the notes from the `notes` collection.
   
2. **Jinja2 Templates**:
   - FastAPI uses Jinja2 templates to render HTML dynamically. In this case, `index.html` is the template that renders the list of notes.
   
3. **Frontend (Bootstrap)**:
   - Bootstrap is used to make the frontend user-friendly. It provides responsive layouts, forms, buttons, etc.

### Conclusion:

FastAPI is an excellent choice for building high-performance web applications or APIs. It automatically handles data validation using Pydantic models, serves interactive API documentation, and integrates well with databases like MongoDB.

For your Notes App:
- You define routes for creating and viewing notes.
- The backend uses MongoDB to persist notes.
- The frontend uses Bootstrap to make the app visually appealing and responsive.

To run your FastAPI project, you'll need to follow these steps:

### 1. **Set Up the Environment (Virtual Environment)**

#### Step 1: Create a Virtual Environment
A virtual environment helps you isolate your project dependencies.

- **On Windows**:

```bash
python -m venv venv
```

- **On macOS/Linux**:

```bash
python3 -m venv venv
```

#### Step 2: Activate the Virtual Environment
After creating the virtual environment, activate it:

- **On Windows**:

```bash
.\venv\Scripts\activate
```

- **On macOS/Linux**:

```bash
source venv/bin/activate
```

After activating, you'll see the `(venv)` prefix in your terminal, indicating that the virtual environment is active.

### 2. **Install Dependencies**

Now that you have your virtual environment set up, you need to install the required dependencies.

Create a file named `requirements.txt` with the following contents:

```txt
fastapi==0.95.1
uvicorn==0.18.2
pymongo==4.3.3
jinja2==3.1.2
python-dotenv==0.21.0
```

#### Install the dependencies:

```bash
pip install -r requirements.txt
```

This will install all the necessary libraries for FastAPI, MongoDB integration, template rendering, etc.

### 3. **Set Up MongoDB URI**

In the root directory of your project, create a `.env` file to store your MongoDB connection URI securely.

Create a file named `.env` with the following content:

```bash
MONGO_URI=mongodb://localhost:27017/notes_db
```

This tells FastAPI where to connect to MongoDB. If you're using MongoDB Atlas (cloud database), you'll need to replace the value with your MongoDB URI provided by Atlas.

### 4. **Run the Application with Uvicorn**

Now you're ready to run your FastAPI app.

1. Make sure your **virtual environment** is still active.
2. Run the FastAPI application with Uvicorn. In your terminal, navigate to the directory where `index.py` (or `main.py`) is located and run:

```bash
uvicorn index:app --reload
```

Here’s what each part of the command means:
- `uvicorn`: The ASGI server used to run the app.
- `app.main:app`: Tells Uvicorn to look for the FastAPI app instance in the `main.py` file inside the `app` folder. (`app.main` refers to the `main.py` file inside the `app` directory, and `app` refers to the FastAPI instance inside that file).
- `--reload`: Enables auto-reloading of the server whenever code changes (useful during development).

### 5. **Verify the Application**

Once Uvicorn starts, you should see an output like this:

```bash
INFO:     Will watch for changes in these directories: ['./app']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

This means your FastAPI app is running locally at `http://127.0.0.1:8000`.

1. **Access the API docs**: FastAPI automatically generates interactive API documentation. You can access it by visiting:
   - Swagger UI: `http://127.0.0.1:8000/docs`
   - ReDoc: `http://127.0.0.1:8000/redoc`

2. **Access the Notes App**: If you open your browser and go to `http://127.0.0.1:8000`, you should see your Notes App running, where you can add and view notes.

### 6. **Stopping the Server**

To stop the FastAPI server, press `CTRL+C` in your terminal.

---

### Summary of Commands:

1. Create and activate the virtual environment:
   - `python -m venv venv`
   - `source venv/bin/activate` (macOS/Linux) or `.\venv\Scripts\activate` (Windows)

2. Install dependencies:
   - `pip install -r requirements.txt`

3. Create a `.env` file for MongoDB URI.

4. Run the FastAPI app:
   - `uvicorn index:app --reload`

5. Visit the app at `http://127.0.0.1:8000` in your browser.

---
