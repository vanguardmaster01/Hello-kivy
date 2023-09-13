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

dbFlag = False

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
        Window.size = (utils.screenX, utils.screenY)
                      
        sm = WindowManager()
        sm.add_widget(AdScreen(name='Ad'))
        sm.add_widget(ListScreen(name='List'))
        sm.add_widget(ItemScreen(name='Item'))

        # create db and insert data 
        if dbFlag:
            self.insertProduct()

        return sm
    
    # create db and insert data 
    def insertProduct(self):
            
            # db.delete_ads()
            db_create.create_tables()


            names = ['1-1.png', '1-2.png', '2-1.png', '2-2.png', '1-1.png', '1-2.png', '2-1.png']
            path = './img'
            for name in names:
                image = path + "/" + name
                data = Product(1, '1234', 'Prodcut1', image, '20mg', '300mAh', 'XXX', 10, 'EUR', 'This is .....')
                # db.insert_product(data)

            ad = Ad(1, 'PPT', './pptx.pptx')
            # ad = Ad(1, 'MP4', './test.mp4')
            db.insert_ads(ad)


if __name__ == '__main__':
    MainApp().run()