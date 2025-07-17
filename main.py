from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai

app = FastAPI()

# Allow frontend to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Request model
class CodeRequest(BaseModel):
    code: str
    task: str  # "explain" or "debug"
    language: str

# Configure GenAI
genai.configure(api_key="AIzaSyDHKICsg0eSoeaJUYvuu-HVhaljLkyn_6I")  # Replace with your Gemini API key
model = genai.GenerativeModel("gemini-2.5-flash")

@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/process/")
async def process_code(request: CodeRequest):
    prompt = f"Please {request.task} this {request.language} code:\n\n{request.code}"
    response = model.generate_content(prompt)
    return {"response": response.text}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Use Render's PORT or default to 8000
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
