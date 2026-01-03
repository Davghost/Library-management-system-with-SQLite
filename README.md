# Library Management System (CLI)

A command-line application written in Python to manage the catalog and loan operations of a small library. The system uses an SQLite database to provide persistent storage for books, readers, and loans.

The application runs in a continuous loop in the terminal and allows users to perform full CRUD operations, manage book loans and returns, and generate reports based on loan data.

---

## Project Purpose

This project was developed to meet the requirements of a technical challenge that focuses on database modeling, data persistence, and command-line interaction using Python.

The main goal is to manage three core entities:

* Books
* Readers
* Loans

---

## Technologies Used

* Python 3
* SQLite
* SQLAlchemy ORM
* Command Line Interface (CLI)

---

## Project Structure

```text
.
├── init_db.py     # Database connection and table creation
├── database.py    # Database operations and business logic
├── main.py        # Command-line interface and application loop
└── library.db     # SQLite database file (created automatically)
```

---

## Database Schema

### Book Table

* `id` (primary key)
* `title`
* `author`

### Reader Table

* `id` (primary key)
* `readers_name`

### Loan Table

* `id` (primary key)
* `book_id` (foreign key referencing Book)
* `reader_id` (foreign key referencing Reader)
* `loan_date`
* `return_date` (nullable)

---

## Application Features

### Book Management

* Create new books
* Update existing books
* Delete books
* List all books

### Reader Management

* Create new readers
* Update reader information
* Delete readers
* Retrieve readers by ID
* List all readers

### Loan Management

* Loan a book to a reader
* Prevent loans of already loaned books
* Register book returns

### Reports

* List all books currently loaned by a specific reader
* List all overdue books (loaned for more than 30 days)

---

## Business Rules

* A book cannot be loaned if it already has an active loan.
* A loan is considered active when `return_date` is null.
* When a book is returned, the return date is set to the current date.
* A book is considered overdue if it has been loaned for more than 30 days and has not been returned.

---

## How to Run the Application

### 1. (Optional) Create a virtual environment

```bash
python -m venv venv
```

Activate the virtual environment:

* Windows:

```bash
venv\Scripts\activate
```

* Linux/macOS:

```bash
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install sqlalchemy
```

### 3. Run the application

```bash
python main.py
```

The `library.db` file will be created automatically on the first run.

---

## Example Interaction

```text
=== Library Menu ===
1. Manage books
2. Manage readers
------------------
Type your choice: 1

You choose to manage books

=== Library Menu ===
1. Register book
2. Update book
3. Delete book
4. Return all books
5. Loans
6. Back
```

---

This application satisfies all the requirements defined in the project specification, including database initialization, CRUD operations, loan control, and report generation.
