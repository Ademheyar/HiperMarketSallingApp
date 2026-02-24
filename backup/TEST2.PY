import sqlite3

from C.API.Get import *
from C.API.API import *
from C.API.Set import *

def copy_data(source_database, destination_database, source_table, destination_table, source_column, destination_column):
    # Create connections to the source and destination databases
    source_connection = sqlite3.connect(f"{source_database}.db")
    destination_connection = sqlite3.connect(f"{destination_database}.db")
    source_cursor = source_connection.cursor()
    destination_cursor = destination_connection.cursor()

    # Get the ID-value pairs from the source table
    source_id_values = source_Update_table_database(f"SELECT id, {source_column} FROM {source_table}").fetchall()

    # Print the source table before making changes
    print("Source Table:")
    for id_value, value in source_id_values:
        print(f"{source_table}: id={id_value}, {source_column}={value}")

    # Print the destination table before making changes
    print("\nDestination Table (Before):")
    destination_values = destination_Update_table_database(f"SELECT id, {destination_column} FROM {destination_table}").fetchall()
    for id_value, value in destination_values:
        print(f"{destination_table}: id={id_value}, {destination_column}={value}")

    # Iterate over the ID-value pairs from the source table
    for id_value, value in source_id_values:
        # Check if the ID value exists in the destination table
        destination_row = destination_Update_table_database(
            f"SELECT * FROM {destination_table} WHERE id = {id_value}"
        ).fetchone()

        # If the ID value exists in the destination table, update the destination column with the value from the source column
        if destination_row is not None:
            destination_Update_table_database(
                f"UPDATE {destination_table} SET {destination_column} = '{value}' WHERE id = {id_value}"
            )
        else:
            # If the ID value does not exist in the destination table, insert a new row with the ID and value
            destination_Update_table_database(
                f"INSERT INTO {destination_table} (id, {destination_column}) VALUES ({id_value}, '{value}')"
            )

    # Commit the changes to the destination database
    destination_connection.commit()

    # Print the destination table after making changes
    print("\nDestination Table (After):")
    destination_values = destination_Update_table_database(f"SELECT id, {destination_column} FROM {destination_table}").fetchall()
    for id_value, value in destination_values:
        print(f"{destination_table}: id={id_value}, {destination_column}={value}")

    # Close the connections to the databases
    source_connection.close()
    destination_connection.close()

    
def copy_data_from_a_to_b():
    # Create the source database (a.db)
    source_connection = sqlite3.connect("a.db")
    source_cursor = source_connection.cursor()

    # Create the source table (at) if it doesn't exist
    source_Update_table_database("CREATE TABLE IF NOT EXISTS at (id INTEGER, ac TEXT)")
    source_connection.commit()

    # Check if the source table already contains the values
    source_Update_table_database("SELECT * FROM at")
    rows = source_cursor.fetchall()

    if not rows:
        # Insert values into the source table
        source_Update_table_database("INSERT INTO at (id, ac) VALUES (100, 'value1')")
        source_Update_table_database("INSERT INTO at (id, ac) VALUES (1, 'value2')")
        source_Update_table_database("INSERT INTO at (id, ac) VALUES (21, 'value3')")
        source_connection.commit()

    # Close the source database connection
    source_connection.close()

    # Create the destination database (b.db)
    destination_connection = sqlite3.connect("b.db")
    destination_cursor = destination_connection.cursor()

    # Create the destination table (bt) if it doesn't exist
    destination_Update_table_database("CREATE TABLE IF NOT EXISTS bt (id INTEGER, bc TEXT)")
    destination_connection.commit()

    # Check if the destination table already contains the values
    destination_Update_table_database("SELECT * FROM bt")
    rows = destination_cursor.fetchall()

    if not rows:
        # Insert values into the destination table
        destination_Update_table_database("INSERT INTO bt (id, bc) VALUES (0, 'value1')")
        destination_Update_table_database("INSERT INTO bt (id, bc) VALUES (1, 'value4')")
        destination_connection.commit()

    # Close the destination database connection
    destination_connection.close()

if __name__ == "__main__":
    copy_data_from_a_to_b()
    # Get the names of the source and destination databases from the user.
    source_database = input("Enter the name of the source database: ")
    destination_database = input("Enter the name of the destination database: ")

    # Get the names of the source and destination tables from the user.
    source_table = input("Enter the name of the source table: ")
    destination_table = input("Enter the name of the destination table: ")

    # Get the names of the source and destination columns from the user.
    source_column = input("Enter the name of the source column: ")
    destination_column = input("Enter the name of the destination column: ")

    # Copy the data from the source database to the destination database.
    copy_data(source_database, destination_database, source_table, destination_table, source_column, destination_column)

    # Print a message to the user indicating that the data has been copied.
    print("Data copied successfully!")
