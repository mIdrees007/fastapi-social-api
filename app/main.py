from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware
models.Base.metadata.create_all(bind=engine)
app = FastAPI()
#orgins = ["*"] all domain public
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "https://www.google.com"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # what domain should be allowed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def root():
    return {"message": "Hello World"}
