import mysql.connector
import random
from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.button import MDRectangleFlatButton
from kivy.lang import Builder
from helpers import title_helper


host = "112.198.173.169"
user = "root"
password = "incidentreportingapp"
database = "reportingApp"

db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "incidentreportingapp",
    database = "reportingApp"
    )

cursor = db.cursor()

class reportApp(MDApp):
    def build(self):
        screen = Screen()
        self.theme_cls.primary_palette = "Green"
        button = MDRectangleFlatButton(text='Submit', pos_hint={'center_x': 0.5, 'center_y': 0.4},
                                       on_release=self.submit_data)
        # Removed the attempt to assign a KivyMD widget to title
        screen.add_widget(Builder.load_string(title_helper))
        screen.add_widget(button)
        return screen

    def userReport(self, obj):
        def report1():
            return "Robbery"

        def report2():
            return "Fire"

        def report3():
            return "Accident"

        pre_defined_reports = {
            1: report1,
            2: report2,
            3: report3,
        }

    def submit_data(self, obj):
        # Assuming there is an input field with the name 'username'
        # print(self.username.text)
        pass

reportApp().run()