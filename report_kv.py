import mysql.connector
import random
from kivymd.app import MDApp
import datetime
from kivy.lang import Builder
from kivymd.uix.menu import MDDropdownMenu

host = "sql12.freesqldatabase.com"
user = "sql12662532"
password = "viDRIhzYSq"
database = "sql12662532"

db = mysql.connector.connect(
    host = "sql12.freesqldatabase.com",
    user = "sql12662532",
    password = "viDRIhzYSq",
    database = "sql12662532",
    )

cursor = db.cursor()

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
        caller.focus = False  # Remove focus from the text field

class ReportApp(MDApp):
    dropdown_handler = DropDownHandler()

    def build(self):
        self.theme_cls.primary_palette = "Green"
        return Builder.load_file('report.kv')

    def show_incident_type_dropdown(self, caller):
        incident_types = ["Medical Emergency", "Natural Disaster", "Security Threat", "Others"]
        self.dropdown_handler.show_custom_dropdown(caller, incident_types)

    def show_urgency_dropdown(self, caller):
        urgency_levels = ["Low", "Medium", "High"]
        self.dropdown_handler.show_custom_dropdown(caller, urgency_levels)

    def submit_data(self):
        # Use the database connection when needed to execute queries
        reportInitial = random.randint(10, 999)
        reportID = str(reportInitial)
        title = self.root.ids.title.text
        incident_type = self.root.ids.choice.text
        image_path = self.root.ids.image_path.text
        details = self.root.ids.details.text
        urgency = self.root.ids.urgency.text
        status = "pending"
        date_created = datetime.datetime.now().strftime("%Y-%m-%d")

        cursor.execute(
            "INSERT INTO report (reportID, title, checklist, image_path, details, urgency, status, dateCreated) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (reportID, title, incident_type, image_path, details, urgency, status, date_created)
        )
        db.commit()

        # Clear the text fields
        self.root.ids.title.text = ""
        self.root.ids.choice.text = ""
        self.root.ids.image_path.text = ""
        self.root.ids.details.text = ""
        self.root.ids.urgency.text = ""

if __name__ == '__main__':
    ReportApp().run()
