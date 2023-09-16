from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.core.image import Image as CoreImage
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
# from kivy.graphics.texture import Texture
from kivy.properties import StringProperty
from PIL import Image as PILImage
import io
import math

from DbFuncs import db
from DbFuncs import db_create
from model.Product import Product
from model.Ad import Ad

from item import ItemScreen
from list import ListScreen
from ad import AdScreen
import os
from dotenv import load_dotenv
load_dotenv()
import api
import asyncio
from kivy.clock import Clock
import threading
import time
from config.utils import initLock

mutex = 0
# connectThread = threading.Thread(target=api.connect_to_server())

def between_callback():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(api.connect_to_server())
    loop.close()


class WindowManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(1, 1, 1, 1) # a white color
            self.rect = Rectangle(pos=self.pos, size=self.size)
            self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

kv = Builder.load_file('./kv/list.kv')


class MainApp(App):
    # Main Application
    def build(self):
        
        print("main thread id", threading.get_native_id())
        initLock(threading.Lock())

        #connect db
        db.openDatabase()

        _thread = threading.Thread(target=between_callback)
        _thread.start()


        width = int(os.environ.get('screenX'))
        height = int(os.environ.get('screenY'))

        db_create.create_tables()

        print('windownamager')
        Window.size = (width, height)

        # asyncio.get_event_loop().run_until_complete(api.connect_to_server())
        
        sm = WindowManager()
        sm.add_widget(AdScreen(name='Ad'))
        sm.add_widget(ListScreen(name='List'))
        sm.add_widget(ItemScreen(name='Item'))

        # Clock.schedule_interval(self.periodic_task, 10)
        
        return sm
    
    # def connect_to_server(self, dt):
    #     api.connect_to_server()

    async def connect_to_server(self):
        await api.connect_to_server()
        print('Connected to server')

    def periodic_task(self, dt):
        asyncio.create_task(self.connect_to_server())


if __name__ == '__main__':
    MainApp().run()
    db.closeDatabase()