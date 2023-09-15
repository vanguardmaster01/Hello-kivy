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

from config import utils

from item import ItemScreen
from list import ListScreen
from ad import AdScreen
import os
import api

dbFlag = False

class WindowManager(ScreenManager):
     pass
    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
    #     with self.canvas.before:
    #         Color(1, 1, 1, 1) # a white color
    #         self.rect = Rectangle(pos=self.pos, size=self.size)
    #         self.bind(pos=self.update_rect, size=self.update_rect)

    # def update_rect(self, *args):
    #     self.rect.pos = self.pos
    #     self.rect.size = self.size

kv = Builder.load_file('./kv/list.kv')

class MainApp(App):
    # Main Application
    def build(self):
        db_create.create_tables()
        self.connect_to_server()

        Window.size = (utils.screenX, utils.screenY)
        sm = WindowManager()
        sm.add_widget(AdScreen(name='Ad'))
        sm.add_widget(ListScreen(name='List'))
        sm.add_widget(ItemScreen(name='Item'))

        return sm
    
    # create db and insert data 
    def connect_to_server(self):
        api.send_get_ads_info()
        api.send_get_machine_info()
        api.send_get_products_info()


if __name__ == '__main__':
    MainApp().run()