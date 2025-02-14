import os
import csv
import random
from faker import Faker
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Initialize Faker instance
fake = Faker()

# Create CSV folder if it doesn't exist
csv_folder = 'CSV'
os.makedirs(csv_folder, exist_ok=True)

# Number of records to generate
num_records = 100

# Generate staff data
staff_data = [['staff_id', 'staff_name', 'salary', 'department', 'made_by']]
departments = ['Administration', 'IT', 'Marketing', 'HR', 'Finance']
for i in range(1, num_records + 1):
    staff_data.append([i, fake.name(), round(random.uniform(30000, 80000), 2), random.choice(departments), os.getenv("DB_MADE_BY")])

# Generate study room data
study_room_data = [['room_no', 'capacity', 'hourly_rate', 'made_by']]
for i in range(1, num_records + 1):
    study_room_data.append([i, random.randint(2, 10), round(random.uniform(15, 50), 2), os.getenv("DB_MADE_BY")])

# Generate booking data
booking_data = [['booking_id', 'booking_date', 'booking_time', 'booking_discount', 'made_by']]
for i in range(1, num_records + 1):
    random_date = fake.date_between(start_date='-1y', end_date='today')
    random_time = fake.time()
    discount = random.choice([0, 5, 10, 15])
    booking_data.append([i, random_date, random_time, discount, os.getenv("DB_MADE_BY")])

# Generate payment data
payment_data = [['payment_id', 'payment_mode', 'amount', 'made_by']]
payment_modes = ['Credit Card', 'Debit Card', 'Paypal', 'UPI', 'Bank Transfer']
for i in range(1, num_records + 1):
    payment_data.append([i, random.choice(payment_modes), round(random.uniform(50, 500), 2), os.getenv("DB_MADE_BY")])

# Generate student data
student_data = [['student_id', 'student_name','contact_no', 'university', 'made_by']]
universities = ['University A', 'University B', 'University C', 'University D']
for i in range(1, num_records + 1):
    student_data.append([i, fake.name(),fake.phone_number(), random.choice(universities), os.getenv("DB_MADE_BY")])

# Generate coworking space data
coworking_space_data = [['brand_name', 'space_name', 'made_by']]
brands = ['EduSpace', 'LearnHub', 'StudyNest', 'Knowledge Point']
for i in range(1, num_records + 1):
    coworking_space_data.append([random.choice(brands), f"Campus {i}", os.getenv("DB_MADE_BY")])

# Mapping of file names to data
files_data = {
    'staff.csv': staff_data,
    'study_room.csv': study_room_data,
    'booking.csv': booking_data,
    'payment.csv': payment_data,
    'student.csv': student_data,
    'coworking_space.csv': coworking_space_data,
}

# Write each CSV file
for file_name, data in files_data.items():
    file_path = os.path.join(csv_folder, file_name)
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)
    print(f"Generated {file_path} with {num_records} records.")