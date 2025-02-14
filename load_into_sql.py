import os
import csv
import mysql.connector
import re
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# MySQL connection configuration (without specifying the database initially)
db_config_no_db = {
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
    'host': os.getenv("DB_HOST"),
    'auth_plugin': os.getenv("DB_AUTH_PLUGIN"),  # Ensure MySQL uses caching_sha2_password
}

# Connect to MySQL (without database) to create it first
conn = mysql.connector.connect(**db_config_no_db)
cursor = conn.cursor()

# Create the database if it does not exist
database_name = "student_coworking_db"
cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name};")
print(f"Database `{database_name}` ensured.")

# Close the connection and reconnect with the new database
cursor.close()
conn.close()

# MySQL connection configuration (now including the database)
db_config= {
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
    'host': os.getenv("DB_HOST"),
    'database': database_name,
    'auth_plugin': os.getenv("DB_AUTH_PLUGIN"),  # Ensure MySQL uses caching_sha2_password
}

# Connect again using the newly created database
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# Create tables if they do not exist
create_table_queries = {
    'staff': """
        CREATE TABLE IF NOT EXISTS staff (
            staff_id INT PRIMARY KEY,
            salary DECIMAL(10,2),
            staff_name VARCHAR(50),
            department VARCHAR(50),
            made_by VARCHAR(50)
        );
    """,
    'study_room': """
        CREATE TABLE IF NOT EXISTS study_room (
            room_no INT PRIMARY KEY,
            capacity INT,
            hourly_rate DECIMAL(10,2),
            made_by VARCHAR(50)
        );
    """,
    'booking': """
        CREATE TABLE IF NOT EXISTS booking (
            booking_id INT PRIMARY KEY,
            booking_date DATE,
            booking_time TIME,
            booking_discount DECIMAL(10,2),
            made_by VARCHAR(50)
        );
    """,
    'payment': """
        CREATE TABLE IF NOT EXISTS payment (
            payment_id INT PRIMARY KEY,
            payment_mode VARCHAR(50),
            amount DECIMAL(10,2),
            made_by VARCHAR(50)
        );
    """,
    'student': """
        CREATE TABLE IF NOT EXISTS student (
            student_id INT PRIMARY KEY,
            student_name VARCHAR(50),
            contact_no VARCHAR(20),
            university VARCHAR(100),
            made_by VARCHAR(50)
        );
    """,
    'coworking_space': """
        CREATE TABLE IF NOT EXISTS coworking_space (
            brand_name VARCHAR(100),
            space_name VARCHAR(100),
            PRIMARY KEY (brand_name, space_name),
            made_by VARCHAR(50)
        );
    """
}

for table, query in create_table_queries.items():
    cursor.execute(query)
    print(f"Table `{table}` ensured.")

# Mapping CSV file names to table names and column orders
csv_to_table = {
    'staff.csv': {
        'table': 'staff',
        'columns': ['staff_id', 'staff_name', 'salary', 'department', 'made_by']
    },
    'study_room.csv': {
        'table': 'study_room',
        'columns': ['room_no', 'capacity', 'hourly_rate', 'made_by']
    },
    'booking.csv': {
        'table': 'booking',
        'columns': ['booking_id', 'booking_date', 'booking_time', 'booking_discount', 'made_by']
    },
    'payment.csv': {
        'table': 'payment',
        'columns': ['payment_id', 'payment_mode', 'amount', 'made_by']
    },
    'student.csv': {
        'table': 'student',
        'columns': ['student_id', 'student_name', 'contact_no', 'university', 'made_by']
    },
    'coworking_space.csv': {
        'table': 'coworking_space',
        'columns': ['brand_name', 'space_name', 'made_by']
    },
}

def clean_phone_number(phone):
    """Extract only digits from phone number and limit to BIGINT range"""
    cleaned = re.sub(r'\D', '', phone)  # Remove non-numeric characters
    return int(cleaned[:15]) if cleaned else None  # Convert to BIGINT, limit length

csv_folder = 'CSV'

# Process each CSV file in the folder
for csv_file, info in csv_to_table.items():
    file_path = os.path.join(csv_folder, csv_file)
    table_name = info['table']
    columns = info['columns']

    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        rows = [row for row in reader]

        # Prepare insert query – using parameterized queries
        col_str = ", ".join(columns)
        placeholders = ", ".join(["%s"] * len(columns))
        # insert_query = f"INSERT INTO {table_name} ({col_str}) VALUES ({placeholders})"
        insert_query = f"REPLACE INTO {table_name} ({col_str}) VALUES ({placeholders})"


        data_to_insert = []
        # for row in rows:
        #     # Ensure proper data types if needed
        #     values = [row[col] for col in columns]
        #     data_to_insert.append(values)
        for row in rows:
            values = []
            for col in columns:
                value = row[col]

                # Convert phone numbers to numeric only if it's the `contact_no` column
                if table_name == "student" and col == "contact_no":
                    value = clean_phone_number(value)

                values.append(value)

            data_to_insert.append(values)

        # Insert data into the table
        if data_to_insert:
            cursor.executemany(insert_query, data_to_insert)
            conn.commit()
            print(f"Inserted {cursor.rowcount} rows into `{table_name}`.")

cursor.close()
conn.close()
