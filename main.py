from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.properties import StringProperty

from DbFuncs import db
from DbFuncs import db_create
from model.Product import Product

dbFlag = False

class ListScreen(Screen):
    def __init__(self, **kwargs):
        super(ListScreen, self).__init__(**kwargs)
        Clock.schedule_once(self.retrieve_image_layout)

    # prevent to delay, so we can get image_layou and draw dynamically
    def retrieve_image_layout(self, dt):
        image_layout = self.ids.image_layout  # Access the image_layout widget
    
        # get all products.
        products = self.get_products()
        if products:
            for product in products:
                image = self.on_draw_item(product)
                image_layout.add_widget(image)
        else:
            image_layout.add_widget(Label(text='Image not found'))


    def click_item(self):
        app = App.get_running_app()
        app.root.current = 'Item'
    
    def get_products(self):
        products = db.get_products()
        return products
    
    # click image, then navigate to itemscreen with item id
    def on_image_click(self, instance, touch):
        if instance.collide_point(*touch.pos):
            print("Image Clicked!")  # You can perform any action you want here
            # self.manager.current = 'Item'
            self.manager.get_screen("Item").set_item_id(1)
    
    # draw one image
    def on_draw_item(self, product):
        image = Image()
        image.size = (100, 100)
        # image.allow_stretch = True
        # image.keep_ratio = False
        # image.source = 'D:\Workspace\Python\Kivy\Hello-kivy\img/1-1.png'
        texture = Texture.create(size=(image.width, image.height))
        texture.blit_buffer(product[2], colorfmt='rgba', bufferfmt='ubyte')
        image.texture = texture
        image.color = [1,0,0,1]
        image.bind(on_touch_down=self.on_image_click)

        return image



class ItemScreen(Screen):
    def __init__(self, **kwargs):
        super(ItemScreen, self).__init__(**kwargs)
        self.itemId = None

    def set_item_id(self, id):
        self.itemId = id
        self.draw_page(self.itemId)

    def draw_page(self, id):
        product = db.get_product(id)
        print(product)


class WindowManager(ScreenManager):
    pass

kv = Builder.load_file('./kv/list.kv')

class MainApp(App):
    # Main Application
    def build(self):
        Window.size = (600, 850)
        
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
                db.insertProduct(data)
    


if __name__ == '__main__':
    MainApp().run()