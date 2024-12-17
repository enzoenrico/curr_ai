from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from RAG import RAG

app = FastAPI()
ai_instance = RAG()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def main():
    ai_resp = ai_instance.query(
        "who is alex the terrible?", context="alex is a piece of shit human being"
    )
    return ai_resp


@app.post("/ai")
def talk2ai(query: str):
    # airesponse = ai_instance.query(query)
    # return airesponse
    return
