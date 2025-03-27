# Address Book Application

A simple Flask web application to manage contacts using a web interface and SQLite database.

---

## ✅ Features

- Add, edit, and delete contacts via web interface
- Contacts stored in SQLite using SQLAlchemy ORM
- Docker and Docker Compose support
- Clean project structure (modularized)

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd address_book
```

### 2. Create and activate virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
python main.py
```

Then open [http://localhost:5000](http://localhost:5000) in your browser.

---

## 🐳 Run with Docker Compose

### 1. Build and start the container

```bash
docker-compose up --build
```

### 2. Open in your browser

[http://localhost:5000](http://localhost:5000)

---

## 📂 Project Structure

```
address_book/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   ├── storage.py
│   └── templates/
│       └── index.html
├── contacts.db         # SQLite database (auto-created)
├── main.py             # Entry point
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── .dockerignore
```
