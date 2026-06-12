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
```
git clone https://github.com/SchrimpsMitReis/Videoflix.git
cd Videoflix
```
---

### 2. Create `.env` file
```
cp .env.template .env
```

Adjust at least:
```
SECRET_KEY=your_secret_key
DEBUG=True
DB_NAME=videoflix
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```
---

### 3. Configure VS Code for Development

This project runs fully inside Docker. A local Python virtual environment such
as `env`, `venv`, or `.venv` is not required.

For Python autocomplete, linting, testing, and debugging in VS Code:

1. Install the **Dev Containers** extension.
2. Open the project folder in VS Code.
3. Run **Dev Containers: Rebuild and Reopen in Container** from the command palette.

VS Code will then use `/usr/local/bin/python` and the dependencies installed
inside the `web` container. Run Django commands through Docker Compose:

```bash
docker compose exec web python manage.py <command>
```

> `.env` is the project's environment configuration file. It is unrelated to
> the optional Python virtual-environment folders named `env` or `venv`.

---

### 4. Configure Email Backend

Set the your Email Configurations in the .env (e.g. AOL Mail)

```
EMAIL_HOST=smtp.aol.com
EMAIL_PORT=465
EMAIL_HOST_USER=yourAccount@aol.de
EMAIL_HOST_PASSWORD=appPassword123
EMAIL_USE_TLS=False
EMAIL_USE_SSL=True
EMAIL_TIMEOUT=10
DEFAULT_FROM_EMAIL=

```
Many Email Providers can give you an App Password so you dont have to user your real password in here.


---
### 5. Start Docker

Start Docker Desktop

```
docker compose up --build
```

---


### Migrations (optional)

```bash
docker compose exec web python manage.py migrate
```

---
q
### Create Superuser (optional)

```bash
docker compose exec web python manage.py createsuperuser
```



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

## 📧 Emails (Development) -  MailHog

For using Mailhoch recomment in the docker-compose.yml

```
      # - mailhog
    # links:
      # - 'mailhog'

  # mailhog:
  #   image: mailhog/mailhog
  #   container_name: mailhog
  #   ports:
  #     - "1025:1025" #127.0.0.1:1025:1025  
  #     - "8025:8025"

```

Emails are not actually sent but captured by:
```
http://localhost:8025
```

---

## 🎥 Video Upload & Streaming
```
/api/video/<movie_id>/<resolution>/index.m3u8
```
Example:
```
/api/video/1/480p/index.m3u8
```
---

## ⚠️ Important Notes

- Never commit your .env file
- Disable DEBUG in production

---

## 👨‍💻 Author

Roman Schröder  
https://github.com/SchrimpsMitReis
