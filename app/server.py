from starlette.responses import Response

from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
import json

app = FastAPI(
    title="French Box Office",
    description="""Predict how much sales make a movie on the first week""",
    version="0.1.0",
)

class Data(BaseModel):
    user: str


@app.get("/")
def read_root():
    return {"message": "Welcome from the API"}

    
@app.post("/predict")
def get_prediction(data: Data):
    """Predict movies"""
    res = f"hello {data.user}"
    return res


if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8080)    