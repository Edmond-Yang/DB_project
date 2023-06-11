import sqlite3

conn = sqlite3.connect('data.db')
cursor = conn.cursor()

def swap(l: list, a: int, b: int):
    l[a], l[b] = l[b], l[a]
    return l  

def callQuest(subStmt: list, target: list):
    
    query = []
    
    stmt = "SELECT * FROM 任務 JOIN NPC ON 接收NPC = NPC名稱 OR 回報NPC = NPC名稱 NATURAL JOIN 任務詳細 " + subStmt[0]
    temp = executeQuery(stmt)
    
    for cnt in range(0, len(temp), 4):
        
        t = temp[cnt][:]
        
        t = swap(t, 2, 6)
        t = swap(t, 6, 5)
        
        t += temp[cnt+3][-2:]
        t[6] = temp[cnt+3][-3]
        
        query.append(t)
        
    print(query)
    
    stmt = "SELECT 任務名稱, 所在地圖, 經驗值 FROM 任務 NATURAL JOIN 任務詳細 NATURAL JOIN 怪物 " + subStmt[1]
    temp = executeQuery(stmt)
    
    print(temp)
    
    for cnt in range(0, len(temp), 2):
            query[cnt//2] += temp[cnt][1:] + temp[cnt+1][1:]
            
    for cnt in range(len(query)):
        total = query[cnt][4] + query[cnt][8]*query[cnt][12]+query[cnt][10]*query[cnt][14]
        query[cnt].append(total)
        
    test = query[:]
    query = []
        
    if target[0] == '怪物':
        for t in test:
            if target[1] in t[7] or target[1] in t[9]:
                query.append(t)
    elif target[0] == 'NPC':
        for t in test:
            if target[1] in t[1] or target[1] in t[5]:
                query.append(t)
    elif target[0] == '總經驗值':
        for t in test:
            if t[-1] >= target[1] and t[-1] <= target[2]:
                query.append(t)
        query.sort(key=lambda x : x[-1], reverse=True)
    else:
        query = test
        
    print('-'*20)
    print(query)
    
    table = ''
    for q in query:
        table+='''
        <tr>
            <th rowspan="2">{}</th>
            <th>{}</th>
            <th>{}</th>
            <th>{}</th>
            <th>{}</th>
            <th>{}</th>
            <th rowspan="2">{}</th>
            <th rowspan="2">{}</th>
            <th rowspan="2">{}</th>
        </tr>
        <tr>
            <th>{}</th>
            <th>{}</th>
            <th>{}</th>
            <th>{}</th>
            <th>{}</th>
        </tr>
        '''.format(q[0], q[1], q[2], q[7], q[11], q[8], q[3], q[4], q[-1], q[5], q[6], q[9], q[12], q[10])
    
    return table

    
def callGear(subStmt: list):
    
    stmt = "SELECT 裝備名稱, 來源NPC名稱, 所在地圖, 裝備.攻擊力, 玩家需求等級 FROM 裝備 JOIN NPC ON NPC名稱 = 來源NPC名稱 " + subStmt[0]
    query = executeQuery(stmt)
    
    for q in query:
        q.insert(1, 'NPC')
    
    stmt = "SELECT 裝備名稱, 來源怪物名稱, 所在地圖, 來源怪物名稱, 裝備.攻擊力, 玩家需求等級 FROM 裝備 JOIN 怪物 ON 來源怪物名稱 = 怪物名稱 " + subStmt[1]
    temp = executeQuery(stmt)
    
    for t in temp:
        t.insert(1, '怪物')
        
    query += temp
    
    choice = None
    for cnt, attr in enumerate(['裝備.攻擊力', '玩家需求等級']):
        
        if attr in subStmt[0] or attr in subStmt[1]:
            choice = cnt+4
            break
        
    if choice is not None:
        query.sort(key=lambda x : x[choice], reverse=True)
        
    print(query)
    
    table = ''
    for q in query:
        table += '<tr>'
        
        for obj in q:
            table += '<td>' + str(obj) + '</td>'
            
        table += '</tr>'
    
    return table
    

def callMonster(subStmt: str):
    
    stmt = "SELECT 怪物名稱, 所在地圖, 等級, 血量, 怪物.攻擊力, 防禦力, 經驗值, 裝備名稱 FROM 怪物 JOIN 裝備 ON 來源怪物名稱 = 怪物名稱 " + subStmt
    temp = executeQuery(stmt)
    
    choice = None
    for cnt, attr in enumerate(['等級', '血量', '怪物.攻擊力', '防禦力', '經驗值']):
        
        if attr in subStmt:
            choice = cnt+2
            break
        
    if choice is not None:
        temp.sort(key=lambda x : x[choice], reverse=True)
    
    table = ''
    for t in temp:
        table += '<tr>'
        
        for obj in t:
            table += '<td>' + str(obj) + '</td>'
            
        table += '</tr>'
    
    return table
    

def callNPC(subStmt: str):
    
    stmt = "SELECT NPC名稱, 所在地圖, 裝備名稱 FROM NPC JOIN 裝備 ON 來源NPC名稱 = NPC名稱 " + subStmt
    temp = executeQuery(stmt)
    
    table = ''
    for t in temp:
        table += '<tr>'
        
        for obj in t:
            table += '<td>' + str(obj) + '</td>'
            
        table += '</tr>'
    
    return table


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
    callQuest(["WHERE 任務名稱 LIKE '%古代神之聖所在%' OR 前置任務 LIKE '%古代神之聖所在%'","WHERE 任務名稱 LIKE '%古代神之聖所在%' OR 前置任務 LIKE '%古代神之聖所在%'"], ['', ''])
    # callGear(['', ''])
    # callNPC([''])
    # callMonster([''])