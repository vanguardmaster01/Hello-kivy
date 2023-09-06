from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.button import ButtonBehavior
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty

class ListScreen(Screen):
    def select_item(self):
        app = App.get_running_app()
        app.root.current = 'Item'

class ItemScreen(Screen):
    pass

class WindowManager(ScreenManager):
    pass

kv = Builder.load_file('list.kv')

class MainApp(App):
    # Main Application
    def build(self):
        Window.size = (600, 850)
        sm = ScreenManager()
        sm.add_widget(ListScreen(name='List'))
        sm.add_widget(ItemScreen(name='Item'))
        return sm

if __name__ == '__main__':
    MainApp().run()