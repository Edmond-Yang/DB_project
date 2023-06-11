import sqlite3

conn = sqlite3.connect('data.db')
cursor = conn.cursor()

def swap(l: list, a: int, b: int):
    l[a], l[b] = l[b], l[a]
    return l  

def callQuest(subStmt: str):
    
    query = []
    
    stmt = "SELECT * FROM 任務 JOIN NPC ON 接收NPC = NPC名稱 OR 回報NPC = NPC名稱 NATURAL JOIN 任務詳細"
    temp = executeQuery(stmt)
    
    for cnt in range(0, len(temp), 4):
        
        t = temp[cnt][:]
        
        t = swap(t, 2, 6)
        t = swap(t, 6, 5)
        
        t += temp[cnt+3][-2:]
        t[6] = temp[cnt+3][-3]
        
        query.append(t)
    
    stmt = "SELECT 任務名稱, 所在地圖, 經驗值 FROM 任務 NATURAL JOIN 任務詳細 NATURAL JOIN 怪物"
    temp = executeQuery(stmt)
    
    print(query[0:5])
    
    # for cnt in range(0, len(temp), 2):
    #     query[cnt//2] += temp[cnt] + temp[cnt+1]
        
    # for cnt in range(len(query)):
    #     total = query[cnt][4] + query[cnt][8]*query[cnt][12]+query[cnt][10]*query[cnt][14]
    #     query[cnt].append(total)
    
    
    # query.sort(key=lambda x : x[-1], reverse=True)
    
    # print(query)
    



def executeQuery(stmt: str):

    new_rows = []
    cursor.execute(stmt)
    rows = cursor.fetchall()
    
    for r in rows:
        
        r = list(r)
        
        for cnt, obj in enumerate(r):
            if obj is None:
                r[cnt] = ''
            
        new_rows.append(r)
    
    return new_rows

if __name__ == '__main__':
    callQuest('')