from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog

KV = '''
<DialogContent>:
    orientation: "vertical"
    spacing: "12dp"
    size_hint_y: None
    height: "50dp"

    MDFlatButton:
        id: dropdown_button
        text: 'Choose Incident Type'
        on_release: app.show_incident_type_dropdown(root)

Screen:
    MDFlatButton:
        text: 'Open Dialog'
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        on_release: app.open_dialog()
'''

class DialogContent(BoxLayout):
    pass

class DropDownHandler:
    def show_custom_dropdown(self, caller, items):
        menu_items = [{"viewclass": "OneLineListItem",
                       "text": option,
                       "on_release": lambda x=option: self.menu_callback(x, caller)} for option in items]
        self.dropdown_menu = MDDropdownMenu(
            caller=caller,
            items=menu_items,
            position="center",
            width_mult=4,
        )
        self.dropdown_menu.open()

    def menu_callback(self, text_item, caller):
        caller.text = text_item
        self.dropdown_menu.dismiss()

class MyApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

    def show_incident_type_dropdown(self, caller):
        incident_type = ["Medical Emergency", "Natural Disaster", "Security Threat", "Others"]
        dropdown_handler = DropDownHandler()
        dropdown_handler.show_custom_dropdown(caller, incident_type)

    def open_dialog(self):
        self.dialog = MDDialog(
            title="Select Incident Type",
            type="custom",
            content_cls=DialogContent(),
            buttons=[
                MDFlatButton(
                    text="CANCEL", 
                    on_release=self.close_dialog
                )
            ]
        )
        self.dialog.open()

    def close_dialog(self, *args):
        self.dialog.dismiss()

MyApp().run()
