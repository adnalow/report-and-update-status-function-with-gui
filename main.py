import mysql.connector
import random
from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.textfield import MDTextField


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
        self.screen = Screen()
        self.theme_cls.primary_palette = "Green"

        # MDTextField title 
        self.title_input = MDTextField(
            pos_hint={'center_x': 0.5, 'center_y': 0.9},
            size_hint_x=None,
            width=300,
            hint_text="Enter Title"
        )
        
        # MDTextField Choice
        self.choice_input = MDTextField(
            pos_hint={'center_x': 0.5, 'center_y': 0.8},
            size_hint_x=None,
            width=500,
            hint_text="Choose from any of the following [1]Robbery [2]Fire [3]Accident [4]Others:"
        )
        
        # MDTextField Image path
        self.imagePath_input = MDTextField(
            pos_hint={'center_x': 0.5, 'center_y': 0.7},
            size_hint_x=None,
            width=300,
            hint_text="Enter image path: "
        )
        
        # MDTextField details
        self.details_input = MDTextField(
            pos_hint={'center_x': 0.5, 'center_y': 0.6},
            size_hint_x=None,
            width=300,
            hint_text="Enter details:"
        )
        
        # MDTextField urgency
        self.urgency_input = MDTextField(
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            size_hint_x=None,
            width=300,
            hint_text="Enter urgency level (Low, Medium, High): "
        )
        
        # MDTextField status update
        self.statusUpdate_input = MDTextField(
            pos_hint={'center_x': 0.5, 'center_y': 0.3},
            size_hint_x=None,
            width=300,
            hint_text="Enter the reportID of the incident:"
        )
        # MDTextField choice 2 update
        self.choice2_input = MDTextField(
            pos_hint={'center_x': 0.5, 'center_y': 0.2},
            size_hint_x=None,
            width=500,
            hint_text="Enter the new status: [1]Preparing to deploy [2]On the Process [3]Resolved: "
        )

        # MDTextField title add
        self.screen.add_widget(self.title_input)
        # MDTextField Choice add
        self.screen.add_widget(self.choice_input)
        # MDTextField Image path add
        self.screen.add_widget(self.imagePath_input)
        # MDTextField details add
        self.screen.add_widget(self.details_input)
        # MDTextField urgency add
        self.screen.add_widget(self.urgency_input)
        # MDTextField status update add
        self.screen.add_widget(self.statusUpdate_input)
        # MDTextField choice2 add
        self.screen.add_widget(self.choice2_input)

        # Create and add the submit button
        button1 = MDRectangleFlatButton(
            text='Submit', 
            pos_hint={'center_x': 0.5, 'center_y': 0.4},
            on_release=self.submit_data
        )
        
        # Create and add the submit button
        button2 = MDRectangleFlatButton(
            text='Update Status', 
            pos_hint={'center_x': 0.5, 'center_y': 0.1},
            on_release=self.status_update
        )
        self.screen.add_widget(button1)
        self.screen.add_widget(button2)

        return self.screen

    def submit_data(self, obj):
        
        # for pre defined reports
        def report1():
            return "Robbery"
        
        def report2():
            return "Fire"
        
        def report3():
            return "Accident"
        
        def report4():
            return "Others"
        
        
        pre_defined_reports ={
            1: report1,
            2: report2,
            3: report3,
            4: report4,
        }
        
        reportID = random.randint(10, 999)
        print("ReportId:", reportID)
        # Title
        self.title = self.title_input.text
        print("Title:", self.title)
        # Checklist
        self.choice = self.choice_input.text
        self.checklist = pre_defined_reports[int(self.choice)]()
        print("Choice:", self.checklist)
        # Title
        self.imagePath = self.imagePath_input.text
        print("Title:", self.imagePath)
        # details
        self.details = self.details_input.text
        print("Title:", self.details)
        # urgency
        self.urgency = self.urgency_input.text
        print("Title:", self.urgency)
        #status
        status = "pending"

        # Insert user input into the database
        cursor.execute("INSERT INTO report (reportID, title, checklist, image_path, details, urgency, status) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (reportID, self.title, self.checklist, self.imagePath, self.details, self.urgency, status))
        
        cursor.execute("INSERT INTO statusUpdate (reportID, title, status) VALUES (%s, %s, %s)",
                (reportID, self.title, status))

        db.commit()
        
    def status_update(self, obj):
        def status1():
            return "Preparing to deploy"
        
        def status2():
            return "On the Process"
        
        def status3():
            return "Resolved"
        
        
        pre_defined_status ={
            1: status1,
            2: status2,
            3: status3,
        }
        self.choice2 = self.choice2_input.text
        newStatus = pre_defined_status[int(self.choice2)]()
        reportId_text = self.statusUpdate_input.text
        
        # Update the status for the specific reportId using a WHERE clause
        cursor.execute("UPDATE report SET status=%s WHERE reportId=%s", (newStatus, reportId_text))

        # Commit the changes to the database
        db.commit()
reportApp().run()

