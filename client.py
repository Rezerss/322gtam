import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView

# Базовый URL сервера
BASE_URL = "http://216.24.57.4:8000"

class MessengerApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')
        self.chat_history = ScrollView(size_hint=(1, 0.8))
        self.chat_label = Label(size_hint_y=None, markup=True)
        self.chat_label.bind(width=lambda *x: self.chat_label.setter('text_size')(self.chat_label, (self.chat_label.width, None)))
        self.chat_history.add_widget(self.chat_label)

        self.message_input = TextInput(size_hint=(1, 0.1), multiline=False)
        self.send_button = Button(text="Отправить", size_hint=(1, 0.1))
        self.send_button.bind(on_press=self.send_message)

        self.layout.add_widget(self.chat_history)
        self.layout.add_widget(self.message_input)
        self.layout.add_widget(self.send_button)
        return self.layout

    def send_message(self, instance):
        message = self.message_input.text
        if message:
            # Отправка сообщения на сервер
            requests.post(f"{BASE_URL}/send_message", json={"sender_id": 1, "receiver_id": 2, "message": message})
            self.message_input.text = ""
            self.update_chat()

    def update_chat(self):
        # Получение сообщений с сервера
        response = requests.get(f"{BASE_URL}/get_messages/2")
        messages = response.json().get("messages", [])
        self.chat_label.text = "\n".join([f"[b]User {msg[1]}:[/b] {msg[3]}" for msg in messages])

if __name__ == "__main__":
    MessengerApp().run()
