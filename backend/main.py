from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import db
import vigenere
import caesar

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

#login
@app.post("/login")
def login_user(username: str, password: str):
    data = db.read_json()
    for user in data["users"].values():
        if user["username"] == username and user["password"] == password :
            return {
                "message": "login successful",
                "username": user["username"], 
                "friends_user": user["user_friends"]
            }   
    return {

       "message": "User doesn't exist or invalid credentials"
        
    }

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
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

@app.get("/txt2vigenere/{text}/{key}")
def txt2vigenere(text: str, key: str):
    encoded_text = vigenere.vigenere_encode(text, key)
    return {"encoded_text": encoded_text}

@app.get("/vigenere2txt/{ciphertext}/{key}")
def vigenere2txt(ciphertext: str, key: str):
    decoded_text = vigenere.vigenere_decode(ciphertext, key)
    return {"decoded_text": decoded_text}
@app.post("/comment")
def create_comment_encrypt (comment: str, author: str, key: str): 
    data = db.read_json()
    encrypt_message = vigenere.vigenere_encode(comment, key)
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
def decrypt_comment (key: str, comment_id: str):
    data = db.read_json()
    
    for comment in data["comments"].values():
        if comment["id"] == comment_id:
            comment_crypt = comment["encrypt_text"]
            comment_decrypt = vigenere.vigenere_decode (comment_crypt, key)
            return comment_decrypt
                    
    return {

        "message": "not found"
    } 


