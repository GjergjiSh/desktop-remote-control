from fastapi import FastAPI, HTTPException, Response, Query
from fastapi.responses import JSONResponse
from core import system

app = FastAPI()
sys = system.System()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/api/v1/system/sleep", tags=["System"])
async def sleep():
    if sys.invoke("sleep") != 0:
        raise HTTPException(status_code=500, detail="Failed to sleep")

    return JSONResponse(content={"status": "success"},
                        status_code=200)

@app.get("/api/v1/system/shutdown", tags=["System"])
async def shutdown():
    if sys.invoke("shutdown") != 0:
        raise HTTPException(status_code=500, detail="Failed to shutdown")

    return JSONResponse(content={"status": "success"},
                        status_code=200)

def run():
    import uvicorn
    uvicorn.run(app, host="localhost", port=3000)