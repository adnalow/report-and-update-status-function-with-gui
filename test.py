from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.button import MDRaisedButton
from kivy.uix.boxlayout import BoxLayout

KV = '''
<Content>
    orientation: "vertical"
    MDRaisedButton:
        id: button
        text: "Open dropdown"
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        on_release: app.open_menu()
'''

class Content(BoxLayout):
    pass

class Example(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"
        return Builder.load_string(KV)

    def open_menu(self):
        menu_items = [{"text": f"Item {i}"} for i in range(5)]
        self.menu = MDDropdownMenu(
            caller=self.root.ids.button,
            items=menu_items,
            position="center",
            width_mult=4,
        )
        self.menu.bind(on_release=self.menu_callback)
        self.menu.open()

    def menu_callback(self, menu, menu_item):
        print(menu_item.text)

Example().run()
