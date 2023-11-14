from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.list import MDList, TwoLineListItem
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.uix.scrollview import ScrollView
from kivymd.uix.menu import MDDropdownMenu
import mysql.connector

KV = '''
Screen:
    MDFlatButton:
        id: button
        text: 'Open Menu'
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        on_release: app.show_incident_type_dropdown(button)
'''

# Database configuration
host = "112.198.173.169"
user = "root"
password = "incidentreportingapp"
database = "reportingApp"

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="incidentreportingapp",
    database="reportingApp"
)
cursor = db.cursor()

class DropDownHandler(BoxLayout):
    selected_item = StringProperty('')  # Property to store the selected item

    def __init__(self, caller, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.caller = caller
        self.create_dropdown_menu()

    def create_dropdown_menu(self):
        menu_items = [{"viewclass": "OneLineListItem",
                       "text": option,
                       "on_release": lambda x=option: self.menu_callback(x)} 
                      for option in ["Preparing to deploy", "On the Process", "Resolved"]]
        self.dropdown_menu = MDDropdownMenu(
            caller=self.caller,
            items=menu_items,
            position="center",
            width_mult=4
        )
        self.dropdown_menu.open()

    def menu_callback(self, text_item):
        self.selected_item = text_item
        self.dropdown_menu.dismiss()

class MyApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Green"
        self.screen = Screen()
        Builder.load_string(KV)

        scroll = ScrollView()
        self.list_view = MDList()
        scroll.add_widget(self.list_view)
        self.screen.add_widget(scroll)
        self.populate_list()

        return self.screen

    def populate_list(self):
        cursor.execute("SELECT ReportId, Title FROM report")
        rows = cursor.fetchall()

        for row in rows:
            item = TwoLineListItem(
                text='Report Id: ' + str(row[0]),
                secondary_text='Title: ' + row[1],
                on_release=lambda x, row=row: self.open_dialog(row)
            )
            self.list_view.add_widget(item)

    def open_dialog(self, row):
        self.selected_report_id = row[0]
        self.dropdown_handler = DropDownHandler(self.screen)  # Store the reference to dropdown_handler
        content = BoxLayout(orientation='vertical')
        content.add_widget(self.dropdown_handler)

        self.dialog = MDDialog(title="Update Status",
                               type="custom",
                               content_cls=content,
                               size_hint=(0.7, 0),
                               buttons=[
                                   MDFlatButton(
                                       text="Submit",
                                       theme_text_color="Custom",
                                       text_color=self.theme_cls.primary_color,
                                       on_release=self.submit_data
                                   ),
                               ])
        self.dialog.open()

    def show_incident_type_dropdown(self, caller):
        dropdown_handler = DropDownHandler(caller)
        dropdown_handler.create_dropdown_menu()

    def submit_data(self, instance):
        new_status = self.dropdown_handler.selected_item  # Use the stored reference
        print('Selected Status: ' + new_status)
        cursor.execute("UPDATE report SET status = %s WHERE ReportId = %s", (new_status, self.selected_report_id))
        db.commit()
        self.dialog.dismiss()

MyApp().run()
