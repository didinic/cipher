from fastapi import FastAPI
import db
import vigenere

app = FastAPI()


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
    return "User doesn't exist or invalid credentials"



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
def create_comment_encrypt (comment: str, key: str): 
    data = db.read_json()
    encrypt_message = vigenere.vigenere_encode(comment, key)
    new_id = len(data["comments"]) + 1
    comment_key = f"comment{new_id}"
    new_comment = {
        "id": str(new_id),
        "plain_text": comment, 
        "encrypt_text":encrypt_message
    }

    data["comments"][comment_key] = new_comment

    db.write_json(data)
    
    return "ok"

@app.post("/decrypt")
def decrypt_comment (key: str, comment_id: str):
    data = db.read_json()
    
    for comment in data["comments"].values():
        if comment["id"] == comment_id:
            comment_crypt = comment["encrypt_text"]
            comment_decrypt = vigenere.vigenere_decode (comment_crypt, key)
            return comment_decrypt
                    
    return "not found"



