# 🎬 Videoflix Backend

Ein Netflix-ähnliches Backend auf Basis von **Django REST Framework**, mit Video-Streaming über **HLS (m3u8 + ts Segmente)**, Authentifizierung und Mail-Verifikation.

---

## 🚀 Features

* 🔐 User Registration & Login (JWT / Cookie-based)
* 📧 Account Activation via Email (MailHog im Dev)
* 🎥 Video Upload & Verarbeitung (ffmpeg)
* 📺 HLS Streaming (adaptive vorbereitbar)
* 🖼️ Thumbnail-Handling
* 🐳 Vollständig Docker-basiert
* ⚡ Background Jobs via Redis (django-rq)

---

## 🧱 Tech Stack

* Python / Django
* Django REST Framework
* PostgreSQL
* Redis
* Docker & Docker Compose
* ffmpeg
* MailHog (für Development E-Mails)

---

## ⚙️ Installation (Development)

### 1. Repository klonen

```bash
git clone https://github.com/SchrimpsMitReis/Videoflix.git
cd Videoflix
```

---

### 2. `.env` Datei erstellen

Erstelle eine `.env` basierend auf `.env.template`:

```bash
cp .env.template .env
```

Passe mindestens an:

```env
SECRET_KEY=dein_geheimer_key
DEBUG=True

DB_NAME=videoflix
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```

---

### 3. Docker starten

```bash
docker compose up --build
```

---

### 4. Migrationen ausführen

```bash
docker compose exec web python manage.py migrate
```

---

### 5. Superuser erstellen (optional)

```bash
docker compose exec web python manage.py createsuperuser
```

### 🧪 Optional: Lokales Development (für Editor / Debugging)

## Optional: Lokales Development Setup

Für bessere IDE-Unterstützung (z. B. VS Code Autocomplete):

```md
python -m venv env
env\Scripts\activate  # Windows

pip install -r requirements.txt
```

---

## API Documentation (drf-spectacular)

This project uses **drf-spectacular** to automatically generate an OpenAPI-compliant schema for the backend API.  
The documentation is derived directly from Django REST Framework views and serializers and is enhanced with explicit annotations for custom logic such as cookie-based authentication and video streaming endpoints.

### Swagger UI

An interactive API documentation is available at:

```
/api/docs/
```


### OpenAPI Schema

The raw OpenAPI schema can be accessed at:

```
/api/schema/
```


### Notes

- The documentation is generated directly from the codebase (views, serializers, and annotations)
- Custom behaviors (e.g. cookie-based JWT authentication and HLS streaming) are explicitly documented
- The schema can be used for client generation, API validation, or integration with external tools

---

## 🌐 Zugriff

| Service     | URL                         |
| ----------- | --------------------------- |
| Backend API | http://localhost:8000       |
| MailHog UI  | http://localhost:8025       |
| Admin Panel | http://localhost:8000/admin |

---

## 📧 E-Mails (Development)

E-Mails werden nicht wirklich versendet, sondern landen in:

👉 http://localhost:8025

Dort kannst du:

* Aktivierungslinks kopieren
* Passwort-Reset testen

---

## 🎥 Video Upload & Streaming

### Upload

Videos werden über die API hochgeladen und anschließend verarbeitet.

### HLS Streaming

Die Videos werden automatisch in HLS konvertiert:

```text
/api/video/<movie_id>/<resolution>/index.m3u8
```

Beispiel:

```text
/api/video/1/480p/index.m3u8
```

---

## 🖼️ Media Files

Media-Dateien werden über Django ausgeliefert:

```text
/media/...
```

Beispiel:

```text
http://localhost:8000/media/thumbnails/...
```

---

## ⚠️ Wichtige Hinweise

### CORS

Für Frontend-Integration:

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5500",
    "http://127.0.0.1:5500",
]
```

---

### Mail (Production)

MailHog ist nur für Development gedacht.

Für Produktion solltest du einen SMTP-Anbieter verwenden:

* Brevo
* Mailgun
* SendGrid

---

### Sicherheit

* `.env` niemals committen!
* `SECRET_KEY` geheim halten
* DEBUG in Produktion deaktivieren

---

## 🧪 Development Tipps

### Datenbank zurücksetzen

```bash
docker compose down -v
docker compose up --build
```

---

### Logs anzeigen

```bash
docker compose logs -f
```

---

### In Container gehen

```bash
docker compose exec web sh
```

---

## 📦 ToDo / Ideen

* Adaptive Bitrate Streaming
* CDN Integration
* Upload Queue Optimierung
* Frontend Integration

---

## 👨‍💻 Autor

Roman Schröder
GitHub: https://github.com/SchrimpsMitReis

---

## 🧠 Fun Fact

Dieses Projekt ist Teil einer Backend-Lernreise mit Fokus auf:

* skalierbare APIs
* Videoverarbeitung
* reale Produktionsprobleme 😄

---
