from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional


app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published : bool = True
    rating: Optional[int] = None
    
    
    
@app.get("/")

async def root():
    return {"message": "Welcome to API, My first API  "}

@app.get("/posts")
def get_posts():
    return {"data": "this is you posts"}

@app.post("/posts")
def create_posts(post : Post):
    print(post.rating)
    print(post.model_dump())
    return {"data": post}
#title str, content str, category , BOOL published 