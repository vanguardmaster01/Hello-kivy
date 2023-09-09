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
# from kivy.graphics.texture import Texture
from kivy.properties import StringProperty
from PIL import Image as PILImage
import io
import math

from DbFuncs import db
from DbFuncs import db_create
from model.Product import Product

from config import utils

dbFlag = False

class ListScreen(Screen):
    def __init__(self, **kwargs):
        super(ListScreen, self).__init__(**kwargs)
        Clock.schedule_once(self.retrieve_image_layout)
        Clock.schedule_once(self.retrieve_up_and_down_image)
        self.imageList = []
        self.height = 0
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
                self.height += image.height
                container = BoxLayout()
                lp = (utils.screenX / 2 - utils.itemLength - 10) / 2
                container.padding = [lp ,10,lp,10]
                container.size_hint_y = None
                container.height = image.height  + 10
                container.add_widget(image)
                self.imageList.append(image)
                image_layout.add_widget(container)
                
        else:
            image_layout.add_widget(Label(text='Image not found'))

        image_layout.height = self.height + 200
    
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
        image = ItemImage()
        image_stream = io.BytesIO(product[2])
        img = CoreImage(image_stream, ext='png')
        image.texture = img.texture
        image.name = product[0]
        image.manager = self.manager      

        # image.bind(on_touch_down=self.on_image_click)

        return image
    
    ###################################################################
    def retrieve_up_and_down_image(self, dt):
        up_image = self.ids.up_image
        up_image.bind(on_touch_down = self.on_up_img_click)
        down_image = self.ids.down_image
        down_image.bind(on_touch_down = self.on_down_img_click)

    def on_up_img_click(self, instance, touch):
        if instance.collide_point(*touch.pos):
            # scroll_view.scroll_y = 1
            if(self.scroll_position > 0):
                self.ids.scroll_view.scroll_y += self.scroll_y_dis
                self.scroll_position -= self.scroll_move_dis
            # scroll_view = self.ids.scroll_view
            # scroll_view.scroll_to(self.ids.image_layout)

    def on_down_img_click(self, instance, touch):
        if instance.collide_point(*touch.pos):
            # scroll_view.scroll_y = 1
            if(self.ids.scroll_view.scroll_y > 0.01):
                self.ids.scroll_view.scroll_y -= self.scroll_y_dis
                self.scroll_position += self.scroll_move_dis



class ItemImage(Image):
    def __init__(self, **kwargs):
        super(ItemImage, self).__init__(**kwargs)
        self.manager = None
        self.size = (utils.itemLength, utils.itemLength)
        self.size_hint = (None, None)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            # self.manager.current = 'Item'
            self.manager.get_screen("Item").set_item_id(self.name)
            print(f'self.name{self.name}')



class ItemScreen(Screen):
    def __init__(self, **kwargs):
        super(ItemScreen, self).__init__(**kwargs)
        self.itemId = None

    def set_item_id(self, id):
        self.itemId = id
        self.draw_page(self.itemId)

    def draw_page(self, id):
        product = db.get_product(id)
        # print(product)


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