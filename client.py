import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.uix.filechooser import FileChooserListView
import base64

# Базовый URL сервера
BASE_URL = "https://three22ram.onrender.com"

class MessengerApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')
        self.chat_history = ScrollView(size_hint=(1, 0.7))
        self.chat_layout = GridLayout(cols=1, size_hint_y=None, spacing=10, padding=10)
        self.chat_layout.bind(minimum_height=self.chat_layout.setter('height'))
        self.chat_history.add_widget(self.chat_layout)
        self.layout.add_widget(self.chat_history)

        self.message_input = TextInput(size_hint=(1, 0.1), multiline=False)
        self.send_button = Button(text="Отправить", size_hint=(1, 0.1))
        self.send_button.bind(on_press=self.send_message)
        self.layout.add_widget(self.message_input)
        self.layout.add_widget(self.send_button)

        # Кнопка для загрузки аватарки
        self.avatar_button = Button(text="Загрузить аватарку", size_hint=(1, 0.1))
        self.avatar_button.bind(on_press=self.open_file_chooser)
        self.layout.add_widget(self.avatar_button)

        # Обновление чата каждые 2 секунды
        Clock.schedule_interval(self.update_chat, 2)
        return self.layout

    def send_message(self, instance):
        message = self.message_input.text
        if message:
            # Отправка сообщения на сервер
            requests.post(f"{BASE_URL}/send_message", json={"sender_id": 1, "receiver_id": 2, "message": message})
            self.message_input.text = ""
            self.update_chat()

    def update_chat(self, *args):
        # Получение сообщений с сервера
        response = requests.get(f"{BASE_URL}/get_messages/2")
        messages = response.json().get("messages", [])
        self.chat_layout.clear_widgets()
        for msg in messages:
            self.chat_layout.add_widget(Label(text=f"User {msg['sender_id']}: {msg['message']}", size_hint_y=None, height=40))

    def open_file_chooser(self, instance):
        # Открытие файлового менеджера для выбора аватарки
        self.file_chooser = FileChooserListView()
        self.file_chooser.bind(on_submit=self.upload_avatar)
        self.layout.add_widget(self.file_chooser)

    def upload_avatar(self, instance, file_path, *args):
        # Загрузка аватарки на сервер
        with open(file_path[0], "rb") as file:
            files = {"file": file}
            response = requests.post(f"{BASE_URL}/upload_avatar/1", files=files)
            if response.status_code == 200:
                print("Аватарка успешно загружена!")
        self.layout.remove_widget(self.file_chooser)

if __name__ == "__main__":
    MessengerApp().run()
