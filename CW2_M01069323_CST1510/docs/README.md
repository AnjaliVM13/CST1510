# CW2_M01069323_CST1510 – Multi-Domain Intelligence Platform

## Overview

This project implements a **professional, multi-domain intelligence platform** integrating:

* Cybersecurity Intelligence
* Data Governance Analytics
* IT Operations Ticketing
* Executive Summary Insights

It follows a clean **MVC-style architecture** using:

* **SQLite** (persistent local database)
* **Pandas** (CSV ingestion)
* **bcrypt** (secure password hashing)
* **Python modules** structured into data, services, and main application layers

---

##  Project Structure

```
CW2_M0123456_CST1510/
│
├─ app/
│  ├─ data/                    # Database layer (Model in MVC)
│  │  ├─ __init__.py
│  │  ├─ db.py                 # Database connection functions
│  │  ├─ schema.py             # CREATE TABLE statements
│  │  ├─ users.py              # User CRUD functions
│  │  ├─ incidents.py          # Cyber incidents CRUD
│  │  ├─ datasets.py           # Metadata CRUD
│  │  └─ tickets.py            # Ticket CRUD
│  │
│  └─ services/                # Business logic layer
│     ├─ __init__.py
│     └─ user_service.py       # User migration & authentication
│
├─ DATA/                       # Data files
│  ├─ users.txt
│  ├─ cyber_incidents.csv
│  ├─ datasets_metadata.csv
│  ├─ it_tickets.csv
│  └─ intelligence_platform.db # Auto-generated database
│
├─ docs/
│  └─ README.md                # Project documentation
│
├─ main.py                     # Entry point demo script
├─ requirements.txt            # Python dependencies
└─ .gitignore
```

---

## Features

### Fully Automated Database Setup

`main.py` performs:

1. Database connection
2. Table creation from schema
3. User migration from `users.txt`
4. CSV ingestion for all domains
5. Final verification report

### Secure Authentication

* Users stored with **bcrypt hashed passwords**
* Migration script automatically hashes plaintext entries

### CRUD Operations for All Domains

* Users
* Cyber Incidents
* Dataset Metadata
* IT Tickets

Each domain is modular and can be extended independently.

### Clean Modular Codebase

* Separation of concerns
* Easy to maintain
* Reusable helpers in `db.py`

---

## How to Run the Project

### **1. Install Requirements**

```bash
pip install -r requirements.txt
```

### **2. Ensure CSV + TXT files are inside the DATA/ folder**

```
DATA/
 ├ users.txt
 ├ cyber_incidents.csv
 ├ datasets_metadata.csv
 ├ it_tickets.csv
```

### **3. Run the main setup + demo script**

```bash
python main.py
```

You should see output like:

```
Users table created successfully!
Cyber Incidents table created successfully!
Datasets Metadata table created successfully!
IT Tickets table created successfully!
Migrated X users from users.txt
Loaded XYZ CSV rows
DATABASE SETUP COMPLETE!
```

---

## Demo Script (main.py)

The demo script does the following:

* Connects to the database
* Creates all tables
* Migrates users
* Loads CSV data
* Prints table row counts
* Demonstrates sample CRUD calls for each domain

---

## Module Descriptions

### **`app/data/db.py`**

* Handles connections
* Includes reusable `execute_query()` and `fetch_all()` wrappers

### **`app/data/schema.py`**

* Contains SQL `CREATE TABLE` statements
* Run once during setup

### **`app/data/users.py`**

CRUD operations:

* add_user()
* get_user_by_username()
* verify_credentials()

### **`app/services/user_service.py`**

* Reads `users.txt`
* Hashes passwords using bcrypt
* Migrates them into the database

### **`app/data/incidents.py`, `datasets.py`, `tickets.py`**

* Load from CSV
* Insert rows with validation
* Provide CRUD functions for analytics

---

## requirements.txt

```
pandas
bcrypt
streamlit
sqlite3-binary
python-dateutil

```

(This Python version already includes sqlite3)

---

## Conclusion

This project delivers a **robust, modular, secure intelligence platform** suitable for academic and professional environments. The documented structure allows easy expansion, integration, and debugging.
