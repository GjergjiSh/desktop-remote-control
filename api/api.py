from fastapi import FastAPI
from core import system

app = FastAPI()
sys = system.System()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/api/v1/sleep")
async def sleep():
    sys.execute("sleep")

def run():
    import uvicorn
    uvicorn.run(app, host="localhost", port=3000)