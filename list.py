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


class ListScreen(Screen):
    def __init__(self, **kwargs):
        super(ListScreen, self).__init__(**kwargs)
        Clock.schedule_once(self.retrieve_image_layout)
        Clock.schedule_once(self.retrieve_up_and_down_image)
        Clock.schedule_once(self.retrieve_category_layout)
        # self.imageList = []
        self.imageLayoutHeight = 0
        self.scroll_position = 0
        self.scroll_move_dis = utils.itemLength
        self.scroll_y_dis = 0

    # prevent to delay, so we can get image_layou and draw dynamically
    def retrieve_image_layout(self, dt):
        image_layout = self.ids.image_layout  # Access the image_layout widget
    
        # get all products.
        products = self.get_products()

        # draw Items
        if products:
            # get scroll_y step 
            self.scroll_y_dis = 1 / (math.ceil(len(products) / 2)  + 1)

            for product in products:
                image = self.on_draw_item(product)
                self.imageLayoutHeight += image.height
                container = BoxLayout()
                lp = (utils.screenX / 2 - utils.itemLength - 10) / 2
                container.padding = [lp ,10,lp,10]
                container.size_hint_y = None
                container.height = image.height  + 10
                container.add_widget(image)
                # self.imageList.append(image)
                image_layout.add_widget(container)
                
        else:
            image_layout.add_widget(Label(text='Image not found'))

        image_layout.height = self.imageLayoutHeight + 10
    
    def get_products(self):
        products = db.get_products()
        return products
    
    # click image, then navigate to itemscreen with item id
    # def on_image_click(self, instance, touch):
    #     for image in self.imageList:
    #         if image.collide_point(*touch.pos):
    #             # self.manager.current = 'Item'
    #             self.manager.get_screen("Item").set_item_id(image.name)

    
    # draw one image
    def on_draw_item(self, product):
        image = ImageItem()
        image_stream = io.BytesIO(product[2])
        img = CoreImage(image_stream, ext='png')
        image.texture = img.texture
        image.name = product[0]
        image.manager = self.manager      

        return image
    
    ###################################################################
    def retrieve_up_and_down_image(self, dt):
        up_image = self.ids.up_image
        up_image.bind(on_touch_down = self.on_up_img_click)
        down_image = self.ids.down_image
        down_image.bind(on_touch_down = self.on_down_img_click)

    def on_up_img_click(self, instance, touch):
        if instance.collide_point(*touch.pos):
            # image_scroll_view.scroll_y = 1
            if(self.scroll_position > 0):
                self.ids.image_scroll_view.scroll_y += self.scroll_y_dis
                self.scroll_position -= self.scroll_move_dis
            # image_scroll_view = self.ids.image_scroll_view
            # image_scroll_view.scroll_to(self.ids.image_layout)

    def on_down_img_click(self, instance, touch):
        if instance.collide_point(*touch.pos):
            # image_scroll_view.scroll_y = 1
            if(self.ids.image_scroll_view.scroll_y > 0.01):
                self.ids.image_scroll_view.scroll_y -= self.scroll_y_dis
                self.scroll_position += self.scroll_move_dis

    ########################################################################

    def retrieve_category_layout(self, dt):
        categoryLayout = self.ids.category_layout  # Access the image_layout widget

        for i in range(8):
            image = self.on_draw_category_item()
            categoryLayout.add_widget(image)
            categoryLayout.width += image.width

    def on_draw_category_item(self):
        boxlayout = BoxLayout(orientation='vertical')
        image = CategoryItem(source='./img/category.png')
        specLabel = Label(text='bis zu 600')
        specLabel.color = '#000000'
        specLabel.font_size = 15
        nameLabel = Label(text='Zuge')
        nameLabel.color = '#000000'
        nameLabel.font_size = 15
        nameLabel.background_color = '#111111'
        boxlayout.add_widget(image)
        boxlayout.add_widget(specLabel)
        boxlayout.add_widget(nameLabel)
        boxlayout.height = 100

        return boxlayout


class ImageItem(Image):
    def __init__(self, **kwargs):
        super(ImageItem, self).__init__(**kwargs)
        self.manager = None
        self.size = (utils.itemLength, utils.itemLength)
        self.size_hint = (None, None)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.manager.current = 'Item'
            self.manager.get_screen("Item").set_item_id(self.name)

class CategoryItem(Image):
    def __init__(self, **kwargs):
        super(CategoryItem, self).__init__(**kwargs)

