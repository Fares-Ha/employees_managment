from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel, QHBoxLayout, QLineEdit, QComboBox
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, pyqtSignal
from ui.dialogs import EmployeeDialog
from ui.dialogs import ImagePreviewDialog
from services.staff_service import get_all_staff, add_staff
from core.translations import translator
from ui.toast import Toast

THUMB_SIZE = 50

class EmployeesPage(QWidget):
    staff_changed = pyqtSignal()

    def __init__(self):
        super().__init__()
        from PyQt6.QtWidgets import QHBoxLayout, QLineEdit, QComboBox, QLabel, QPushButton
        self.layout = QVBoxLayout(self)
        self.staff_data = []

        # Search, filter, and export/import bar
        search_filter_layout = QHBoxLayout()
        self.search_label = QLabel(translator.tr("Search"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(translator.tr("Search employees..."))
        self.search_input.textChanged.connect(self.load_data)
        search_filter_layout.addWidget(self.search_label)
        search_filter_layout.addWidget(self.search_input)

        # Salary filter (customizable)
        self.filter_salary_label = QLabel(translator.tr("Salary"))
        self.salary_from = QLineEdit()
        self.salary_from.setPlaceholderText(translator.tr("From"))
        self.salary_from.setFixedWidth(70)
        self.salary_to = QLineEdit()
        self.salary_to.setPlaceholderText(translator.tr("To"))
        self.salary_to.setFixedWidth(70)
        self.salary_from.textChanged.connect(self.load_data)
        self.salary_to.textChanged.connect(self.load_data)
        search_filter_layout.addWidget(self.filter_salary_label)
        search_filter_layout.addWidget(self.salary_from)
        search_filter_layout.addWidget(QLabel("-"))
        search_filter_layout.addWidget(self.salary_to)

        # DOB filter (customizable)
        self.filter_dob_label = QLabel(translator.tr("DOB"))
        self.dob_from = QLineEdit()
        self.dob_from.setPlaceholderText(translator.tr("From (YYYY-MM-DD)"))
        self.dob_from.setFixedWidth(110)
        self.dob_to = QLineEdit()
        self.dob_to.setPlaceholderText(translator.tr("To (YYYY-MM-DD)"))
        self.dob_to.setFixedWidth(110)
        self.dob_from.textChanged.connect(self.load_data)
        self.dob_to.textChanged.connect(self.load_data)
        search_filter_layout.addWidget(self.filter_dob_label)
        search_filter_layout.addWidget(self.dob_from)
        search_filter_layout.addWidget(QLabel("-"))
        search_filter_layout.addWidget(self.dob_to)

        # Export/Import buttons
        from PyQt6.QtWidgets import QPushButton, QFileDialog, QMessageBox
        self.export_btn = QPushButton(translator.tr("Export CSV"))
        self.export_btn.clicked.connect(self.export_csv)
        self.import_btn = QPushButton(translator.tr("Import CSV"))
        self.import_btn.clicked.connect(self.import_csv)
        search_filter_layout.addWidget(self.export_btn)
        search_filter_layout.addWidget(self.import_btn)

        self.table = QTableWidget()
        self.table.setColumnCount(10)
        self.table.setHorizontalHeaderLabels([
            "First Name","Last Name","DOB","Emirates ID","Passport #",
            "Salary","Position","EID Front","EID Back","Passport Image"
        ])
        self.table.setSortingEnabled(True)
        self.table.cellClicked.connect(self.on_cell_clicked)
        self.layout.addWidget(self.table)

        # Add Employee button at page level (top)
        from ui.pages.employees_page import EmployeeDialogButton
        self.add_employee_btn = EmployeeDialogButton(self)
        self.layout.addWidget(self.add_employee_btn)

        self.load_data()

        self.layout.addLayout(search_filter_layout)

        translator.language_changed.connect(self.update_translations)

    def on_cell_clicked(self, row, column):
        image_columns = {
            7: "emirates_id_front",
            8: "emirates_id_back",
            9: "passport_img"
        }
        if column in image_columns:
            # Check if the row index is valid
            if 0 <= row < len(self.staff_data):
                staff = self.staff_data[row]
                image_source = staff.get(image_columns[column])

                # Determine the image data to pass to the dialog
                image_data_for_dialog = None
                if isinstance(image_source, str): # It's a path
                    try:
                        with open(image_source, 'rb') as f:
                            image_data_for_dialog = f.read()
                    except FileNotFoundError:
                        pass # Image path is invalid, do nothing
                elif isinstance(image_source, bytes): # It's already bytes
                    image_data_for_dialog = image_source

                if image_data_for_dialog:
                    dialog = ImagePreviewDialog(image_data_for_dialog, self)
                    dialog.exec()

    def export_csv(self):
        import csv
        from services.staff_service import get_all_staff
        from PyQt6.QtWidgets import QFileDialog, QMessageBox
        file, _ = QFileDialog.getSaveFileName(self, "Export Employees to CSV", "employees.csv", "CSV Files (*.csv)")
        if file:
            staff = get_all_staff()
            if not staff:
                QMessageBox.warning(self, "No Data", "No employees to export.")
                return
            with open(file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=list(staff[0].keys()))
                writer.writeheader()
                writer.writerows(staff)
            Toast(f"Exported {len(staff)} employees to {file}", self).show()

    def update_translations(self):
        self.search_label.setText(translator.tr("Search"))
        self.search_input.setPlaceholderText(translator.tr("Search employees..."))
        self.filter_salary_label.setText(translator.tr("Salary"))
        self.salary_from.setPlaceholderText(translator.tr("From"))
        self.salary_to.setPlaceholderText(translator.tr("To"))
        self.filter_dob_label.setText(translator.tr("DOB"))
        self.dob_from.setPlaceholderText(translator.tr("From (YYYY-MM-DD)"))
        self.dob_to.setPlaceholderText(translator.tr("To (YYYY-MM-DD)"))
        self.export_btn.setText(translator.tr("Export CSV"))
        self.import_btn.setText(translator.tr("Import CSV"))

        self.table.setColumnCount(10)
        self.table.setHorizontalHeaderLabels([
            "First Name","Last Name","DOB","Emirates ID","Passport #",
            "Salary","Position","EID Front","EID Back","Passport Image"
        ])
        self.table.setSortingEnabled(True)
        self.layout.addWidget(self.table)

        self.load_data()

    def import_csv(self):
        import csv
        from services.staff_service import add_staff, get_all_staff
        from PyQt6.QtWidgets import QFileDialog, QMessageBox
        file, _ = QFileDialog.getOpenFileName(self, "Import Employees from CSV", "", "CSV Files (*.csv)")
        if file:
            reply = QMessageBox.question(self, "Import Employees", "Importing will add to existing employees. Continue?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply != QMessageBox.StandardButton.Yes:
                return
            with open(file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                count = 0
                for row in reader:
                    row.pop('id', None)
                    add_staff(row)
                    count += 1
            Toast(f"Imported {count} employees from {file}", self).show()
            self.load_data()
            self.staff_changed.emit()

    def load_data(self):
        self.table.setRowCount(0)
        search_text = self.search_input.text().lower() if hasattr(self, 'search_input') else ""
        salary_from = self.salary_from.text().strip()
        salary_to = self.salary_to.text().strip()
        dob_from = self.dob_from.text().strip()
        dob_to = self.dob_to.text().strip()

        self.staff_data = []
        for staff in get_all_staff():
            if search_text:
                if not any(search_text in str(staff.get(field, "")).lower() for field in ["first_name","last_name","emirates_id","passport_number"]):
                    continue
            salary = float(staff.get("salary", 0))
            if salary_from:
                try:
                    if salary < float(salary_from):
                        continue
                except ValueError:
                    pass
            if salary_to:
                try:
                    if salary > float(salary_to):
                        continue
                except ValueError:
                    pass
            dob = staff.get("dob", "")
            if dob_from and dob < dob_from:
                continue
            if dob_to and dob > dob_to:
                continue
            self.staff_data.append(staff)

        from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QWidget, QMessageBox
        from core.translations import translator
        self.table.setColumnCount(11)
        self.table.setHorizontalHeaderLabels([
            translator.tr("First Name"), translator.tr("Last Name"), translator.tr("DOB"), translator.tr("Emirates ID"), translator.tr("Passport Number"),
            translator.tr("Salary"), translator.tr("Position"), translator.tr("EID Front"), translator.tr("EID Back"), translator.tr("Passport Image"), translator.tr("Actions")
        ])
        for row_idx, staff in enumerate(self.staff_data):
            self.table.insertRow(row_idx)
            self.table.setItem(row_idx, 0, QTableWidgetItem(staff["first_name"]))
            self.table.setItem(row_idx, 1, QTableWidgetItem(staff["last_name"]))
            self.table.setItem(row_idx, 2, QTableWidgetItem(staff["dob"]))
            self.table.setItem(row_idx, 3, QTableWidgetItem(staff["emirates_id"]))
            self.table.setItem(row_idx, 4, QTableWidgetItem(staff["passport_number"]))
            self.table.setItem(row_idx, 5, QTableWidgetItem(f"$ {staff['salary']}"))
            self.table.setItem(row_idx, 6, QTableWidgetItem(staff.get("position", "") or staff.get("job", "")))

            # --- Start of new image loading logic ---
            def create_image_label(image_source):
                label = QLabel()
                if not image_source:
                    return label

                pixmap = QPixmap()
                if isinstance(image_source, str):
                    pixmap.load(image_source) # Load from path
                else:
                    pixmap.loadFromData(image_source) # Load from bytes

                if not pixmap.isNull():
                    label.setPixmap(pixmap.scaled(THUMB_SIZE, THUMB_SIZE, Qt.AspectRatioMode.KeepAspectRatio))
                return label

            self.table.setCellWidget(row_idx, 7, create_image_label(staff.get("emirates_id_front")))
            self.table.setCellWidget(row_idx, 8, create_image_label(staff.get("emirates_id_back")))
            self.table.setCellWidget(row_idx, 9, create_image_label(staff.get("passport_img")))
            # --- End of new image loading logic ---

            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(0,0,0,0)
            edit_btn = QPushButton(translator.tr("Edit"))
            delete_btn = QPushButton(translator.tr("Delete"))
            edit_btn.setStyleSheet("background:#2980b9; color:white; border-radius:5px; padding:4px 10px;")
            delete_btn.setStyleSheet("background:#c0392b; color:white; border-radius:5px; padding:4px 10px;")
            actions_layout.addWidget(edit_btn)
            actions_layout.addWidget(delete_btn)
            self.table.setCellWidget(row_idx, 10, actions_widget)

            import functools
            def edit_row(staff):
                from ui.dialogs import EmployeeDialog
                from services.staff_service import update_staff
                dlg = EmployeeDialog(data=staff, save_callback=lambda d: self._edit_callback(staff["id"], d))
                dlg.exec()
            def delete__row(staff):
                from services.staff_service import delete_staff
                reply = QMessageBox.question(self, translator.tr("Delete Employee"), translator.tr("Delete {first} {last}?", first=staff['first_name'], last=staff['last_name']), QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                if reply == QMessageBox.StandardButton.Yes:
                    delete_staff(staff["id"])
                    self.load_data()
                    self.staff_changed.emit()
                    Toast(translator.tr("Employee deleted!"), self).show()
            edit_btn.clicked.connect(functools.partial(edit_row, staff))
            delete_btn.clicked.connect(functools.partial(delete_row, staff))

    def _edit_callback(self, staff_id, data):
        from services.staff_service import update_staff
        update_staff(staff_id, data)
        self.load_data()
        self.staff_changed.emit()
        Toast(translator.tr("Employee updated!"), self).show()


class EmployeeDialogButton(QWidget):
    def __init__(self, parent_page):
        super().__init__()
        self.parent_page = parent_page
        from PyQt6.QtWidgets import QPushButton, QHBoxLayout
        layout = QHBoxLayout(self)
        from core.translations import translator
        self.btn = QPushButton(translator.tr("Add Employee"))
        self.btn.clicked.connect(self.open_dialog)
        layout.addWidget(self.btn)
        translator.language_changed.connect(self.update_translation)

    def update_translation(self):
        from core.translations import translator
        self.btn.setText(translator.tr("Add Employee"))

    def open_dialog(self):
        dlg = EmployeeDialog(save_callback=self.save_employee)
        dlg.exec()

    def save_employee(self, data):
        add_staff(data)
        self.parent_page.load_data()
        self.parent_page.staff_changed.emit()
        Toast(translator.tr("Employee added!"), self.parent_page).show()
