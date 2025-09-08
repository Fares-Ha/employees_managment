from core.database import get_connection

def add_staff(data):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        INSERT INTO staff 
        (first_name,last_name,dob,emirates_id,passport_number,emirates_id_front,emirates_id_back,passport_img,salary,position)
        VALUES (?,?,?,?,?,?,?,?,?,?)
    """, (
        data["first_name"], data["last_name"], data["dob"],
        data["emirates_id"], data["passport_number"],
        data["emirates_id_front"], data["emirates_id_back"], data["passport_img"],
        data["salary"], data.get("position", "")
    ))
    conn.commit()
    conn.close()

def get_all_staff():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM staff")
    columns = [description[0] for description in c.description]
    rows = [dict(zip(columns, row)) for row in c.fetchall()]
    conn.close()
    return rows

def update_staff(staff_id, data):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        UPDATE staff SET
        first_name=?, last_name=?, dob=?, emirates_id=?, passport_number=?,
        emirates_id_front=?, emirates_id_back=?, passport_img=?, salary=?, position=?
        WHERE id=?
    """, (
        data["first_name"], data["last_name"], data["dob"],
        data["emirates_id"], data["passport_number"],
        data["emirates_id_front"], data["emirates_id_back"], data["passport_img"],
        data["salary"], data.get("position", ""),
        staff_id
    ))
    conn.commit()
    conn.close()

def delete_staff(staff_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM staff WHERE id=?", (staff_id,))
    conn.commit()
    conn.close()
