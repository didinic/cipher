from fastapi import FastAPI
import db
import vigenere
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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




