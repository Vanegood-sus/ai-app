import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image as KivyImage
from kivy.core.window import Window
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from kivy.clock import Clock
import asyncio
from threading import Thread
import aiohttp
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Window.clearcolor = (0.1, 0.1, 0.1, 1)

class AIAssistantApp(App):
    API_URL = "https://text.pollinations.ai/openai"
    API_MODEL = "gpt-4o-mini"
    API_TIMEOUT = 60
    MAX_TOKENS_TEXT = 1000
    MAX_TOKENS_VISION = 1500
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.conversation_history = []
        
    def build(self):
        self.title = 'AI Assistant'
        
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        title_label = Label(
            text='🤖 AI Assistant с Pollinations.ai',
            size_hint=(1, 0.1),
            font_size='20sp',
            bold=True
        )
        main_layout.add_widget(title_label)
        
        self.chat_display = TextInput(
            text='Привет! Я AI помощник. Напиши мне что-нибудь или выбери режим работы.\n\n',
            multiline=True,
            readonly=True,
            size_hint=(1, 0.5),
            background_color=(0.2, 0.2, 0.2, 1),
            foreground_color=(1, 1, 1, 1)
        )
        
        scroll = ScrollView(size_hint=(1, 0.5))
        scroll.add_widget(self.chat_display)
        main_layout.add_widget(scroll)
        
        buttons_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), spacing=5)
        
        ocr_btn = Button(text='📸 OCR', on_press=self.show_ocr_mode)
        analyze_btn = Button(text='🔍 Анализ', on_press=self.show_analyze_mode)
        solve_btn = Button(text='📝 Решить', on_press=self.show_solve_mode)
        
        buttons_layout.add_widget(ocr_btn)
        buttons_layout.add_widget(analyze_btn)
        buttons_layout.add_widget(solve_btn)
        
        main_layout.add_widget(buttons_layout)
        
        input_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.15), spacing=5)
        
        self.user_input = TextInput(
            hint_text='Напишите сообщение...',
            multiline=False,
            size_hint=(0.7, 1),
            background_color=(0.2, 0.2, 0.2, 1),
            foreground_color=(1, 1, 1, 1)
        )
        self.user_input.bind(on_text_validate=self.send_message)
        
        send_btn = Button(
            text='Отправить',
            size_hint=(0.3, 1),
            on_press=self.send_message
        )
        
        input_layout.add_widget(self.user_input)
        input_layout.add_widget(send_btn)
        
        main_layout.add_widget(input_layout)
        
        return main_layout
    
    def append_to_chat(self, message):
        self.chat_display.text += message + '\n\n'
        self.chat_display.cursor = (0, len(self.chat_display.text))
    
    def show_ocr_mode(self, instance):
        self.append_to_chat('📸 Режим OCR активирован. Выберите изображение для распознавания текста.')
        self.show_image_picker('ocr')
    
    def show_analyze_mode(self, instance):
        self.append_to_chat('🔍 Режим анализа активирован. Выберите изображение для анализа.')
        self.show_image_picker('analyze')
    
    def show_solve_mode(self, instance):
        self.append_to_chat('📝 Режим решения задач активирован. Выберите изображение с задачей.')
        self.show_image_picker('solve')
    
    def show_image_picker(self, mode):
        content = BoxLayout(orientation='vertical')
        
        filechooser = FileChooserIconView(
            filters=['*.png', '*.jpg', '*.jpeg'],
            path=os.path.expanduser('~')
        )
        
        def select_image(instance):
            if filechooser.selection:
                image_path = filechooser.selection[0]
                popup.dismiss()
                Thread(target=lambda: asyncio.run(self.process_image(image_path, mode))).start()
        
        select_btn = Button(text='Выбрать', size_hint=(1, 0.1), on_press=select_image)
        
        content.add_widget(filechooser)
        content.add_widget(select_btn)
        
        popup = Popup(title='Выберите изображение', content=content, size_hint=(0.9, 0.9))
        popup.open()
    
    async def process_image(self, image_path, mode):
        Clock.schedule_once(lambda dt: self.append_to_chat(f'⏳ Обрабатываю изображение...'))
        
        try:
            with open(image_path, 'rb') as f:
                image_data = f.read()
            
            import base64
            base64_image = base64.b64encode(image_data).decode('utf-8')
            image_url = f"data:image/jpeg;base64,{base64_image}"
            
            if mode == 'ocr':
                prompt = "Распознай весь текст с этого изображения. Выведи только текст без комментариев."
            elif mode == 'analyze':
                prompt = "Подробно опиши что изображено на этой картинке."
            elif mode == 'solve':
                prompt = "Реши задачу с этого изображения. Покажи подробное решение."
            else:
                prompt = "Что изображено на картинке?"
            
            result = await self.call_pollinations_vision(image_url, prompt)
            
            Clock.schedule_once(lambda dt: self.append_to_chat(f'🤖 Результат:\n{result}'))
            
        except Exception as e:
            logger.error(f"Error processing image: {e}")
            Clock.schedule_once(lambda dt: self.append_to_chat(f'❌ Ошибка: {str(e)}'))
    
    async def call_pollinations_vision(self, image_url, prompt):
        headers = {"Content-Type": "application/json"}
        
        payload = {
            "model": self.API_MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": image_url}}
                    ]
                }
            ],
            "max_tokens": self.MAX_TOKENS_VISION
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.API_URL, headers=headers, json=payload, timeout=self.API_TIMEOUT) as response:
                    if response.status == 200:
                        result = await response.json()
                        if result and 'choices' in result and len(result['choices']) > 0:
                            return result['choices'][0]['message']['content']
                    return "Не удалось получить ответ от API"
        except Exception as e:
            logger.error(f"API error: {e}")
            return f"Ошибка API: {str(e)}"
    
    def send_message(self, instance):
        user_text = self.user_input.text.strip()
        if not user_text:
            return
        
        self.append_to_chat(f'👤 Вы: {user_text}')
        self.user_input.text = ''
        
        Thread(target=lambda: asyncio.run(self.get_ai_response(user_text))).start()
    
    async def get_ai_response(self, user_message):
        Clock.schedule_once(lambda dt: self.append_to_chat('⏳ AI думает...'))
        
        try:
            self.conversation_history.append({"role": "user", "content": user_message})
            
            messages = [
                {"role": "system", "content": "Ты полезный AI ассистент. Отвечай кратко и по делу на русском языке."}
            ] + self.conversation_history[-10:]
            
            headers = {"Content-Type": "application/json"}
            
            payload = {
                "model": self.API_MODEL,
                "messages": messages,
                "max_tokens": self.MAX_TOKENS_TEXT
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(self.API_URL, headers=headers, json=payload, timeout=self.API_TIMEOUT) as response:
                    if response.status == 200:
                        result = await response.json()
                        if result and 'choices' in result and len(result['choices']) > 0:
                            ai_response = result['choices'][0]['message']['content']
                            self.conversation_history.append({"role": "assistant", "content": ai_response})
                            
                            Clock.schedule_once(lambda dt: self.append_to_chat(f'🤖 AI: {ai_response}'))
                        else:
                            Clock.schedule_once(lambda dt: self.append_to_chat('❌ Не удалось получить ответ'))
                    else:
                        Clock.schedule_once(lambda dt: self.append_to_chat(f'❌ Ошибка API: {response.status}'))
                        
        except Exception as e:
            logger.error(f"Error getting AI response: {e}")
            Clock.schedule_once(lambda dt: self.append_to_chat(f'❌ Ошибка: {str(e)}'))

if __name__ == '__main__':
    AIAssistantApp().run()
