from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from sql import *

import uvicorn

class NameSearch(BaseModel):
    category: str
    objects: str 
    name: str
    
class NumSearch(BaseModel):
    category: str
    objects: str
    minimum: int
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
    
    if item.minimum < 0 or item.maximum < 0:
        return {'status': -1, 'details': '數值不得小於零'}
    
    if item.minimum > item.maximum:
        return {'status': -1, 'details': '最小值不得大於最大值'}
    
    try:
    
        if item.category == '任務':       
            return {'status': 200, 'details': callQuest(['', ''], ['總經驗值', item.minimum, item.maximum])}
            
        else:
            
            stmt = f'WHERE {item.objects} BETWEEN {item.minimum} AND {item.maximum}'
            
            if item.category == '裝備':
                return {'status': 200, 'details': callGear([stmt, stmt])}
                        
            elif item.category == 'NPC':
                return {'status': 200, 'details': callNPC(stmt)}
                
            elif item.category == '怪物':
                return {'status': 200, 'details': callMonster(stmt)}
                
    except Exception as e:
        return {'status': -1, 'details': e}
    
    
@app.post('/data/search_by_name')
async def nameQuery(item: NameSearch):
    
    if len(item.name) <= 0:
        return {'status': -1, 'details': '名稱不得為空'}
    
    if item.name[0] == ' ':
        return {'status': -1, 'details': '名稱開頭不得為空'}
    
    
    if item.category == '任務':
        
        subQuery = []
        target = []
        
        if '任務' in item.objects:
            stmt = f"WHERE 任務名稱 LIKE '%{item.name}%' OR 前置任務 LIKE '%{item.name}%'"
            subQuery += [stmt, stmt]
            target += ['', '']
        else:
            subQuery += ['', '']
            target += [item.objects, item.name]
        
        try:
            return {'status': 200, 'details': callQuest(subQuery, target)}
        except Exception as e:
            return {'status': -1, 'details': e}
        
    else:
        stmt = f"WHERE {item.objects} LIKE '%{item.name}%'"
        
        try:
            if item.category == '裝備':
                
                if 'NPC' in item.objects:
                    return {'status': 200, 'details': callGear([stmt, ''])}
                elif '怪物' in item.objects:
                    return {'status': 200, 'details': callGear(['', stmt])}
                else:
                    return {'status': 200, 'details': callGear([stmt, stmt])}
                    
            elif item.category == 'NPC':
                return {'status': 200, 'details': callNPC(stmt)}
                
            elif item.category == '怪物':
                return {'status': 200, 'details': callMonster(stmt)}
            
            else:
                return {'status': -1, 'details': 'error occur'}
                
        except Exception as e:
            return  {'status': -1, 'details': e}
        
    
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)