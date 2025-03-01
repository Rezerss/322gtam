from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
import sqlite3
from datetime import datetime
from cryptography.fernet import Fernet
import base64

# Генерация ключа для шифрования
key = Fernet.generate_key()
cipher_suite = Fernet(key)

app = FastAPI()

# Подключение к базе данных
conn = sqlite3.connect('messenger.db', check_same_thread=False)
cursor = conn.cursor()

# Создание таблиц
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    avatar TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender_id INTEGER NOT NULL,
    receiver_id INTEGER NOT NULL,
    message TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
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

class UserAvatar(BaseModel):
    avatar: str  # Base64-строка

# Регистрация пользователя
@app.post("/register")
def register(user: UserCreate):
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (user.username, user.password))
    conn.commit()
    return {"message": "User registered successfully"}

# Загрузка аватарки
@app.post("/upload_avatar/{user_id}")
async def upload_avatar(user_id: int, file: UploadFile = File(...)):
    file_content = await file.read()
    avatar_base64 = base64.b64encode(file_content).decode('utf-8')
    cursor.execute("UPDATE users SET avatar = ? WHERE id = ?", (avatar_base64, user_id))
    conn.commit()
    return {"message": "Avatar uploaded successfully"}

# Получение аватарки
@app.get("/get_avatar/{user_id}")
def get_avatar(user_id: int):
    cursor.execute("SELECT avatar FROM users WHERE id = ?", (user_id,))
    avatar = cursor.fetchone()
    if avatar and avatar[0]:
        return {"avatar": avatar[0]}
    raise HTTPException(status_code=404, detail="Avatar not found")

# Отправка сообщения (с шифрованием)
@app.post("/send_message")
def send_message(msg: MessageSend):
    encrypted_message = cipher_suite.encrypt(msg.message.encode())
    cursor.execute("INSERT INTO messages (sender_id, receiver_id, message) VALUES (?, ?, ?)",
                   (msg.sender_id, msg.receiver_id, encrypted_message))
    conn.commit()
    return {"message": "Message sent successfully"}

# Получение сообщений (с расшифровкой)
@app.get("/get_messages/{user_id}")
def get_messages(user_id: int):
    cursor.execute("SELECT * FROM messages WHERE receiver_id = ?", (user_id,))
    messages = cursor.fetchall()
    decrypted_messages = []
    for msg in messages:
        decrypted_msg = cipher_suite.decrypt(msg[3]).decode()
        decrypted_messages.append({
            "id": msg[0],
            "sender_id": msg[1],
            "receiver_id": msg[2],
            "message": decrypted_msg,
            "timestamp": msg[4]
        })
    return {"messages": decrypted_messages}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
