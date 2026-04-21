from fastapi import FastAPI
import db

app = FastAPI()


@app.get("/users")
def get_users():
    data = db.read_json()
    return data["users"]


@app.get("/comments")
def get_users():
    data = db.read_json()
    return data["comments"]

