from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
from typing import List

app = FastAPI()

# Подключение к базе данных
conn = sqlite3.connect('messenger.db', check_same_thread=False)
cursor = conn.cursor()

# Создание таблиц
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender_id INTEGER NOT NULL,
    receiver_id INTEGER NOT NULL,
    message TEXT NOT NULL,
    FOREIGN KEY (sender_id) REFERENCES users (id),
    FOREIGN KEY (receiver_id) REFERENCES users (id)
)
''')
conn.commit()

# Модели данных
class UserCreate(BaseModel):
    username: str
    password: str

class MessageSend(BaseModel):
    sender_id: int
    receiver_id: int
    message: str

# Регистрация пользователя
@app.post("/register")
def register(user: UserCreate):
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (user.username, user.password))
    conn.commit()
    return {"message": "User registered successfully"}

# Отправка сообщения
@app.post("/send_message")
def send_message(msg: MessageSend):
    cursor.execute("INSERT INTO messages (sender_id, receiver_id, message) VALUES (?, ?, ?)",
                   (msg.sender_id, msg.receiver_id, msg.message))
    conn.commit()
    return {"message": "Message sent successfully"}

# Получение сообщений
@app.get("/get_messages/{user_id}")
def get_messages(user_id: int):
    cursor.execute("SELECT * FROM messages WHERE receiver_id = ?", (user_id,))
    messages = cursor.fetchall()
    return {"messages": messages}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="216.24.57.4", port=8000)
