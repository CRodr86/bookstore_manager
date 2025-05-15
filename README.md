# Bookstore Manager

A Django application to manage book inventory and automatic restock events, with a React frontend for user interactions.

---

## 🛠️ Prerequisites

* Docker & Docker Compose
* Python 3.12 (optional for local development)
* Node.js & npm (for local frontend development)
* PostgreSQL (Dockerized)

---

## 🚀 Quick Start

1. **Clone the repo** and navigate in:

   ```bash
   git clone <repo-url> && cd bookstore_manager
   ```
2. **Copy environment variables**:

   ```bash
   cp .env.example .env    # Django settings
   cp frontend/.env.example frontend/.env  # React settings
   ```
3. **Build & run with Docker**:

   ```bash
   docker-compose down --remove-orphans
   docker-compose up -d --build
   ```
4. **Apply migrations** (if not automatic):

   ```bash
   docker-compose run web python manage.py migrate
   ```
5. **Access the app**:

   * Backend API & Admin: [http://localhost:8000/](http://localhost:8000/)
   * Frontend UI:         [http://localhost:5173/](http://localhost:5173/)

---

## 👤 Creating Users

1. **Superuser (admin)**:

   ```bash
   docker-compose run web python manage.py createsuperuser
   ```
2. **Regular user** (via shell):

   ```bash
   docker-compose run web python manage.py shell
   ```

   ```python
   from django.contrib.auth.models import User
   User.objects.create_user('employee1', 'email@example.com', 'password123')
   ```

---

## 🔍 Running Tests

```bash
docker-compose run web python manage.py test books
```

---

## ⚙️ Configuration

* **Database**: PostgreSQL (service `db`)
* **Broker/Cache**: Redis (service `redis`)
* **Celery**: worker + beat for deferred restock
* **RESTOCK\_DELAY\_DAYS**: adjust in `.env`

---

## 🧩 Project Structure

```
bookstore_manager/
├── manage.py
├── bookstore_manager/    # Django project
├── books/                # Django app
├── Dockerfile            # Backend build
├── requirements.txt
├── .env
├── docker-compose.yml
├── frontend/             # React (Vite) app
└── README.md
```

---

## 🎨 Next Steps (Optional)

* Add **frontend authentication** (login/logout)
* Enhance **UI/UX styling**
* Deploy to production (Gunicorn + Nginx)

---

*This README covers the essentials to get the application up and running. Good luck!*
