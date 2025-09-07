from core.database import get_connection

def add_staff(data):
    """
    Adds a new staff member to the database.
    """
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        INSERT INTO staff
        (first_name,last_name,dob,emirates_id,passport_number,emirates_id_front,emirates_id_back,passport_img,salary)
        VALUES (?,?,?,?,?,?,?,?,?)
    """, (
        data["first_name"], data["last_name"], data["dob"],
        data["emirates_id"], data["passport_number"],
        data["emirates_id_front"], data["emirates_id_back"], data["passport_img"],
        data["salary"]
    ))
    conn.commit()
    conn.close()

def get_all_staff(search_term=None, salary_filter=None):
    """
    Retrieves all staff from the database, with optional search and filtering.
    """
    conn = get_connection()
    c = conn.cursor()

    base_query = "SELECT * FROM staff"
    conditions = []
    params = []

    if search_term:
        conditions.append("(first_name LIKE ? OR last_name LIKE ? OR emirates_id LIKE ? OR passport_number LIKE ?)")
        term = f"%{search_term}%"
        params.extend([term, term, term, term])

    if salary_filter:
        if salary_filter == "gt_50k":
            conditions.append("salary > ?")
            params.append(50000)
        elif salary_filter == "lt_50k":
            conditions.append("salary <= ?")
            params.append(50000)

    if conditions:
        query = f"{base_query} WHERE {' AND '.join(conditions)}"
        c.execute(query, tuple(params))
    else:
        c.execute(base_query)

    rows = [dict(row) for row in c.fetchall()]
    conn.close()
    return rows

def get_staff_by_id(staff_id):
    """
    Retrieves a single staff member by their ID.
    """
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM staff WHERE id=?", (staff_id,))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None

def update_staff(staff_id, data):
    """
    Updates an existing staff member in the database.
    """
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        UPDATE staff SET
        first_name=?, last_name=?, dob=?, emirates_id=?, passport_number=?,
        emirates_id_front=?, emirates_id_back=?, passport_img=?, salary=?
        WHERE id=?
    """, (
        data["first_name"], data["last_name"], data["dob"],
        data["emirates_id"], data["passport_number"],
        data["emirates_id_front"], data["emirates_id_back"], data["passport_img"],
        data["salary"],
        staff_id
    ))
    conn.commit()
    conn.close()

def delete_staff(staff_id):
    """
    Deletes a staff member from the database.
    """
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM staff WHERE id=?", (staff_id,))
    conn.commit()
    conn.close()
