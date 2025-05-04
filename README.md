# BiblioNest Project

BiblioNest is a Django-based application for managing bibliographic references, collections, and tags. This guide will help you set up the development environment.

---

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- Python 3.12 or higher
- [Poetry](https://python-poetry.org/) (for dependency management)
- SQLite (default database for Django)

---

## Setup Instructions

### 1. Clone the Repository

Clone the project repository to your local machine:

```bash
git clone <repository-url>
cd biblionest_project1
```

### 2. Install Dependencies

Use Poetry to install the required dependencies:

```bash
poetry install
```

If Poetry's virtual environment is not activated automatically, activate it manually:

```bash
source $(poetry env info --path)/bin activate
```
### 3. Apply Migrations

Set up the database by applying migrations:

```bash
python BiblioDjango/manage.py migrate
```
### 4. Run the Development Server

Start the Django development server:

```bash
python BiblioDjango/manage.py runserver
```

Access the application in your browser at:


```bash
http://127.0.0.1:8000/
```