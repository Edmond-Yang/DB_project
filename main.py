from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import sqlite3
import uvicorn

class NameSearch(BaseModel):
    category: str 
    name: str
    
class NumSearch(BaseModel):
    category: str
    mininum: int
    maximum: int
    

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
    return templates.TemplateResponse(f"{category} page.html",{'request':request})

@app.post('/data/search_by_num')
async def numQuery(item: NumSearch):
    pass

@app.post('/data/search_by_name')
async def nameQuery(item: NameSearch):
    pass


def executeQuery(stmt: str):
    try:
        new_rows = []
        cursor.execute(stmt)
        rows = cursor.fetchall()
        
        for r in rows:
            new_rows.append(list(r))
            
        
    except Exception as e:
        
        return {'status': -1, 'details': e}
    
    
    
    return {'status': 200, 'details': new_rows}
    

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8080)