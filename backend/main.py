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


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}