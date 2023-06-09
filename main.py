from fastapi import FastAPI
import sqlite3

app = FastAPI(
    title='DB project'
)

conn = sqlite3.connect('data.db')
cursor = conn.cursor()

@app.get('/')
def main():
    pass