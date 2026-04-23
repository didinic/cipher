from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import db
import vigenere

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/users")
def get_users():
    data = db.read_json()
    return data["users"]


@app.get("/comments")
def get_users():
    data = db.read_json()
    return data["comments"]

@app.get("/txt2vigenere/{text}/{key}")
def txt2vigenere(text: str, key: str):
    encoded_text = vigenere.vigenere_encode(text, key)
    return {"encoded_text": encoded_text}

@app.get("/vigenere2txt/{ciphertext}/{key}")
def vigenere2txt(ciphertext: str, key: str):
    decoded_text = vigenere.vigenere_decode(ciphertext, key)
    return {"decoded_text": decoded_text}
