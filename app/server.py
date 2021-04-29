from starlette.responses import Response
from fastapi import FastAPI, HTTPException
import uvicorn
from pydantic import BaseModel


app = FastAPI(
    title="French Box Office",
    description="""Predict how much sales make a movie on the first week""",
    version="0.1.0",
)

class Data(BaseModel):
    movie_title: str


@app.get("/")
def read_root():
    return {"message": "Welcome from the API"}

    
@app.post("/predict")
def get_prediction(data: Data):
    """Predict movies"""


if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8080)    