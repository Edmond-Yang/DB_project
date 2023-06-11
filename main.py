from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

import uvicorn

class NameSearch(BaseModel):
    category: str
    objects: str 
    name: str
    
class NumSearch(BaseModel):
    category: str
    objects: str
    mininum: int
    maximum: int
    

app = FastAPI(
    title='DB project'
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")



@app.get('/', response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse("home page.html",{'request':request})

@app.get('/{category}', response_class=HTMLResponse)
async def htmlQuery(category: str, request: Request):
    return templates.TemplateResponse(f"{category} page.html",{'request':request})

@app.post('/data/search_by_num')
async def numQuery(item: NumSearch):
    
    if item.mininum < 0 or item.maximum < 0:
        return {'status': -1, 'details': '數值不得小於零'}
    
    if item.mininum > item.maximum:
        return {'status': -1, 'details': '最小值不得大於最大值'}
    
    
    pass

@app.post('/data/search_by_name')
async def nameQuery(item: NameSearch):
    
    if len(item.name) <= 0:
        return {'status': -1, 'details': '名稱不得為空'}
    
    if item.name[0] == ' ':
        return {'status': -1, 'details': '名稱開頭不得為空'}
    pass



    

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8080)