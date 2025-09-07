from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableView,
                             QHeaderView, QLineEdit, QComboBox, QAbstractItemView, QLabel)
from PyQt6.QtGui import QStandardItemModel, QStandardItem, QPixmap
from PyQt6.QtCore import Qt

from services.staff_service import get_all_staff, get_staff_by_id, update_staff, delete_staff
from ui.dialogs import EmployeeDialog

THUMB_SIZE = 50

class EmployeesPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        # Top bar with controls
        self.controls_layout = QHBoxLayout()
        self.layout.addLayout(self.controls_layout)

        # Search and filter
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search...")
        self.search_input.textChanged.connect(self.on_search_or_filter_changed)
        self.controls_layout.addWidget(self.search_input)

        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["All Salaries", "Salary > 50k", "Salary <= 50k"])
        self.filter_combo.currentIndexChanged.connect(self.on_search_or_filter_changed)
        self.controls_layout.addWidget(self.filter_combo)

        self.controls_layout.addStretch()

        # Action buttons
        self.add_button = QPushButton("Add Employee")
        self.add_button.clicked.connect(self.add_employee)
        self.controls_layout.addWidget(self.add_button)

        self.edit_button = QPushButton("Edit Employee")
        self.edit_button.clicked.connect(self.edit_employee)
        self.controls_layout.addWidget(self.edit_button)

        self.delete_button = QPushButton("Delete Employee")
        self.delete_button.clicked.connect(self.delete_employee)
        self.controls_layout.addWidget(self.delete_button)

        # Employee table
        self.table_view = QTableView()
        self.model = QStandardItemModel()
        self.table_view.setModel(self.model)
        self.layout.addWidget(self.table_view)

        self.setup_table()
        self.load_staff_data()

    def setup_table(self):
        self.model.setHorizontalHeaderLabels([
            "ID", "First Name", "Last Name", "DOB", "Emirates ID",
            "Passport Number", "Salary", "EID Front", "EID Back", "Passport"
        ])
        header = self.table_view.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_view.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_view.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table_view.setSortingEnabled(True)
        self.table_view.setAlternatingRowColors(True)

    def on_search_or_filter_changed(self):
        search_term = self.search_input.text()
        filter_index = self.filter_combo.currentIndex()

        salary_filter = None
        if filter_index == 1:
            salary_filter = "gt_50k"
        elif filter_index == 2:
            salary_filter = "lt_50k"

        self.load_staff_data(search_term=search_term, salary_filter=salary_filter)

    def load_staff_data(self, search_term=None, salary_filter=None):
        self.model.removeRows(0, self.model.rowCount())
        staff_list = get_all_staff(search_term=search_term, salary_filter=salary_filter)
        for row_idx, staff in enumerate(staff_list):
            row = [
                QStandardItem(str(staff['id'])),
                QStandardItem(staff['first_name']),
                QStandardItem(staff['last_name']),
                QStandardItem(staff['dob']),
                QStandardItem(staff['emirates_id']),
                QStandardItem(staff['passport_number']),
                QStandardItem(f"${staff['salary']:.2f}"),
            ]
            self.model.appendRow(row)

            # Image thumbnails
            self.add_thumbnail(row_idx, 7, staff.get("emirates_id_front"))
            self.add_thumbnail(row_idx, 8, staff.get("emirates_id_back"))
            self.add_thumbnail(row_idx, 9, staff.get("passport_img"))

    def add_thumbnail(self, row, col, image_path):
        if image_path:
            pixmap = QPixmap(image_path).scaled(THUMB_SIZE, THUMB_SIZE, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            label = QLabel()
            label.setPixmap(pixmap)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table_view.setIndexWidget(self.model.index(row, col), label)

    def add_employee(self):
        dialog = EmployeeDialog(save_callback=self.save_new_employee)
        dialog.exec()

    def save_new_employee(self, data):
        from services.staff_service import add_staff
        add_staff(data)
        self.on_search_or_filter_changed()

    def edit_employee(self):
        selected_rows = self.table_view.selectionModel().selectedRows()
        if not selected_rows:
            return

        staff_id_item = self.model.item(selected_rows[0].row(), 0)
        staff_id = int(staff_id_item.text())

        staff_data = get_staff_by_id(staff_id)
        if not staff_data:
            return

        dialog = EmployeeDialog(data=staff_data, save_callback=lambda data: self.save_edited_employee(staff_id, data))
        dialog.exec()

    def save_edited_employee(self, staff_id, data):
        update_staff(staff_id, data)
        self.on_search_or_filter_changed()

    def delete_employee(self):
        selected_rows = self.table_view.selectionModel().selectedRows()
        if not selected_rows:
            return

        staff_id_item = self.model.item(selected_rows[0].row(), 0)
        staff_id = int(staff_id_item.text())

        delete_staff(staff_id)
        self.on_search_or_filter_changed()
