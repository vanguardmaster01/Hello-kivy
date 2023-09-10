from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.button import ButtonBehavior, Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.core.image import Image as CoreImage
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
import io
import math

from DbFuncs import db
from DbFuncs import db_create
from model.Product import Product

from config import utils

class ItemScreen(Screen):
    def __init__(self, **kwargs):
        super(ItemScreen, self).__init__(**kwargs)
        self.itemId = None

    def set_item_id(self, id):
        self.itemId = id
        self.draw_page(self.itemId)

    def draw_page(self, id):
        product = db.get_product(id)

        # display name
        self.draw_title(product[1])

        # display product (image, price, ...)
        self.draw_product_info(product)

        self.draw_bigo()
        
    def draw_title(self, name):
        titleLayout = self.ids.title_layout    
        titleLabel = Label(text=name)
        titleLabel.color = '#c00000'
        titleLabel.font_size = 30   
        titleLabel.size_hint_x = None
        titleLabel.padding = [200, 5, 5, 5]
        titleLayout.add_widget(titleLabel)

    def draw_product_info(self, product):
        image = Image()
        image_stream = io.BytesIO(product[2])
        img = CoreImage(image_stream, ext='png')
        image.texture = img.texture
        self.ids.image_layout.add_widget(image)

        self.draw_label('Abc1234')
        self.draw_label('600')
        self.draw_label('20mg')
        self.draw_label('40asda0mAh')
        self.draw_label('2ml')

    def draw_label(self, value):
        boxLayout = BoxLayout()
        boxLayout.size_hint_x = None
        boxLayout.padding = [10, 2, 2, 2]

        firstLabel = Label(text=value)
        firstLabel.color = '#000000'
        boxLayout.add_widget(firstLabel)
        self.ids.info_layout.add_widget(boxLayout)

    def draw_bigo(self):
        bigoLayout = self.ids.bigo_layout
        # Create an Image widget
        img = Image(source='./img/bigo.png')  # Replace 'your_image.png' with your image file path
        
        # Calculate the position for the image (top-right corner)
        image_x = utils.screenX - img.width - 50
        image_y = utils.screenY / 4  - img.height / 2

        # Draw the image on the canvas
        with bigoLayout.canvas:
            Rectangle(pos=(image_x, image_y), size=img.size, texture=img.texture)
