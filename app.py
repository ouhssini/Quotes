import json
from collections import defaultdict

from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel

import random

app = FastAPI()
# Load quotes from the quotes.json file
with open("quotes.json", "r", encoding="utf-8") as file:
    quotes = json.load(file)


class Quote(BaseModel):
    id: int
    quote: str
    author: str


@app.get("/random-quotes/{count}")
def get_random_quotes(count: int):
    if not quotes:
        raise HTTPException(status_code=404, detail="No quotes available")

    if count <= 0:
        raise HTTPException(status_code=400, detail="Count must be greater than zero")

    if count >= len(quotes):  # Use >= to return all quotes if count is greater or equal to the total
        formatted_quotes = jsonable_encoder(quotes)
    else:
        selected_quotes = random.sample(quotes, count)
        formatted_quotes = jsonable_encoder(selected_quotes)

    # Return the formatted JSON response
    return JSONResponse(content=formatted_quotes, media_type="application/json")



@app.get("/random-quote")
def get_single_random_quote():
    if not quotes:
        raise HTTPException(status_code=404, detail="No quotes available")

    # Select a single random quote
    random_quote = random.choice(quotes)

    # Use jsonable_encoder to ensure proper JSON encoding
    formatted_quote = jsonable_encoder(random_quote)

    # Return the formatted JSON response
    return JSONResponse(content=formatted_quote, media_type="application/json")


@app.get("/quotes-by-author/{author_name}")
def get_quotes_by_author(author_name: str):
    # Use a case-insensitive comparison for author names
    filtered_quotes = [quote for quote in quotes if quote["author"].lower() == author_name.lower()]

    if not filtered_quotes:
        raise HTTPException(status_code=404, detail=f"No quotes found for author: {author_name}")

    formatted_quotes = jsonable_encoder(filtered_quotes)

    return JSONResponse(content=formatted_quotes, media_type="application/json")


@app.get("/authors")
def get_authors_with_quote_count():
    # Use defaultdict to count the number of quotes per author
    author_count = defaultdict(int)
    for quote in quotes:
        author_count[quote["author"]] += 1

    # Convert the defaultdict to a list of dictionaries for JSON response
    authors_with_count = [{"author": author, "quote_count": count} for author, count in author_count.items()]

    formatted_authors = jsonable_encoder(authors_with_count)
    return JSONResponse(content=formatted_authors, media_type="application/json")