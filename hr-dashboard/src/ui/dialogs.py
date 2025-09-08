from PyQt6.QtWidgets import QDialog, QFormLayout, QLineEdit, QPushButton, QDateEdit, QVBoxLayout, QMessageBox, QFileDialog, QDoubleSpinBox
from PyQt6.QtCore import QDate
from ui.animations import fade_in_widget

class EmployeeDialog(QDialog):
    def __init__(self, parent=None, data=None, save_callback=None):
        super().__init__(parent)
        self.setWindowTitle("Add / Edit Employee")
        self.resize(400, 400)
        self.setWindowOpacity(0)

        self.save_callback = save_callback

        layout = QVBoxLayout(self)
        form = QFormLayout()
        layout.addLayout(form)

        self.first_name = QLineEdit()
        self.last_name = QLineEdit()
        self.position = QLineEdit()
        self.dob = QDateEdit()
        self.dob.setCalendarPopup(True)
        self.dob.setDate(QDate.currentDate())
        self.emirates_id = QLineEdit()
        self.passport_number = QLineEdit()
        self.salary = QDoubleSpinBox()
        self.salary.setMaximum(1_000_000)
        self.salary.setPrefix("$ ")
        self.salary.setValue(0)

        # Image paths
        self.emirates_id_front_path = ""
        self.emirates_id_back_path = ""
        self.passport_img_path = ""

        self.btn_eid_front = QPushButton("Select Emirates ID Front")
        self.btn_eid_back = QPushButton("Select Emirates ID Back")
        self.btn_passport = QPushButton("Select Passport Image")

        self.btn_eid_front.clicked.connect(lambda: self.select_file("eid_front"))
        self.btn_eid_back.clicked.connect(lambda: self.select_file("eid_back"))
        self.btn_passport.clicked.connect(lambda: self.select_file("passport"))

        form.addRow("First Name", self.first_name)
        form.addRow("Last Name", self.last_name)
        form.addRow("Position", self.position)
        form.addRow("Date of Birth", self.dob)
        form.addRow("Emirates ID", self.emirates_id)
        form.addRow("Passport Number", self.passport_number)
        form.addRow("Salary", self.salary)
        form.addRow("Emirates ID Front", self.btn_eid_front)
        form.addRow("Emirates ID Back", self.btn_eid_back)
        form.addRow("Passport Image", self.btn_passport)

        self.save_btn = QPushButton("Add Employee")
        self.save_btn.clicked.connect(self.save_employee)
        layout.addWidget(self.save_btn)

        if data:
            self.first_name.setText(data.get("first_name",""))
            self.last_name.setText(data.get("last_name",""))
            self.position.setText(data.get("position", ""))
            self.dob.setDate(QDate.fromString(data.get("dob","2000-01-01"), "yyyy-MM-dd"))
            self.emirates_id.setText(data.get("emirates_id",""))
            self.passport_number.setText(data.get("passport_number",""))
            self.salary.setValue(float(data.get("salary",0)))
            self.emirates_id_front_path = data.get("emirates_id_front","")
            self.emirates_id_back_path = data.get("emirates_id_back","")
            self.passport_img_path = data.get("passport_img","")
        # Fade in animation
        fade_in_widget(self)

    def select_file(self, field):
        path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Images (*.png *.jpg *.jpeg)")
        if path:
            if field == "eid_front":
                self.emirates_id_front_path = path
                self.btn_eid_front.setText(path.split("/")[-1])
            elif field == "eid_back":
                self.emirates_id_back_path = path
                self.btn_eid_back.setText(path.split("/")[-1])
            elif field == "passport":
                self.passport_img_path = path
                self.btn_passport.setText(path.split("/")[-1])

    def get_data(self):
        return {
            "first_name": self.first_name.text().strip(),
            "last_name": self.last_name.text().strip(),
            "position": self.position.text().strip(),
            "dob": self.dob.date().toString("yyyy-MM-dd"),
            "emirates_id": self.emirates_id.text().strip(),
            "passport_number": self.passport_number.text().strip(),
            "salary": self.salary.value(),
            "emirates_id_front": self.emirates_id_front_path,
            "emirates_id_back": self.emirates_id_back_path,
            "passport_img": self.passport_img_path
        }

    def save_employee(self):
        data = self.get_data()
        if not data["first_name"] or not data["last_name"]:
            QMessageBox.warning(self, "Error", "First and Last name are required!")
            return
        if self.save_callback:
            self.save_callback(data)
        self.accept()
