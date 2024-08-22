from fastapi import FastAPI, Request
from typing import Any, Dict
from fastapi import Body, FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

app = FastAPI(
    title="SAM Quote Giver",
    description="Get a real quote said by SAM himself.",
)

user_token_db = {"ABCDEF": "SAM"}

class Quote(BaseModel):
    quote: str = Field(
        description="The quote that SAM said.",
    )
    year: int = Field(
        description="The year when SAM said the quote.",
    )


@app.get(
    "/quote",
    summary="Returns a random quote by SAM",
    description="Upon receiving a GET request this endpoint will return a real quiote said by SAM himself.",
    response_description="A Quote object that contains the quote said by SAM and the date when the quote was said.",
    response_model=Quote,
)
def get_quote(request: Request):
    print(request.headers)
    return {
        "quote": "Life is short so eat it all.",
        "year": 1950,
    }


@app.get(
    "/authorize",
    response_class=HTMLResponse,
)
def handle_authorize(client_id: str, redirect_uri: str, state: str):
    return f"""
    <html>
        <head>
            <title>SAM Log In</title>
        </head>
        <body>
            <h1>Log Into SAM</h1>
            <a href="{redirect_uri}?code=ABCDEF&state={state}">Authorize SAM GPT</a>
        </body>
    </html>
    """


@app.post("/token")
def handle_token(code=Form(...)):
    return {
        "access_token": user_token_db[code]
    }