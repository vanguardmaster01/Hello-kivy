from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.button import ButtonBehavior
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty

from DbFuncs import db
from DbFuncs import db_create
from model.Product import Product

dbFlag = False

class ListScreen(Screen):
    def select_item(self):
        app = App.get_running_app()
        app.root.current = 'Item'

class ItemScreen(Screen):
    pass

class WindowManager(ScreenManager):
    pass

kv = Builder.load_file('./kv/list.kv')

class MainApp(App):
    # Main Application
    def build(self):
        Window.size = (600, 850)
        
        sm = ScreenManager()
        sm.add_widget(ListScreen(name='List'))
        sm.add_widget(ItemScreen(name='Item'))


        # create db and insert data 
        if dbFlag:
            self.insertProduct()

        # get all products.
        products = self.getProducts()

        # display products on the selling-screen


        return sm
    
    # create db and insert data 
    def insertProduct(self):
            
            db_create.createDb()

            names = ['1-1.png', '1-2.png', '2-1.png', '2-2.png', '1-1.png', '1-2.png', '2-1.png']
            path = 'D:\Workspace\Python\Kivy\Hello-kivy\img'
            for name in names:
                image = path + "/" + name
                data = Product('111', image, 10, 100)
                db.insertProduct(data)
    
    def getProducts(self):
        products = db.getProducts()
        return products

if __name__ == '__main__':
    MainApp().run()