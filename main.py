from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.image import Image as CoreImage
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle

from DbFuncs import db
from DbFuncs import db_create

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
from config.utils import stopWebsocket
from kivy.config import Config

_thread = None
stop_thread = False
loop = None
delta = 0


def between_callback():
    global stop_thread
    global loop
    # while not stop_thread:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.create_task(api.connect_to_server())
    loop.run_forever()
    # loop.close()


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

sm = WindowManager()

adScreen = AdScreen(name='Ad')        
listScreen = ListScreen(name='List')        
itemScreen = ItemScreen(name='Item') 

class MainApp(App):

    # Main Application
    def build(self):
        global _thread

        print("main thread id", threading.get_native_id())
        initLock(threading.Lock())

        #connect db
        db.openDatabase()

        # _thread = threading.Thread(target=between_callback)
        # _thread.start()

        width = int(os.environ.get('screenX'))
        height = int(os.environ.get('screenY'))

        db_create.create_tables()

        Config.set('graphics', 'width', width)
        Config.set('graphics', 'height', height)
        Config.set('graphics', 'custom_titlebar', '1')
        Config.write()

        # Window.size = (width, height)
        
        # asyncio.get_event_loop().run_until_complete(api.connect_to_server())
       
        sm.add_widget(adScreen)
        sm.add_widget(listScreen)
        sm.add_widget(itemScreen)

        Clock.schedule_interval(self.count_time, 1)
        
        adScreen.bind(on_touch_down=self.touch_screen)
        listScreen.bind(on_touch_down=self.touch_screen)
        itemScreen.bind(on_touch_down=self.touch_screen)
        
        return sm

    def touch_screen(self, instance, touch):
        global delta
        delta = 0

    def on_stop(self):
        print('here')
        global _thread
        global stop_thread
        global loop

        stopWebsocket = True
        # stop_thread = True
        
        _thread.join(1)

        # process = multiprocessing.current_process()
        # process.kill()

        loop.stop()

        print('222')

    def count_time(self, dt):
        global delta
        delta += 1
        print(f'delta:{delta}')
        if delta > 10:
            sm.current = 'Ad'
            listScreen.clear_widgets()
            listScreen.__init__()
            itemScreen.clear_widgets()
            itemScreen.__init__()
            delta = 0

if __name__ == '__main__':
    MainApp().run()
    db.closeDatabase()