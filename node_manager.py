import sqlite3
import uuid
from datetime import datetime


def create_connection(db_name="lms.db"):
    conn = sqlite3.connect(db_name)
    return conn


def add_record(conn, host, port):
    record_id = str(uuid.uuid4())  # Generate a unique UUID for the record
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Current timestamp
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO node_discovery (id, host, port, created_at)
        VALUES (?, ?, ?, ?)
        """,
        (record_id, host, port, created_at)
    )
    conn.commit()
    print(f"Record added with ID: {record_id}")


def delete_record(conn, record_id):
    """Delete a record from the node_discovery table by ID."""
    cursor = conn.cursor()
    cursor.execute(
        """
        DELETE FROM node_discovery
        WHERE id = ?
        """,
        (record_id,)
    )
    if cursor.rowcount > 0:
        conn.commit()
        print("Record deleted successfully.")
    else:
        print("No record found with the given ID.")


def view_records(conn):
    """View all records in the node_discovery table."""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM node_discovery")
    rows = cursor.fetchall()
    if rows:
        print("\nAll Records:")
        print(f"{'ID':<36} {'Host':<20} {'Port':<10} {'Created At'}")
        print("-" * 80)
        for row in rows:
            print(f"{row[0]:<36} {row[1]:<20} {row[2]:<10} {row[3]}")
    else:
        print("\nNo records found.")


def main():
    conn = create_connection()
    while True:
        print("\nMenu:")
        print("1. Add Record")
        print("2. Delete Record")
        print("3. View All Records")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            host = input("Enter host: ")
            port = input("Enter port: ")
            add_record(conn, host, port)
        elif choice == "2":
            record_id = input("Enter the ID of the record to delete: ")
            delete_record(conn, record_id)
        elif choice == "3":
            view_records(conn)
        elif choice == "4":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")
    conn.close()


if __name__ == "__main__":
    main()
