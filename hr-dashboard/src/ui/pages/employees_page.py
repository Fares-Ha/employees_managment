from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from ui.dialogs import EmployeeDialog
from services.staff_service import get_all_staff, add_staff

THUMB_SIZE = 50

class EmployeesPage(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)

        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels([
            "First Name","Last Name","DOB","Emirates ID","Passport #",
            "Salary","EID Front","EID Back","Passport Image"
        ])
        self.layout.addWidget(self.table)

        # Add Employee button at page level
        self.add_employee_btn = EmployeeDialogButton(self)
        self.layout.addWidget(self.add_employee_btn)

        self.load_data()

    def load_data(self):
        self.table.setRowCount(0)
        for row_idx, staff in enumerate(get_all_staff()):
            self.table.insertRow(row_idx)
            self.table.setItem(row_idx, 0, QTableWidgetItem(staff["first_name"]))
            self.table.setItem(row_idx, 1, QTableWidgetItem(staff["last_name"]))
            self.table.setItem(row_idx, 2, QTableWidgetItem(staff["dob"]))
            self.table.setItem(row_idx, 3, QTableWidgetItem(staff["emirates_id"]))
            self.table.setItem(row_idx, 4, QTableWidgetItem(staff["passport_number"]))
            self.table.setItem(row_idx, 5, QTableWidgetItem(f"$ {staff['salary']}"))

            # EID Front thumbnail
            eid_front_label = QLabel()
            if staff["emirates_id_front"]:
                pixmap = QPixmap(staff["emirates_id_front"]).scaled(THUMB_SIZE, THUMB_SIZE, Qt.AspectRatioMode.KeepAspectRatio)
                eid_front_label.setPixmap(pixmap)
            self.table.setCellWidget(row_idx, 6, eid_front_label)

            # EID Back thumbnail
            eid_back_label = QLabel()
            if staff["emirates_id_back"]:
                pixmap = QPixmap(staff["emirates_id_back"]).scaled(THUMB_SIZE, THUMB_SIZE, Qt.AspectRatioMode.KeepAspectRatio)
                eid_back_label.setPixmap(pixmap)
            self.table.setCellWidget(row_idx, 7, eid_back_label)

            # Passport thumbnail
            passport_label = QLabel()
            if staff["passport_img"]:
                pixmap = QPixmap(staff["passport_img"]).scaled(THUMB_SIZE, THUMB_SIZE, Qt.AspectRatioMode.KeepAspectRatio)
                passport_label.setPixmap(pixmap)
            self.table.setCellWidget(row_idx, 8, passport_label)


class EmployeeDialogButton(QWidget):
    def __init__(self, parent_page):
        super().__init__()
        self.parent_page = parent_page
        from PyQt6.QtWidgets import QPushButton, QHBoxLayout
        layout = QHBoxLayout(self)
        self.btn = QPushButton("Add Employee")
        self.btn.clicked.connect(self.open_dialog)
        layout.addWidget(self.btn)

    def open_dialog(self):
        dlg = EmployeeDialog(save_callback=self.save_employee)
        dlg.exec()

    def save_employee(self, data):
        add_staff(data)
        self.parent_page.load_data()
