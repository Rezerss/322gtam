from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.clock import Clock
from kivy.uix.modalview import ModalView

# Настройка цветов
WINDOW_BG = (0.1, 0.1, 0.1, 1)  # Тёмно-серый фон
CHAT_BG = (0.2, 0.2, 0.2, 1)     # Серый фон чатов
TEXT_COLOR = (1, 1, 1, 1)         # Белый текст
BUTTON_COLOR = (0.3, 0.3, 0.3, 1) # Серый цвет кнопок

# Класс для кнопки с иконкой
class IconButton(ButtonBehavior, Image):
    pass

# Основной интерфейс
class TelegramUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.spacing = 10
        self.padding = 10

        # Боковая панель с чатами
        self.chat_list = BoxLayout(orientation='vertical', size_hint=(0.3, 1))
        self.chat_list.add_widget(Label(text="Чаты", size_hint=(1, 0.1), color=TEXT_COLOR))
        self.chat_scroll = ScrollView(size_hint=(1, 0.9))
        self.chat_layout = GridLayout(cols=1, size_hint_y=None, spacing=10, padding=10)
        self.chat_layout.bind(minimum_height=self.chat_layout.setter('height'))
        self.chat_scroll.add_widget(self.chat_layout)
        self.chat_list.add_widget(self.chat_scroll)
        self.add_widget(self.chat_list)

        # Основное окно чата
        self.chat_window = BoxLayout(orientation='vertical', size_hint=(0.7, 1))
        self.chat_history = ScrollView(size_hint=(1, 0.8))
        self.chat_messages = GridLayout(cols=1, size_hint_y=None, spacing=10, padding=10)
        self.chat_messages.bind(minimum_height=self.chat_messages.setter('height'))
        self.chat_history.add_widget(self.chat_messages)
        self.chat_window.add_widget(self.chat_history)

        # Поле ввода и кнопка отправки
        self.input_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), spacing=10)
        self.message_input = TextInput(hint_text="Введите сообщение...", multiline=False, background_color=CHAT_BG, foreground_color=TEXT_COLOR)
        self.send_button = Button(text="Отправить", background_color=BUTTON_COLOR, color=TEXT_COLOR)
        self.send_button.bind(on_press=self.send_message)
        self.input_layout.add_widget(self.message_input)
        self.input_layout.add_widget(self.send_button)
        self.chat_window.add_widget(self.input_layout)
        self.add_widget(self.chat_window)

        # Добавляем тестовые чаты
        self.add_chat("Чат 1")
        self.add_chat("Чат 2")
        self.add_chat("Чат 3")

    def add_chat(self, chat_name):
        chat_button = Button(text=chat_name, size_hint_y=None, height=50, background_color=CHAT_BG, color=TEXT_COLOR)
        chat_button.bind(on_press=self.open_chat)
        self.chat_layout.add_widget(chat_button)

    def open_chat(self, instance):
        self.chat_messages.clear_widgets()
        self.chat_messages.add_widget(Label(text=f"Открыт чат: {instance.text}", color=TEXT_COLOR))

    def send_message(self, instance):
        message = self.message_input.text
        if message:
            self.chat_messages.add_widget(Label(text=f"Вы: {message}", color=TEXT_COLOR, halign='left', size_hint_y=None, height=40))
            self.message_input.text = ""
            self.chat_history.scroll_to(self.chat_messages.children[0])

# Приложение
class TelegramApp(App):
    def build(self):
        Window.clearcolor = WINDOW_BG
        return TelegramUI()

if __name__ == "__main__":
    TelegramApp().run()
