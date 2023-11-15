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
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.menu import MDDropdownMenu
from kivy.properties import ObjectProperty

# Kivy Builder String for the custom content layout
KV = '''
<DialogContent>:
    orientation: "vertical"
    size_hint_y: None
    height: "400dp"

    ScrollView:
        size_hint_y: None
        height: 400  # Adjust based on your dialog box size

        GridLayout:
            cols: 1
            size_hint_y: None
            size_hint_x: 1  # Take full width of the ScrollView
            height: self.minimum_height
            spacing: "30dp"
            padding: [30, 60, 30, 30]  # Padding: [left, top, right, bottom]
            pos_hint: {'center_x': 0.5, 'top': 50}  # Adjust pos_hint as needed

            MDLabel:
                id: title
                text: "label text"
                halign: "center"  # Align text within the label
                size_hint_y: (1)
                height: self.texture_size[1]
                
            MDLabel:
                id: checklist
                text: "label text"
                halign: "center"  # Align text within the label
                size_hint_y: None
                height: self.texture_size[1]
            
            MDLabel:
                id: image_path
                text: "label text"
                halign: "center"  # Align text within the label
                size_hint_y: None
                height: self.texture_size[1]
                
            MDLabel:
                id: details
                text: "label text"
                halign: "center"  # Align text within the label
                size_hint_y: None
                height: self.texture_size[1]
                
            MDLabel:
                id: urgency
                text: "label text"
                halign: "center"  # Align text within the label
                size_hint_y: None
                height: self.texture_size[1]
            
            MDLabel:
                id: status
                text: "label text"
                halign: "center"  # Align text within the label
                size_hint_y: None
                height: self.texture_size[1]
                
            MDLabel:
                id: dateCreated
                text: "label text"
                halign: "center"  # Align text within the label
                size_hint_y: None
                height: self.texture_size[1]
            
    BoxLayout:
        orientation: 'vertical'
        size_hint_y: None
        height: "48dp"  # Fixed height for the button area

        MDRaisedButton:
            id: button
            text: "Select Status"
            pos_hint: {"center_x": 0.5, "center_y": 0.5}
            on_release: app.menu_callback()
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
    
    dropdown = ObjectProperty()
    
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

    # displaying the reports
    def open_dialog(self, row):
        self.selected_report_id = row[0]  # Store the selected ReportId

        # Fetch data for the selected report
        cursor.execute("SELECT Title, Checklist, image_Path, Details, Urgency, Status, dateCreated FROM report WHERE ReportId = %s", (self.selected_report_id,))
        data = cursor.fetchone()

        # Create dialog content
        self.dialog_content = DialogContent()

        if data:
            # Update label texts
            self.dialog_content.ids.title.text = "Title: " + str(data[0])
            self.dialog_content.ids.checklist.text = "Checklist: " + str(data[1])
            self.dialog_content.ids.image_path.text = "Image Path: " + str(data[2])
            self.dialog_content.ids.details.text = "Details: " + str(data[3])
            self.dialog_content.ids.urgency.text = "Urgency: " + str(data[4])
            self.dialog_content.ids.status.text = "Status: " + str(data[5])
            if data[6] is None or data[6] == '':
                self.dialog_content.ids.dateCreated.text = "Date: Unknown"
            else:
                self.dialog_content.ids.dateCreated.text = "Date: " + str(data[6])


        self.dialog = MDDialog(title="Update Status",
                               type="custom",
                               content_cls=self.dialog_content,  # Use custom content class
                               size_hint=(0.8, None),
                               buttons=[
                                   MDFlatButton(
                                       text="Submit",
                                       theme_text_color="Custom",
                                       text_color=self.theme_cls.primary_color,
                                       on_release=self.submit_data
                                   ),
                               ])
        self.dialog.open()
        self.create_dropdown_menu()

    def create_dropdown_menu(self):
        menu_items = [
            {"viewclass": "OneLineListItem", "text": "Preparing to deploy"},
            {"viewclass": "OneLineListItem", "text": "On the Process"},
            {"viewclass": "OneLineListItem", "text": "Resolved"}
        ]

        self.dropdown = MDDropdownMenu(
            caller=self.dialog_content.ids.button,
            items=menu_items,
            width_mult=4
        )

        for item in menu_items:
            item['on_release'] = lambda x=item['text']: self.option_callback(x)

    def menu_callback(self):
        self.dropdown.open()

    def option_callback(self, option_text):
        self.new_status = option_text
        print(option_text)
        self.dropdown.dismiss()

    def submit_data(self, instance):
        cursor.execute("UPDATE report SET status = %s WHERE ReportId = %s", (self.new_status, self.selected_report_id))
        db.commit()
        self.dialog.dismiss()

listApp = ListApp()
listApp.run()
