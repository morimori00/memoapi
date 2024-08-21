import uuid
from fastapi import FastAPI, HTTPException
from tinydb import TinyDB, Query
from pydantic import BaseModel

app = FastAPI()
db = TinyDB('db.json')

class SaveRequest(BaseModel):
    key: str = None
    data: str

@app.post("/save")
async def save_string(save_request: SaveRequest):
    key = save_request.key or str(uuid.uuid4())  # UUIDを生成
    key_with_data = key + save_request.data
    db.insert({'key': key, 'data': key_with_data})
    # POSTリクエストの返り値はなし
    return

@app.get("/")
async def get_string(key: str = None):
    if key:
        result = db.search(Query().key == key)
        if result:
            return {"key": key, "data": result[0]['data']}
        else:
            raise HTTPException(status_code=404, detail="Key not found")
    else:
        if len(db) == 0:
            raise HTTPException(status_code=404, detail="No data available")
        latest_entry = db.all()[-1]
        return {"key": latest_entry['key'], "data": latest_entry['data']}

@app.delete("/alldel")
async def delete_all():
    db.truncate()  # 全データを削除
    return {"message": "All data deleted successfully"}
