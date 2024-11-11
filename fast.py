import asyncio
from fastapi import FastAPI
import uvicorn
app = FastAPI()
# To convert this to a webrtc server we need to call it from our normal server. 
# backend index.ts needs to create a websocket with this server can connect to it. 
@app.get("/")
async def read_root():
    return {"message": "demBoobiez"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)