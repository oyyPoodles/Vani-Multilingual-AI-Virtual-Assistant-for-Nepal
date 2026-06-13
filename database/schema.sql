-- ═══════════════════════════════════════════════════════════
-- VANI — Voice Assistant for Nepal Intelligence
-- Database Schema (PostgreSQL)
-- ═══════════════════════════════════════════════════════════

-- Enable UUID extension for future use
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ═══════════════════════════════════════════════════════════
-- TABLE: customers
-- Stores SME customer information
-- ═══════════════════════════════════════════════════════════
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(255),
    address TEXT,
    credit_balance DECIMAL(12,2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ═══════════════════════════════════════════════════════════
-- TABLE: products
-- Stores product/inventory information for SMEs
-- ═══════════════════════════════════════════════════════════
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    stock INTEGER DEFAULT 0,
    category VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ═══════════════════════════════════════════════════════════
-- TABLE: sales
-- Records individual sale transactions
-- ═══════════════════════════════════════════════════════════
CREATE TABLE sales (
    sale_id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(customer_id) ON DELETE SET NULL,
    product_id INTEGER REFERENCES products(product_id) ON DELETE SET NULL,
    quantity INTEGER DEFAULT 1,
    amount DECIMAL(12,2) NOT NULL,
    date DATE DEFAULT CURRENT_DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ═══════════════════════════════════════════════════════════
-- TABLE: employees
-- Stores employee records
-- ═══════════════════════════════════════════════════════════
CREATE TABLE employees (
    employee_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    department VARCHAR(100),
    position VARCHAR(100),
    attendance BOOLEAN DEFAULT TRUE,
    salary DECIMAL(10,2),
    phone VARCHAR(20),
    email VARCHAR(255),
    hired_date DATE DEFAULT CURRENT_DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ═══════════════════════════════════════════════════════════
-- TABLE: invoices
-- Tracks invoices generated for customers
-- ═══════════════════════════════════════════════════════════
CREATE TABLE invoices (
    invoice_id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(customer_id) ON DELETE SET NULL,
    amount DECIMAL(12,2) NOT NULL,
    tax_amount DECIMAL(10,2) DEFAULT 0,
    total_amount DECIMAL(12,2) NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    due_date DATE,
    date DATE DEFAULT CURRENT_DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ═══════════════════════════════════════════════════════════
-- TABLE: attendance_records
-- Tracks daily employee attendance
-- ═══════════════════════════════════════════════════════════
CREATE TABLE attendance_records (
    record_id SERIAL PRIMARY KEY,
    employee_id INTEGER REFERENCES employees(employee_id) ON DELETE CASCADE,
    date DATE DEFAULT CURRENT_DATE,
    check_in TIME,
    check_out TIME,
    status VARCHAR(20) DEFAULT 'present',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(employee_id, date)
);

-- ═══════════════════════════════════════════════════════════
-- TABLE: complaints
-- Citizen complaint tracking (governance feature)
-- ═══════════════════════════════════════════════════════════
CREATE TABLE complaints (
    complaint_id SERIAL PRIMARY KEY,
    citizen_name VARCHAR(255),
    phone VARCHAR(20),
    category VARCHAR(100),
    description TEXT NOT NULL,
    status VARCHAR(50) DEFAULT 'registered',
    assigned_to VARCHAR(255),
    resolution TEXT,
    date DATE DEFAULT CURRENT_DATE,
    resolved_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ═══════════════════════════════════════════════════════════
-- TABLE: government_services
-- Tracks government service applications
-- ═══════════════════════════════════════════════════════════
CREATE TABLE government_services (
    service_id SERIAL PRIMARY KEY,
    applicant_name VARCHAR(255) NOT NULL,
    service_type VARCHAR(100) NOT NULL,
    application_number VARCHAR(50) UNIQUE,
    status VARCHAR(50) DEFAULT 'submitted',
    office VARCHAR(255),
    submitted_date DATE DEFAULT CURRENT_DATE,
    estimated_completion DATE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ═══════════════════════════════════════════════════════════
-- INDEXES for performance
-- ═══════════════════════════════════════════════════════════
CREATE INDEX idx_sales_date ON sales(date);
CREATE INDEX idx_sales_customer ON sales(customer_id);
CREATE INDEX idx_invoices_customer ON invoices(customer_id);
CREATE INDEX idx_invoices_status ON invoices(status);
CREATE INDEX idx_attendance_date ON attendance_records(date);
CREATE INDEX idx_complaints_status ON complaints(status);
CREATE INDEX idx_gov_services_status ON government_services(status);
CREATE INDEX idx_gov_services_app_number ON government_services(application_number);
CREATE INDEX idx_products_category ON products(category);
CREATE INDEX idx_employees_department ON employees(department);
