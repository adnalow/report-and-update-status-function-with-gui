from kivy.lang import Builder
from kivymd.app import MDApp

KV = '''
BoxLayout:
    orientation: 'vertical'
    spacing: 10
    size_hint_y: None
    height: text_field.height + dp(10)

    MDTextField:
        id: text_field
        hint_text: 'Enter text'
        size_hint_x: None
        width: '200dp'

    MDRaisedButton:
        text: 'Button'
        size_hint: None, None
        size: 3 * dp(48), dp(48)
        pos_hint: {'center_x': 0.5}
'''

class MainApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

MainApp().run()
