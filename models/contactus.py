import sqlite3 as s


def create_tbl(path: str) -> None:
    """Creates the contact_us table in the database

    Args:
        path: Path to database

    Returns:
            None: Table is created if it doesnt already exist
    """
    conn = s.connect(path)
    cur = conn.cursor()

    tbl = "CREATE TABLE IF NOT EXISTS contact_us(Email TEXT, Message TEXT)"
    cur.execute(tbl)
    conn.commit()


def insert(email: str, message: str, path: str) -> None:
    """Inserts message and email id from Contact_Us Page

    Args:
        email: User Email ID
        message: User Feedback Message
        path: Path to database

    Returns:
            None: Inserts data into table
    """
    conn = s.connect(path)
    cur = conn.cursor()

    insrt = f"INSERT INTO contact_us VALUES('{email}','{message}')"
    cur.execute(insrt)
    conn.commit()


if __name__ == "__main__":
    test_path = "../test.db"
    create_tbl(test_path)
