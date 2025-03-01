import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';

const socket = io('http://localhost:5000');

function App() {
  const [user, setUser] = useState(null);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');

  // Вход
  const login = async (username, password) => {
    const response = await fetch('/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password }),
    });
    const data = await response.json();
    if (data.user_id) {
      setUser(data);
      socket.emit('join', data.user_id);
    }
  };

  // Отправка сообщения
  const sendMessage = (receiver_id, message) => {
    socket.emit('message', { sender_id: user.user_id, receiver_id, message });
  };

  // Получение сообщений
  useEffect(() => {
    socket.on('message', (data) => {
      setMessages((prev) => [...prev, data]);
    });
  }, []);

  return (
    <div>
      <h1>Мой Telegram</h1>
      {!user ? (
        <div>
          <input type="text" placeholder="Логин" />
          <input type="password" placeholder="Пароль" />
          <button onClick={() => login('username', 'password')}>Войти</button>
        </div>
      ) : (
        <div>
          <div>
            {messages.map((msg, index) => (
              <div key={index}>
                <strong>{msg.sender_id}</strong>: {msg.message}
              </div>
            ))}
          </div>
          <input value={input} onChange={(e) => setInput(e.target.value)} />
          <button onClick={() => sendMessage(2, input)}>Отправить</button>
        </div>
      )}
    </div>
  );
}

export default App;
