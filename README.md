# 📝 Todo App — FastAPI + SQLAlchemy

A RESTful Todo API built with **FastAPI** and **SQLAlchemy** (async). It supports user authentication (signup/login with JWT) and full CRUD operations on todos, where each user can only manage their own tasks.

---

## 🚀 What This Project Does

- **User Signup & Login** — Register with email/password; login to receive a JWT access token.
- **JWT Authentication** — All todo endpoints are protected. Passwords are hashed with bcrypt.
- **Create Todos** — Add new todo items linked to the authenticated user.
- **View Todos** — Retrieve all todos belonging to the logged-in user.
- **Update Todos** — Edit the title or toggle the completed status of a todo.
- **Delete Todos** — Remove a todo (only if you own it).
- **Async SQLite Database** — Uses `aiosqlite` for non-blocking database operations.

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| FastAPI | Web framework / API |
| SQLAlchemy (async) | ORM & database models |
| aiosqlite | Async SQLite driver |
| Pydantic | Request/response validation |
| python-jose | JWT token creation & verification |
| passlib (bcrypt) | Password hashing |
| Uvicorn | ASGI server |

---

## 📁 Project Structure

```
todo/
├── app/
│   ├── __init__.py        # Package initializer
│   ├── main.py            # FastAPI app & all API routes
│   ├── models.py          # SQLAlchemy models (Todo, User)
│   ├── schemas.py         # Pydantic schemas for validation
│   ├── database.py        # Async engine, session & table creation
│   └── auth_utils.py      # Password hashing, JWT utils, auth dependency
├── requirement.txt        # Python dependencies
├── venv/                  # Virtual environment (not committed)
└── README.md
```

---

## ⚙️ Setup & Installation

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd todo
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**macOS / Linux:**
```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirement.txt
```

### 5. Run the Application

```bash
uvicorn app.main:app --reload
```

The server will start at **http://127.0.0.1:8000**.

### 6. Open the API Docs

FastAPI auto-generates interactive documentation:

- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 📡 API Endpoints

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/signup` | Register a new user (email & password) |
| `POST` | `/login` | Login and receive a JWT access token |

### Todos (🔒 Requires Bearer Token)

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/add` | Create a new todo |
| `GET` | `/todos` | Get all todos for the logged-in user |
| `PUT` | `/update/{todo_id}` | Update a todo's title or completed status |
| `DELETE` | `/delete/{todo_id}` | Delete a todo |

---

## 🔐 Authentication Flow

1. **Sign up** via `POST /signup` with `email` and `password`.
2. **Log in** via `POST /login` (form data: `username` = your email, `password` = your password).
3. You will receive an `access_token` in the response.
4. For all todo endpoints, include the token in the `Authorization` header:
   ```
   Authorization: Bearer <your_access_token>
   ```

---

## 📌 Example Usage (cURL)

**Sign Up:**
```bash
curl -X POST http://127.0.0.1:8000/signup \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "mypassword"}'
```

**Log In:**
```bash
curl -X POST http://127.0.0.1:8000/login \
  -d "username=user@example.com&password=mypassword"
```

**Add a Todo:**
```bash
curl -X POST http://127.0.0.1:8000/add \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries"}'
```

**Get My Todos:**
```bash
curl http://127.0.0.1:8000/todos \
  -H "Authorization: Bearer <token>"
```

---

## 📝 License

This project is open-source and available under the [MIT License](LICENSE).
