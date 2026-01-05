# db.py

import sqlite3

def connect_db(db_name):
    """Connection to SQLite-Database; database file is passed as parameter"""
    conn = sqlite3.connect(db_name)
    return conn

def create_table(conn, table_name):
    """Create table with specified table name - be aware of the rest is hardcoded."""
    cursor = conn.cursor()
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
        	TagID	INTEGER NOT NULL UNIQUE,
	        Code	TEXT NOT NULL UNIQUE,
	        Unit	TEXT NOT NULL,
	        Category_German	TEXT,
	        Category	TEXT,
	        Description_German	TEXT,
	        PRIMARY KEY("TagID")
        );
    ''')
    conn.commit()

def insert_data_from_csv(conn, table_name, data):
    """Insert data from csv file to specified table - be aware of the rest is hardcoded"""
    cursor = conn.cursor()
    cursor.executemany(f"INSERT OR IGNORE INTO {table_name} (TagID, Code, Unit, Category_German, Category, Description_German) VALUES (?, ?, ?, ?, ?, ?)", data)
    conn.commit()

def fetch_all_data(conn, table_name):
    """Get all data from specified table"""
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    return cursor.fetchall()

def close_db(conn):
    """Close database connection"""
    conn.close()

def create_table_energy_values(conn, table_name):
    """Create table with specified table name - be aware of the rest is hardcoded."""
    #For timestamps you will need as type DATETIME
    cursor = conn.cursor()
    #Your code here
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            TagID INTEGER NOT NULL UNIQUE PRIMARY KEY,
            Timestamp DATETIME NOT NULL PRIMARY KEY,
            Value REAL NOT NULL,
        );
    ''')
    conn.commit()
    conn.commit()

def insert_data_from_energy_values_csv(conn, table_name, data):
    """Insert data from csv file to specified table - be aware of the rest is hardcoded"""
    cursor = conn.cursor()
    cursor.execute('PRAGMA journal_mode=OFF;')
    cursor.execute('PRAGMA synchronous=OFF;')

    # Transaction Begin
    cursor.execute('BEGIN TRANSACTION;')

    # Add Data via Batch
    batch_size = 10000
    for i in range(0, len(data), batch_size):
        batch = data[i:i + batch_size]
        # Your code here (similar to the other insert but the data you use here is called "batch" - see the line before

        # First row - header (TagID from the different data points)
        if i == 0:
            tag_ids = batch[0][1:]  # TagIDs from second column onward
            continue

        # First column - Timestamp
        # All other cells - Values
        # Flatten using nested list comprehension (single pass)
        records = [
            (tag_id, row[0], value)
            for row in batch
            for tag_id, value in zip(tag_ids, row[1:])
        ]

        cursor.executemany(
            f'INSERT OR IGNORE INTO {table_name} (TagID, Timestamp, Value) VALUES (?, ?, ?)',
            records
        )
        conn.commit()

    # Close transaction
    conn.commit()


def fetch_all_data_floor_counter_values(conn):
    """Get all data from the energy counter values for the floors of the Building (OG1 - OG11)"""
    cursor = conn.cursor()
    # Your code here
    # This will return all values with 5min Timestamps for the whole year but only for 11 TagID (OG1 until OG 11)
    # To combine two tables have a look on the slides of Data Management Part 2: Slide 27
    # For finding a specific sequence in a string you have to use the word "like" in your statement
    # Placeholder % stands for any character
    # Example: SELECT * FROM users WHERE name LIKE 'John%';
    # John% means: All names that begin with “John” and have any characters after them.
    # So this example select selects all attributes stored in the table users where the name starts with John
    # Query 1: Get all data where the TagID belongs to the EnergyMeters where the "Description_German" Field consists of "2P1_Gesamt_OG" and the "Unit" is "MWh"
    # (this will provide the energy counter values of all floors of the building)
    cursor.execute(f'''
        SELECT ev.TagID, ev.Timestamp, ev.Value 
        FROM EnergyMeterValues ev
        WHERE ev.TagID = em.TagID
            AND ev.Description_German LIKE '%2P1_Gesamt_OG%'
            AND ev.Unit = 'MWh';
    ''')
    conn.commit()

    return cursor.fetchall()

def fetch_average_day_power_floors(conn):
    """Get the average of a day for the whole year for all floors of the Building (OG1 - OG11)"""
    cursor = conn.cursor()
    # Your code here
    # This will return 365 values for each floor from OG1 until OG11
    # Date(Timestamp) AS day -> this in the select will give you based on the timestamp the day
    # like before you have to combine both tables in the database - think of the value which is in both tables to combine the two tables
    # Have a look on the slides of Data Management Part 2: Slide 27, Slide 28, Slide 29, Slide 30
    # You can try out your select statements first in the DB Browser - there you see directly if it is working out (it will take some time since it has to calculate 4015 values)
    # for making clear in which table you are searching which columns use some characters to identify your table:
    # Example select a.name, b.address from user a, addressinformation b where a.id=b.id will give you the name stored in the user table, the address stored in the addressinformation table where the id exists in both tables

    cursor.execute(f'''
            
        ''')
    conn.commit()

    return cursor.fetchall()