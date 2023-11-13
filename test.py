from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.button import MDFlatButton

KV = '''
Screen:
    MDFlatButton:
        id: button
        text: 'Open Menu'
        on_release: app.show_incident_type_dropdown(button)
'''

class DropDownHandler:
    def show_custom_dropdown(self, caller, items):
        menu_items = [{"viewclass": "OneLineListItem",
                       "text": option,
                       "on_release": lambda x=option: self.menu_callback(x, caller)} for option in items]
        self.dropdown_menu = MDDropdownMenu(
            caller=caller,
            items=menu_items,
            position="bottom",
            width_mult=4,
        )
        self.dropdown_menu.open()

    def menu_callback(self, text_item, caller):
        caller.text = text_item
        self.dropdown_menu.dismiss()
        caller.focus = False

class MyApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

    def show_incident_type_dropdown(self, caller):
        incident_type = ["Medical Emergency", "Natural Disaster", "Security Threat", "Others"]
        dropdown_handler = DropDownHandler()
        dropdown_handler.show_custom_dropdown(caller, incident_type)

MyApp().run()
