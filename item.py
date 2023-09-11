from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.button import ButtonBehavior, Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.core.image import Image as CoreImage
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, Triangle
import io
import math

from DbFuncs import db
from DbFuncs import db_create
from model.Product import Product

from config import utils

from kivy.graphics import RoundedRectangle, Color, Line

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

        self.ids.back_img.bind(on_touch_down = self.on_back_press)
        
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

        priceStr = str(product[4]) + ' EUR'
        priceLabel = Label(
            text= priceStr,
            size_hint=(None, None),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},  # Center the label on the image
            color=(0, 0, 0, 1),  # Set the text color (white in this example)
            font_size = 30
        )
        self.ids.price_layout.add_widget(priceLabel)

    # display infos
    def draw_label(self, value):
        boxLayout = BoxLayout()
        boxLayout.size_hint_x = None
        boxLayout.padding = [10, 2, 2, 2]

        firstLabel = Label(text=value)
        firstLabel.color = '#000000'
        firstLabel.halign = 'left'
        firstLabel.size_hint_x = None
        firstLabel.text_size = (firstLabel.width, None)
        boxLayout.add_widget(firstLabel)
        self.ids.info_layout.add_widget(boxLayout)

    # display bigo (labels, img on the top-right )
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

    def on_back_press(self, instance, touch):
        if instance.collide_point(*touch.pos):
            print('back_pressed')

    def on_buy_press(self):
        print(f'buy_pressed')



class CountNumber(GridLayout):
    def __init__(self, **kwargs):
        super(CountNumber, self).__init__(**kwargs)
        self.number = 0
        self.cols = 2
        self.padding = [0,0,25,0]
        self.number_text = None
        self.draw_widget()

    def draw_widget(self):
        self.number_text = Label(
            text=str(self.number),
            color='#000000',
            font_size = 30
        )
        self.number_text.size_hint_x = 0.6
        self.add_widget(self.number_text)

        controlLayout = BoxLayout(orientation='vertical')
        controlLayout.size_hint_x = None
        controlLayout.width = 30

        incImg = Image(source='./img/up-shape.png')
        incImg.allow_stretch = True
        incImg.bind(on_touch_down = self.increase_number)
        controlLayout.add_widget(incImg)
        decImg = Image(source='./img/down-shape.png')
        decImg.allow_stretch = True
        decImg.bind(on_touch_down = self.decrease_number)
        controlLayout.add_widget(decImg)

        self.add_widget(controlLayout)

    def increase_number(self, instance, touch):
        if instance.collide_point(*touch.pos):
            self.number += 1
            self.update_number()
    def decrease_number(self, instance, touch):
        if instance.collide_point(*touch.pos):
            if self.number > 0:
                self.number -= 1
                self.update_number()

    def update_number(self):
        self.number_text.text = str(self.number)