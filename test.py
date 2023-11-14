from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.menu import MDDropdownMenu
from kivy.properties import ObjectProperty

KV = '''
BoxLayout:
    orientation: 'vertical'
    MDRaisedButton:
        id: button
        text: "Report Incident"
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        on_release: app.menu_callback()
'''

class MainApp(MDApp):
    dropdown = ObjectProperty()

    def build(self):
        self.theme_cls.primary_palette = "Blue"
        return Builder.load_string(KV)
    
    def on_start(self):
        # Menu items list
        menu_items = [
            {"viewclass": "OneLineListItem", "text": "Medical Emergency"},
            {"viewclass": "OneLineListItem", "text": "Natural Disaster"},
            {"viewclass": "OneLineListItem", "text": "Security Threat"},
            {"viewclass": "OneLineListItem", "text": "Others"}
        ]
        
        # Create the dropdown menu
        self.dropdown = MDDropdownMenu(
            caller=self.root.ids.button,
            items=menu_items,
            width_mult=4,
            position="center"
        )
        
        # Set the release callback for each menu item
        for item in menu_items:
            item['on_release'] = lambda x=item['text']: self.option_callback(x)

    def menu_callback(self):
        # Open the dropdown menu
        self.dropdown.open()

    def option_callback(self, option_text):
        # Print the text of the selected option
        print(option_text)
        # Close the dropdown to avoid double opening on multiple clicks
        self.dropdown.dismiss()

MainApp().run()
