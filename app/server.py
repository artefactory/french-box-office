# Copyright (C) 2020 Artefact
# licence-information@artefact.com

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

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