from core.database import get_connection

def get_total_employees():
    """
    Returns the total number of employees.
    """
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT COUNT(id) FROM staff")
    total = c.fetchone()[0]
    conn.close()
    return total

def get_average_salary():
    """
    Returns the average salary of all employees.
    """
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT AVG(salary) FROM staff")
    avg_salary = c.fetchone()[0]
    conn.close()
    return avg_salary if avg_salary is not None else 0

def get_salary_distribution():
    """
    Returns the number of employees in different salary brackets.
    """
    conn = get_connection()
    c = conn.cursor()

    brackets = {
        "< 30k": (0, 30000),
        "30k - 50k": (30000, 50000),
        "50k - 80k": (50000, 80000),
        "> 80k": (80000, 10000000) # A large number for the upper bound
    }

    distribution = {}
    for label, (lower, upper) in brackets.items():
        c.execute("SELECT COUNT(id) FROM staff WHERE salary >= ? AND salary < ?", (lower, upper))
        count = c.fetchone()[0]
        distribution[label] = count

    conn.close()
    return distribution

def get_employees_by_dob_year():
    """
    Returns the number of employees for each year of birth.
    """
    conn = get_connection()
    c = conn.cursor()
    # Assuming dob is stored as 'YYYY-MM-DD'
    c.execute("SELECT strftime('%Y', dob) as year, COUNT(id) as count FROM staff GROUP BY year ORDER BY year")
    rows = c.fetchall()
    conn.close()
    return {row['year']: row['count'] for row in rows}
