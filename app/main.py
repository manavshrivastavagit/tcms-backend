from fastapi import FastAPI
import uvicorn
from api.api import app 



if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)