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

from config import utils

from item import ItemScreen
from list import ListScreen

dbFlag = False

class WindowManager(ScreenManager):
    pass

kv = Builder.load_file('./kv/list.kv')

class MainApp(App):
    # Main Application
    def build(self):
        Window.size = (utils.screenX, utils.screenY)
        
        sm = WindowManager()
        sm.add_widget(ListScreen(name='List'))
        sm.add_widget(ItemScreen(name='Item'))

        # create db and insert data 
        if dbFlag:
            self.insertProduct()

        return sm
    
    # create db and insert data 
    def insertProduct(self):
            
            db_create.create_table_if_not_exists()

            names = ['1-1.png', '1-2.png', '2-1.png', '2-2.png', '1-1.png', '1-2.png', '2-1.png']
            path = 'D:\Workspace\Python\Kivy\Hello-kivy\img'
            for name in names:
                image = path + "/" + name
                data = Product('111', image, 10, 100)
                db.insert_product(data)
    


if __name__ == '__main__':
    MainApp().run()