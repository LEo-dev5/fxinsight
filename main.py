from fastapi import FastAPI
from fastapi.responses import FileResponse
from routers import rates

app = FastAPI()

app.include_router(rates.router, prefix="/api")

@app.get("/")
def read_index():
    return FileResponse("static/index.html")