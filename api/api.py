from fastapi import FastAPI, HTTPException, Response, Query
from fastapi.responses import JSONResponse
from core.system import System
from core.multimedia import Multimedia

app = FastAPI()
sys = System()
multimedia = Multimedia()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.put("/api/v1/system/sleep", tags=["System"])
async def sleep():
    if not sys.invoke("sleep", type="sleep").succeded():
        raise HTTPException(status_code=500, detail="Failed to sleep")

    return JSONResponse(content={"status": "success"},
                        status_code=200)

@app.put("/api/v1/system/shutdown", tags=["System"])
async def shutdown():
    if not sys.invoke("sleep", type="sleep").succeded():
        raise HTTPException(status_code=500, detail="Failed to shutdown")

    return JSONResponse(content={"status": "success"},
                        status_code=200)

@app.put("/api/v1/multimedia/volume", tags=["Multimedia"])
async def volume(volume: float = Query(..., ge=0, le=100)):
    if not multimedia.invoke("volume", volume=volume).succeded():
        raise HTTPException(status_code=500, detail="Failed to set volume")

    return JSONResponse(content={"status": "success"},
                        status_code=200)

@app.put("/api/v1/multimedia/playpause", tags=["Multimedia"])
async def track_control(action: str = Query(..., description="The action to perform. Possible values are 'playpause', 'next', and 'prev'")):
    if not multimedia.invoke("track", action=action).succeded():
        raise HTTPException(status_code=500, detail="Failed to perform action")

    return JSONResponse(content={"status": "success"},
                        status_code=200)

def run():
    import uvicorn
    uvicorn.run(app, host="localhost", port=3000)