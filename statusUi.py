import mysql.connector
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.list import MDList, TwoLineListItem
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDFlatButton
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window

# Kivy Builder String for the custom content layout
KV = '''
<DialogContent>:
    orientation: "vertical"
    spacing: "12dp"
    size_hint_y: None
    height: "100dp"

    MDTextField:
        id: status_field
        pos_hint: {'center_x': 0.5, 'center_y': 0.8}
        size_hint_x: None
        width: 300
        hint_text: "Enter the new status: [1] Preparing to deploy [2] On the Process [3] Resolved"
'''

# Custom content class for the dialog
class DialogContent(BoxLayout):
    pass

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

class ListApp(MDApp):
    def build(self):
        Builder.load_string(KV)  # Load the Kivy Builder string
        self.screen = Screen()
        self.theme_cls.primary_palette = "Green"
        scroll = ScrollView()
        self.list_view = MDList()
        scroll.add_widget(self.list_view)
        self.populate_list()
        self.screen.add_widget(scroll)
        return self.screen

    def populate_list(self):
        cursor.execute("SELECT ReportId, Title FROM report")
        rows = cursor.fetchall()  # Fetch all rows from the query

        for row in rows:
            item = TwoLineListItem(
                text='Report Id: ' + str(row[0]),  # ReportId
                secondary_text='Title: ' + row[1],  # Title
                on_release=lambda x, row=row: self.open_dialog(row)  # Add on_release callback
            )
            self.list_view.add_widget(item)

    def open_dialog(self, row):
        self.selected_report_id = row[0]  # Store the selected ReportId
        self.dialog = MDDialog(title="Update Status",
                               type="custom",
                               content_cls=DialogContent(),  # Use custom content class
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

    def submit_data(self, instance):
        new_status = self.dialog.content_cls.ids.status_field.text  # Get the new status from the text field
        # Define the mapping for the status
        status_map = {
            "1": "Preparing to deploy",
            "2": "On the Process",
            "3": "Resolved",
        }
        # Update the status for the specific reportId using a WHERE clause
        if new_status in status_map:
            updated_status = status_map[new_status]
            cursor.execute("UPDATE report SET status = %s WHERE ReportId = %s", (updated_status, self.selected_report_id))
            db.commit()
        self.dialog.dismiss()  # Close the dialog

listApp = ListApp()
listApp.run()
