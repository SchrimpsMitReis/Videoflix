# Create the README.md file with the provided content

content = """# 🎬 Videoflix Backend

A Netflix-like backend built with **Django REST Framework**, featuring video streaming via **HLS (m3u8 + ts segments)**, authentication, and email verification.

---

## 🚀 Features

* 🔐 User Registration & Login (JWT / Cookie-based)
* 📧 Account Activation via Email (MailHog in development)
* 🎥 Video Upload & Processing (ffmpeg)
* 📺 HLS Streaming (adaptive-ready)
* 🖼️ Thumbnail Handling
* 🐳 Fully Docker-based
* ⚡ Background Jobs via Redis (django-rq)

---

## 🧱 Tech Stack

* Python / Django
* Django REST Framework
* PostgreSQL
* Redis
* Docker & Docker Compose
* ffmpeg
* MailHog (for development emails)

---

## ⚙️ Installation (Development)

### 1. Clone repository

git clone https://github.com/SchrimpsMitReis/Videoflix.git
cd Videoflix

---

### 2. Create `.env` file

cp .env.template .env

Adjust at least:

SECRET_KEY=your_secret_key
DEBUG=True

DB_NAME=videoflix
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

---

### 3. Start Docker

docker compose up --build

---

### 4. Run migrations

docker compose exec web python manage.py migrate

---

### 5. Create superuser (optional)

docker compose exec web python manage.py createsuperuser

---

## 🧪 Optional: Local Development (for IDE / Debugging)

python -m venv env
env\\Scripts\\activate  # Windows

pip install -r requirements.txt

---

## API Documentation (drf-spectacular)

This project uses **drf-spectacular** to automatically generate an OpenAPI-compliant schema for the backend API.  
The documentation is derived directly from Django REST Framework views and serializers and is enhanced with explicit annotations for custom logic such as cookie-based authentication and video streaming endpoints.`

```
Swagger UI: /api/docs/  
Schema: /api/schema/
```

---

## 🌐 Access

| Service     | URL                         |
| ----------- | --------------------------- |
| Backend API | http://localhost:8000       |
| MailHog UI  | http://localhost:8025       |
| Admin Panel | http://localhost:8000/admin |

---

## 📧 Emails (Development)

Emails are not actually sent but captured by:

http://localhost:8025

---

## 🎥 Video Upload & Streaming

/api/video/<movie_id>/<resolution>/index.m3u8

Example:
/api/video/1/480p/index.m3u8

---

## ⚠️ Important Notes

- Never commit your .env file
- Disable DEBUG in production

---

## 👨‍💻 Author

Roman Schröder  
https://github.com/SchrimpsMitReis

