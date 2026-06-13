"""
═══════════════════════════════════════════════════════════
VANI — Synthetic Data Generator
Generates realistic Nepali SME business data for development.

Output: CSV files in datasets/synthetic/
DO NOT use for training. Data generation only.
═══════════════════════════════════════════════════════════
"""

import os
import random
import pandas as pd
from datetime import datetime, timedelta

# ═══════════════════════════════════════════════════════════
# Configuration
# ═══════════════════════════════════════════════════════════

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'datasets', 'synthetic')
os.makedirs(OUTPUT_DIR, exist_ok=True)

SEED = 42
random.seed(SEED)

# ═══════════════════════════════════════════════════════════
# Nepali Name Data
# ═══════════════════════════════════════════════════════════

NEPALI_FIRST_NAMES = [
    "Ram", "Shyam", "Hari", "Sita", "Gita", "Krishna", "Laxmi", "Bishnu",
    "Durga", "Sarita", "Bikash", "Sunil", "Anita", "Mina", "Raju", "Gopal",
    "Kamala", "Binod", "Prabha", "Santosh", "Manish", "Deepak", "Sunita",
    "Rekha", "Rajesh", "Mahesh", "Ganesh", "Nabin", "Suman", "Devi",
    "Prakash", "Binita", "Roshan", "Puspa", "Saroj", "Nirmala", "Dipendra",
    "Sabina", "Bibek", "Puja", "Arun", "Keshav", "Indra", "Sabin",
    "Tara", "Uma", "Yogesh", "Bimal", "Kopila", "Ramesh", "Suresh",
    "Kamal", "Rita", "Nisha", "Bijay", "Sandip", "Kiran", "Basanta",
    "Madan", "Bhim", "Asha", "Tulsi", "Lok", "Dil", "Chandra",
    "Narayan", "Mohan", "Prem", "Tek", "Bal", "Dev", "Jaya",
    "Meena", "Shanti", "Radha", "Saraswati", "Parvati", "Janaki", "Ambika"
]

NEPALI_LAST_NAMES = [
    "Sharma", "Adhikari", "Gautam", "Basnet", "Thapa", "Gurung", "Tamang",
    "Rai", "Limbu", "Magar", "Shrestha", "Maharjan", "Pradhan", "Joshi",
    "Poudel", "Ghimire", "Bhattarai", "Sapkota", "Regmi", "Pandey",
    "Acharya", "Dhakal", "Khadka", "Bhandari", "Karki", "KC", "Oli",
    "Lamichhane", "Neupane", "Rijal", "Subedi", "Dahal", "Pokhrel",
    "Giri", "Pant", "Koirala", "Devkota", "Sitaula", "Chaudhary",
    "Shah", "Yadav", "Mandal", "Mishra", "Tiwari", "Singh", "Lama",
    "Sherpa", "Budathoki", "Bista", "Raut"
]

NEPAL_DISTRICTS = [
    "Kathmandu", "Lalitpur", "Bhaktapur", "Pokhara", "Biratnagar",
    "Birgunj", "Dharan", "Butwal", "Hetauda", "Itahari",
    "Janakpur", "Nepalgunj", "Dhangadhi", "Bharatpur", "Tulsipur",
    "Ghorahi", "Siddharthanagar", "Damak", "Mechinagar", "Lahan"
]

NEPAL_TOLES = [
    "Thamel", "New Baneshwor", "Kalimati", "Balaju", "Chabahil",
    "Jorpati", "Koteshwor", "Kalanki", "Satdobato", "Lagankhel",
    "Mangalbazar", "Sukedhara", "Maharajgunj", "Lazimpat", "Putalisadak",
    "Naxal", "Gongabu", "Boudha", "Swayambhu", "Kirtipur",
    "Thankot", "Godawari", "Sundarijal", "Budhanilkantha", "Kapan"
]

# ═══════════════════════════════════════════════════════════
# Product Data (Nepali SME realistic inventory)
# ═══════════════════════════════════════════════════════════

PRODUCT_CATEGORIES = {
    "Electronics": [
        "Laptop", "Desktop Computer", "Mobile Phone", "Tablet", "Smart Watch",
        "Headphones", "Bluetooth Speaker", "Power Bank", "USB Cable", "Charger",
        "Mouse", "Keyboard", "Monitor", "Printer", "Scanner",
        "Webcam", "Microphone", "Router", "Modem", "Hard Drive",
        "Pen Drive", "Memory Card", "HDMI Cable", "Extension Board", "UPS"
    ],
    "Stationery": [
        "Notebook", "Pen", "Pencil", "Eraser", "Ruler",
        "Stapler", "Paper Clip", "Folder", "File Cover", "Marker",
        "Whiteboard", "Chalk", "Register", "Envelope", "Glue Stick",
        "Scissors", "Tape", "Calculator", "Punching Machine", "Stamp Pad"
    ],
    "Grocery": [
        "Rice (Basmati)", "Rice (Local)", "Dal (Masoor)", "Dal (Chana)",
        "Sugar", "Salt", "Oil (Mustard)", "Oil (Sunflower)", "Ghee",
        "Tea (Ilam)", "Coffee", "Milk Powder", "Biscuit", "Noodles",
        "Flour (Maida)", "Flour (Atta)", "Spice (Turmeric)", "Spice (Chili)",
        "Soap", "Detergent"
    ],
    "Hardware": [
        "Hammer", "Screwdriver Set", "Pliers", "Wrench", "Drill Machine",
        "Saw", "Nails (1kg)", "Screws Pack", "Paint (1L)", "Brush",
        "Cement (50kg)", "Sand (cubic ft)", "Rod (12mm)", "Pipe (PVC)",
        "Wire (Electrical)", "Switch Board", "Bulb (LED)", "Tube Light",
        "Fan (Ceiling)", "Lock"
    ],
    "Clothing": [
        "T-Shirt", "Shirt", "Pants", "Jeans", "Jacket",
        "Sweater", "Kurta", "Sari", "Dhoti", "Topi (Nepali Cap)",
        "Shawl", "Scarf", "Socks", "Belt", "Handkerchief",
        "School Uniform", "Sports Wear", "Raincoat", "Sandals", "Shoes"
    ],
    "Pharmacy": [
        "Paracetamol", "Ibuprofen", "Amoxicillin", "Cetrizine", "ORS Packet",
        "Bandage", "Cotton", "Antiseptic", "Cough Syrup", "Vitamin C",
        "Calcium Tablet", "Iron Supplement", "Eye Drops", "Ear Drops",
        "Pain Relief Balm", "Hand Sanitizer", "Face Mask", "Thermometer",
        "Blood Pressure Monitor", "Glucose Strips"
    ]
}

# ═══════════════════════════════════════════════════════════
# Departments & Positions for Employees
# ═══════════════════════════════════════════════════════════

DEPARTMENTS = ["Sales", "Inventory", "Accounts", "HR", "IT", "Management", "Customer Service", "Logistics"]
POSITIONS = [
    "Manager", "Assistant Manager", "Executive", "Officer", "Supervisor",
    "Clerk", "Helper", "Cashier", "Accountant", "Guard",
    "Driver", "Delivery Person", "Intern", "Trainee", "Senior Executive"
]

# ═══════════════════════════════════════════════════════════
# Phone number generator (Nepal format)
# ═══════════════════════════════════════════════════════════

NEPAL_PHONE_PREFIXES = ["984", "985", "986", "980", "981", "982", "974", "975", "976"]

def generate_phone():
    prefix = random.choice(NEPAL_PHONE_PREFIXES)
    return f"+977-{prefix}{random.randint(1000000, 9999999)}"

def generate_email(first_name, last_name):
    domains = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "mail.com"]
    sep = random.choice([".", "_", ""])
    num = random.randint(1, 999) if random.random() > 0.5 else ""
    return f"{first_name.lower()}{sep}{last_name.lower()}{num}@{random.choice(domains)}"

def generate_address():
    tole = random.choice(NEPAL_TOLES)
    district = random.choice(NEPAL_DISTRICTS)
    ward = random.randint(1, 32)
    return f"{tole}-{ward}, {district}"


# ═══════════════════════════════════════════════════════════
# 1. Generate Customers (10,000)
# ═══════════════════════════════════════════════════════════

def generate_customers(n=10000):
    print(f"Generating {n} customers...")
    customers = []
    for i in range(1, n + 1):
        first = random.choice(NEPALI_FIRST_NAMES)
        last = random.choice(NEPALI_LAST_NAMES)
        customers.append({
            "customer_id": i,
            "name": f"{first} {last}",
            "phone": generate_phone(),
            "email": generate_email(first, last) if random.random() > 0.3 else "",
            "address": generate_address(),
            "credit_balance": round(random.uniform(0, 50000), 2) if random.random() > 0.5 else 0
        })
    df = pd.DataFrame(customers)
    path = os.path.join(OUTPUT_DIR, "customers.csv")
    df.to_csv(path, index=False)
    print(f"  ✅ Saved {len(df)} customers to {path}")
    return df


# ═══════════════════════════════════════════════════════════
# 2. Generate Products (5,000)
# ═══════════════════════════════════════════════════════════

def generate_products(n=5000):
    print(f"Generating {n} products...")
    products = []
    pid = 1
    for _ in range(n):
        category = random.choice(list(PRODUCT_CATEGORIES.keys()))
        product_name = random.choice(PRODUCT_CATEGORIES[category])
        # Add variant suffix to make names more unique
        variant = random.choice(["", " (Small)", " (Medium)", " (Large)", " (Premium)", " (Standard)", " (Budget)"])
        brand = random.choice(["", "CG ", "Goldstar ", "Himalayan ", "Everest ", "Nepal ", "Yeti "])

        # Price ranges by category
        price_ranges = {
            "Electronics": (500, 150000),
            "Stationery": (10, 2000),
            "Grocery": (20, 5000),
            "Hardware": (50, 25000),
            "Clothing": (200, 15000),
            "Pharmacy": (20, 5000)
        }
        min_p, max_p = price_ranges[category]

        products.append({
            "product_id": pid,
            "product_name": f"{brand}{product_name}{variant}".strip(),
            "price": round(random.uniform(min_p, max_p), 2),
            "stock": random.randint(0, 500),
            "category": category
        })
        pid += 1

    df = pd.DataFrame(products)
    path = os.path.join(OUTPUT_DIR, "products.csv")
    df.to_csv(path, index=False)
    print(f"  ✅ Saved {len(df)} products to {path}")
    return df


# ═══════════════════════════════════════════════════════════
# 3. Generate Sales (100,000)
# ═══════════════════════════════════════════════════════════

def generate_sales(n=100000, num_customers=10000, num_products=5000):
    print(f"Generating {n} sales records...")
    sales = []
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2026, 6, 13)
    delta = (end_date - start_date).days

    for i in range(1, n + 1):
        cid = random.randint(1, num_customers)
        pid = random.randint(1, num_products)
        qty = random.randint(1, 20)
        unit_price = round(random.uniform(50, 50000), 2)
        amount = round(unit_price * qty, 2)
        sale_date = start_date + timedelta(days=random.randint(0, delta))

        sales.append({
            "sale_id": i,
            "customer_id": cid,
            "product_id": pid,
            "quantity": qty,
            "amount": amount,
            "date": sale_date.strftime("%Y-%m-%d")
        })

    df = pd.DataFrame(sales)
    path = os.path.join(OUTPUT_DIR, "sales.csv")
    df.to_csv(path, index=False)
    print(f"  ✅ Saved {len(df)} sales records to {path}")
    return df


# ═══════════════════════════════════════════════════════════
# 4. Generate Invoices (5,000)
# ═══════════════════════════════════════════════════════════

def generate_invoices(n=5000, num_customers=10000):
    print(f"Generating {n} invoices...")
    invoices = []
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2026, 6, 13)
    delta = (end_date - start_date).days
    statuses = ["pending", "paid", "overdue", "cancelled", "partial"]

    for i in range(1, n + 1):
        amount = round(random.uniform(500, 200000), 2)
        tax = round(amount * 0.13, 2)  # Nepal VAT is 13%
        total = round(amount + tax, 2)
        inv_date = start_date + timedelta(days=random.randint(0, delta))
        due_date = inv_date + timedelta(days=random.choice([7, 15, 30, 45, 60]))

        invoices.append({
            "invoice_id": i,
            "customer_id": random.randint(1, num_customers),
            "amount": amount,
            "tax_amount": tax,
            "total_amount": total,
            "status": random.choices(statuses, weights=[30, 40, 15, 5, 10])[0],
            "due_date": due_date.strftime("%Y-%m-%d"),
            "date": inv_date.strftime("%Y-%m-%d")
        })

    df = pd.DataFrame(invoices)
    path = os.path.join(OUTPUT_DIR, "invoices.csv")
    df.to_csv(path, index=False)
    print(f"  ✅ Saved {len(df)} invoices to {path}")
    return df


# ═══════════════════════════════════════════════════════════
# 5. Generate Employees (500)
# ═══════════════════════════════════════════════════════════

def generate_employees(n=500):
    print(f"Generating {n} employees...")
    employees = []
    for i in range(1, n + 1):
        first = random.choice(NEPALI_FIRST_NAMES)
        last = random.choice(NEPALI_LAST_NAMES)
        dept = random.choice(DEPARTMENTS)
        pos = random.choice(POSITIONS)

        # Salary ranges by position
        salary_map = {
            "Manager": (40000, 80000),
            "Assistant Manager": (30000, 50000),
            "Senior Executive": (25000, 45000),
            "Executive": (20000, 35000),
            "Officer": (18000, 30000),
            "Supervisor": (20000, 35000),
            "Accountant": (22000, 40000),
            "Cashier": (15000, 25000),
            "Clerk": (12000, 20000),
            "Helper": (10000, 18000),
            "Guard": (12000, 18000),
            "Driver": (15000, 25000),
            "Delivery Person": (12000, 22000),
            "Intern": (5000, 12000),
            "Trainee": (8000, 15000)
        }
        min_s, max_s = salary_map.get(pos, (15000, 30000))
        hired = datetime(2020, 1, 1) + timedelta(days=random.randint(0, 2000))

        employees.append({
            "employee_id": i,
            "name": f"{first} {last}",
            "department": dept,
            "position": pos,
            "attendance": random.choice([True, True, True, True, False]),  # 80% present
            "salary": round(random.uniform(min_s, max_s), 2),
            "phone": generate_phone(),
            "email": generate_email(first, last),
            "hired_date": hired.strftime("%Y-%m-%d")
        })

    df = pd.DataFrame(employees)
    path = os.path.join(OUTPUT_DIR, "employees.csv")
    df.to_csv(path, index=False)
    print(f"  ✅ Saved {len(df)} employees to {path}")
    return df


# ═══════════════════════════════════════════════════════════
# Main Execution
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("🇳🇵 VANI — Synthetic Data Generator")
    print("=" * 60)
    print()

    customers_df = generate_customers(10000)
    products_df = generate_products(5000)
    sales_df = generate_sales(100000)
    invoices_df = generate_invoices(5000)
    employees_df = generate_employees(500)

    print()
    print("=" * 60)
    print("✅ All synthetic data generated successfully!")
    print(f"📁 Output directory: {os.path.abspath(OUTPUT_DIR)}")
    print("=" * 60)
    print()
    print("Summary:")
    print(f"  • Customers:  {len(customers_df):,}")
    print(f"  • Products:   {len(products_df):,}")
    print(f"  • Sales:      {len(sales_df):,}")
    print(f"  • Invoices:   {len(invoices_df):,}")
    print(f"  • Employees:  {len(employees_df):,}")
    print()
    print("⚠️  To load into PostgreSQL, run:")
    print("    psql -U postgres -d vani -f database/schema.sql")
    print("    Then use COPY commands or a loader script.")
