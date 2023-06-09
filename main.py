from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import sqlite3, uvicorn

app = FastAPI(
    title='DB project'
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

conn = sqlite3.connect('data.db')
cursor = conn.cursor()

@app.get('/', response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse("home page.html",{'request':request})

@app.get('/{category}', response_class=HTMLResponse)
async def htmlQuery(category: str, request: Request):
    print(category)
    return templates.TemplateResponse(f"{category} page.html",{'request':request})

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8080)