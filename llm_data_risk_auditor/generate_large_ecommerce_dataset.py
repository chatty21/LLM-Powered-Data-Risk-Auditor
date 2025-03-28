import pandas as pd
import numpy as np
import random
from faker import Faker
from datetime import timedelta
import os

# ---------------------- CONFIG ---------------------- #
OUTPUT_FILE = "ecommerce_orders_500mb.csv"
NUM_ROWS = 4_000_000  # ~500MB depending on column length
SEED = 42
# ---------------------------------------------------- #

random.seed(SEED)
np.random.seed(SEED)
fake = Faker()
Faker.seed(SEED)

categories = ['Electronics', 'Clothing', 'Books', 'Home', 'Beauty', 'Sports']
payment_methods = ['Card', 'UPI', 'Cash', 'Wallet']

def generate_chunk(start_id, chunk_size):
    data = {
        "OrderID": [f"O{start_id + i}" for i in range(chunk_size)],
        "UserID": [f"U{start_id + i}" for i in range(chunk_size)],
        "UserName": [fake.name() for _ in range(chunk_size)],
        "Email": [fake.email() for _ in range(chunk_size)],
        "PhoneNumber": [fake.phone_number() if random.random() > 0.15 else None for _ in range(chunk_size)],
        "Gender": [random.choice(['Male', 'Female', 'Other']) for _ in range(chunk_size)],
        "Age": [random.randint(18, 70) for _ in range(chunk_size)],
        "Country": [fake.country() for _ in range(chunk_size)],
        "ProductID": [f"P{random.randint(100, 999)}" for _ in range(chunk_size)],
        "Category": [random.choice(categories) for _ in range(chunk_size)],
        "Price": [round(random.uniform(5.0, 500.0), 2) for _ in range(chunk_size)],
        "Quantity": [random.randint(1, 5) for _ in range(chunk_size)],
        "PaymentMethod": [random.choice(payment_methods) for _ in range(chunk_size)],
        "OrderDate": [fake.date_between(start_date='-1y', end_date='today') for _ in range(chunk_size)],
    }

    df = pd.DataFrame(data)
    df["TotalAmount"] = df["Price"] * df["Quantity"]
    df["DeliveryDate"] = pd.to_datetime(df["OrderDate"]) + pd.to_timedelta(np.random.randint(2, 10, size=chunk_size), unit='D')
    df["IsReturned"] = np.random.choice([0, 1], size=chunk_size, p=[0.7, 0.3])
    return df

# ---------------------- MAIN ---------------------- #
print(f"Generating {NUM_ROWS} rows. This may take several minutes...")

CHUNK_SIZE = 100_000
chunks = NUM_ROWS // CHUNK_SIZE
first_chunk = True

for i in range(chunks):
    df_chunk = generate_chunk(start_id=i * CHUNK_SIZE, chunk_size=CHUNK_SIZE)
    df_chunk.to_csv(OUTPUT_FILE, index=False, mode='a', header=first_chunk)
    first_chunk = False
    print(f"Chunk {i+1}/{chunks} written")

print(f"\n✅ Done! File saved as: {os.path.abspath(OUTPUT_FILE)}")