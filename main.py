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
from config.utils import initThreadLock, setThreadStatus, getThreadStatus, THREAD_INIT, THREAD_RUNNING, THREAD_STOPPING, THREAD_FINISHED
from config.utils import initDBLock
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar
from kivy.uix.popup import Popup
from contextlib import suppress


_thread = None
stop_thread = False
loop = None
delta = 0

def between_callback():
    # global stop_thread
    global loop
    # while not stop_thread:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(api.connect_to_server())


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
        initDBLock()
        initThreadLock()

        #connect db
        db.openDatabase()

        _thread = threading.Thread(target=between_callback)
        _thread.start()

        width = int(os.environ.get('screenX'))
        height = int(os.environ.get('screenY'))
        Window.size = (width, height)

        db_create.create_tables()
       
        sm.add_widget(adScreen)
        sm.add_widget(listScreen)
        sm.add_widget(itemScreen)

        Clock.schedule_interval(self.count_time, 1)
        
        adScreen.bind(on_touch_down=self.touch_screen)
        listScreen.bind(on_touch_down=self.touch_screen)
        itemScreen.bind(on_touch_down=self.touch_screen)
        
        Window.bind(on_request_close=self.on_request_close)
        Window.bind(on_resize=self.on_resize)

        return sm

    # if user action, .....
    def touch_screen(self, instance, touch):
        global delta
        delta = 0  

    def wait_apithread_stop(self, td):  
        global _thread
        global loop
        try:
            _thread.join(0.1)
            if getThreadStatus() == THREAD_FINISHED:
                _thread.join()
                self.stopEvent.cancel() 
                self.stop()
        except RuntimeError:
            pass        
  
    # if nothing action for 1 min, display ad
    def count_time(self, dt):
        global delta
        delta += 1
        print(f'delta:{delta}')
        if delta > 10:
            listScreen.kill_all_timeser()
            listScreen.clear_widgets()
            listScreen.__init__()

            itemScreen.kill_all_timers()
            itemScreen.clear_widgets()
            itemScreen.__init__()
            delta = 0
            sm.current = 'Ad'

    def on_request_close(self, *args):
        print('request_close')
        self.textpopup(title='Exit', text='Are you sure?')
        return True
    
    def wait_threadstop(self, *args):
        if getThreadStatus() != THREAD_FINISHED:
            setThreadStatus(THREAD_STOPPING)
            self.stopEvent = Clock.schedule_interval(self.wait_apithread_stop, 0.2)
        else : 
            self.stop()

    def textpopup(self, title='', text=''):
        box = BoxLayout(orientation='vertical')
        box.add_widget(Label(text=text))
        mybutton = Button(text='OK', size_hint=(1, 0.5))
        # box.add_widget(progress_bar)
        box.add_widget(mybutton)
        popup = Popup(title=title, content=box, size_hint=(None, None), size=(300, 150), auto_dismiss = False)
        mybutton.bind(on_release=self.wait_threadstop)
        popup.open()

    def on_resize(self, window, width, heigt):
        print('main_resize')
        listScreen.on_resize()
        itemScreen.on_resize()


if __name__ == '__main__':
    MainApp().run()
    db.closeDatabase()