from typing import Any, Dict
from fastapi import Body, FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from pinecone import Pinecone
import os
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain_pinecone import PineconeVectorStore

load_dotenv()

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

embeddings = OpenAIEmbeddings()

vector_store = Pinecone.from_existing_index(
    "recipes",
    embeddings,
)


app = FastAPI(
    title="CheftGPT. The best provider of Indian Recipes in the world.",
    description="Give ChefGPT the name of an ingredient and it will give you multiple recipes to use that ingredient on in return.",
    servers=[
        {
            "url": "https://occupations-partition-governments-analyzed.trycloudflare.com",
        },
    ],
)


class Document(BaseModel):
    page_content: str


@app.get(
    "/recipes",
    summary="Returns a list of recipes.",
    description="Upon receiving an ingredient, this endpoint will return a list of recipes that contain that ingredient.",
    response_description="A Document object that contains the recipe and preparation instructions",
    response_model=list[Document],
    openapi_extra={
        "x-openai-isConsequential": False,
    },
)
def get_recipe(ingredient: str):
    docs = vector_store.similarity_search(ingredient)
    return docs


user_token_db = {"ABCDEF": "aaacccaa11231"}


@app.get(
    "/authorize",
    response_class=HTMLResponse,
    include_in_schema=False,
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


@app.post(
    "/token",
    include_in_schema=False,
)
def handle_token(code=Form(...)):
    return {
        "access_token": user_token_db[code],
    }