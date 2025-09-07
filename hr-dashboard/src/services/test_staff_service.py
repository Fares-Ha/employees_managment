import unittest
import sqlite3
from unittest.mock import patch
from services.staff_service import add_staff, get_all_staff, update_staff, delete_staff

class TestStaffService(unittest.TestCase):

    def setUp(self):
        # Use a named in-memory database that can be shared across connections
        self.db_uri = 'file:memdb1?mode=memory&cache=shared'

        # Create a master connection to initialize and keep the DB alive
        self.master_conn = sqlite3.connect(self.db_uri, uri=True)
        self.master_conn.row_factory = sqlite3.Row

        # Create the schema
        self.master_conn.execute("""
            CREATE TABLE staff (
                id INTEGER PRIMARY KEY,
                first_name TEXT, last_name TEXT, dob TEXT,
                emirates_id TEXT, passport_number TEXT,
                emirates_id_front BLOB, emirates_id_back BLOB, passport_img BLOB,
                salary REAL
            )
        """)

    def tearDown(self):
        # Close the master connection, which will delete the in-memory DB
        self.master_conn.close()

    def get_new_connection(self):
        # This function will be the side_effect of our mock.
        # It returns a new connection to the same in-memory database.
        conn = sqlite3.connect(self.db_uri, uri=True)
        conn.row_factory = sqlite3.Row
        return conn

    @patch('services.staff_service.get_connection')
    def test_add_and_get_staff_with_salary(self, mock_get_connection):
        """Test that salary is correctly added to the database."""
        mock_get_connection.side_effect = self.get_new_connection

        staff_data = {
            "first_name": "John", "last_name": "Doe", "dob": "1990-01-01",
            "emirates_id": "12345", "passport_number": "A12345678",
            "emirates_id_front": b"front_img_data", "emirates_id_back": b"back_img_data",
            "passport_img": b"passport_img_data", "salary": 60000.0
        }
        add_staff(staff_data)

        staff_list = get_all_staff()
        self.assertEqual(len(staff_list), 1)
        self.assertEqual(staff_list[0]["salary"], 60000.0)

    @patch('services.staff_service.get_connection')
    def test_update_staff_with_salary(self, mock_get_connection):
        """Test that salary is correctly updated in the database."""
        mock_get_connection.side_effect = self.get_new_connection

        # Add a staff member first
        staff_data = {
            "first_name": "Jane", "last_name": "Doe", "dob": "1992-02-02",
            "emirates_id": "67890", "passport_number": "B67890",
            "emirates_id_front": b"front_img_data_2", "emirates_id_back": b"back_img_data_2",
            "passport_img": b"passport_img_data_2", "salary": 70000.0
        }
        add_staff(staff_data)

        staff_list = get_all_staff()
        staff_id = staff_list[0]["id"]

        # Update the salary
        updated_data = staff_data.copy()
        updated_data["salary"] = 80000.0
        update_staff(staff_id, updated_data)

        updated_staff_list = get_all_staff()
        self.assertEqual(updated_staff_list[0]["salary"], 80000.0)

    @patch('services.staff_service.get_connection')
    def test_delete_staff(self, mock_get_connection):
        """Test that a staff member can be deleted from the database."""
        mock_get_connection.side_effect = self.get_new_connection

        # Add a staff member first
        staff_data = {
            "first_name": "Peter", "last_name": "Jones", "dob": "1985-05-05",
            "emirates_id": "11223", "passport_number": "C112233",
            "emirates_id_front": b"front_img_data_3", "emirates_id_back": b"back_img_data_3",
            "passport_img": b"passport_img_data_3", "salary": 90000.0
        }
        add_staff(staff_data)

        # Check the staff member was added
        staff_list = get_all_staff()
        self.assertEqual(len(staff_list), 1)
        staff_id = staff_list[0]["id"]

        # Delete the staff member
        delete_staff(staff_id)

        # Check the staff member was deleted
        staff_list = get_all_staff()
        self.assertEqual(len(staff_list), 0)
