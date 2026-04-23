from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import db
import vigenere
import caesar
from fastapi import HTTPException


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LoginRequest(BaseModel):
    username: str
    password: str

class CommentRequest (BaseModel): 
    comment: str
    author: str
    key: str

class DecryptRequest (BaseModel):
    comment_id: str
    key: str

#guest
@app.get("/txt2vigenere/{text}/{key}")
def txt2vigenere(text: str, key: str):
    return {"result": vigenere.vigenere_encode(text, key, encode=True)}

@app.get("/vigenere2txt/{text}/{key}")
def vigenere2txt(text: str, key: str):
    return {"result": vigenere.vigenere_encode(text, key, encode=False)}

@app.get("/txt2caesar/{text}/{shift}")
def txt2caesar(text: str, shift: int):
    return {"result": caesar.encode_caesar(text, shift)}

@app.get("/caesar2txt/{text}/{shift}")  
def caesar2txt(text: str, shift: int):
    return {"result": caesar.decode_caesar(text, shift)}

@app.get("/txt2vigenere/{text}/{key}")
def txt2vigenere(text: str, key: str):
    encoded_text = vigenere.vigenere_encode(text, key)
    return {"encoded_text": encoded_text}

@app.get("/vigenere2txt/{ciphertext}/{key}")
def vigenere2txt(ciphertext: str, key: str):
    decoded_text = vigenere.vigenere_decode(ciphertext, key)
    return {"decoded_text": decoded_text}

#login
@app.post("/login")
def login_user(data: LoginRequest):
    username = data.username
    password = data.password

    data_db = db.read_json()

    for user in data_db["users"].values():
        if user["username"] == username and user["password"] == password:
            return {
                "message": "login successful",
                "username": user["username"],
                "friends_user": user["user_friends"]
            }

    raise HTTPException(
        status_code=401,
        detail="User doesn't exist or invalid credentials"
    )


#social-media
@app.get("/users")
def get_users():
    data = db.read_json()
    return data["users"]

@app.get("/comments")
def get_comments():
    data = db.read_json()
    return data["comments"]

@app.post("/comment")
def create_comment_encrypt (data: CommentRequest): 
    
    comment = data.comment
    key = data.key
    author = data.author
    
    data = db.read_json()
    encrypt_message = vigenere.vigenere_encode(comment, key, True)
    new_id = len(data["comments"]) + 1
    comment_key = f"comment{new_id}"
    new_comment = {
        "id": str(new_id),
        "author": author,
        "plain_text": comment, 
        "encrypt_text":encrypt_message
    }

    data["comments"][comment_key] = new_comment

    db.write_json(data)
    
    return {
        "message": "ok"
    } 

    

@app.post("/decrypt")
def decrypt_comment (data: DecryptRequest):
    
    comment_id = data.comment_id
    key = data.key
    
    data = db.read_json()
    
    for comment in data["comments"].values():
        if comment["id"] == comment_id:
            comment_crypt = comment["encrypt_text"]
            comment_decrypt = vigenere.vigenere_encode (comment_crypt, key, False)
            return comment_decrypt
                    
    return {

        "message": "not found"
    } 


