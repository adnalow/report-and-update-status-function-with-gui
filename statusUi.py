import mysql.connector
from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.list import MDList, TwoLineListItem
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window

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

Window.size = (360, 600)

class listApp(MDApp):

    def build(self):
        screen = Screen()
        scroll = ScrollView()
        list_view = MDList()
        scroll.add_widget(list_view)

        cursor.execute("SELECT ReportId, Title FROM report")
        rows = cursor.fetchall()  # Fetch all rows from the query

        for row in rows:
            item = TwoLineListItem(
                text='Report Id: ' + str(row[0]),  # ReportId
                secondary_text='Title: ' + row[1],  # Title
                on_release=self.open_dialog  # Add on_release callback
            )
            list_view.add_widget(item)
                
        screen.add_widget(scroll)
        return screen

    def open_dialog(self, list_item):
        # MDTextField choice 2 update
        self.choice2_input = MDTextField(
            pos_hint={'center_x': 0.5, 'center_y': 0.2},
            size_hint_x=None,
            width=500,
            hint_text="Enter the new status: [1]Preparing to deploy [2]On the Process [3]Resolved: "
        )
        dialog = MDDialog(title="Item Selected",
                          text=f"You selected {list_item.text}.",
                          size_hint=(0.7, 0))
        dialog.open()
        self.some_other_function(list_item)  # Call another function

    def some_other_function(self, list_item):
        # Your code here
        print(f"Function called for {list_item.text}")

listApp().run()
