from fastapi import FastAPI
#CORS allows requests to be made to the API from a different domain than the API's domain.
from fastapi.middleware.cors import CORSMiddleware
from .routers import post, user, auth, vote

app = FastAPI()

origins = ["*"] #list of different domains that can make requests(all)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(post.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return "Hello World!"