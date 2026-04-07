# ⚙️ PhysioShop Backend API (FastAPI)

Profesjonalne, asynchroniczne REST API zasilające platformę **FIZJO STORE**. Zbudowane z naciskiem na wydajność, bezpieczeństwo (JWT) oraz czystą architekturę warstwową.

---

## 🚀 Technologie i Stack Techniczny

- **Framework**: [FastAPI](https://fastapi.tiangolo.com) (Standard ASGI)
- **Baza Danych**: PostgreSQL 16 (wspierana przez `asyncpg`)
- **ORM**: SQLAlchemy 2.0 (Full Async Support)
- **Migracje**: Alembic
- **Walidacja**: Pydantic v2
- **Bezpieczeństwo**: JWT (JSON Web Tokens) z rolami `Admin` / `Customer`
- **Testy**: Pytest (Asyncio Support)

---

## 🏗️ Architektura Kodu

Projekt stosuje wzorzec **Layered Architecture** (Architektura Warstwowa) zapewniający separację odpowiedzialności:

1. **API Layer (`app/api/`)**: Endpointy, kontrolery i obsługa tras (Routing).
2. **Service Layer (`app/services/`)**: Warstwa logiki biznesowej – tu dzieje się magia procesowa.
3. **Repository Layer (`app/repositories/`)**: Abstrakcja dostępu do danych (Pattern Repository).
4. **Model Layer (`app/models/`)**: Definicje tabel bazy danych (SQLAlchemy Models).
5. **Schema Layer (`app/schemas/`)**: Modele danych wejściowych/wyjściowych (Pydantic).
6. **Core Layer (`app/core/`)**: Konfiguracja, zabezpieczenia i narzędzia wspólne.

---

## 🛠️ Instalacja i Uruchomienie

### W Kontenerze (Zalecane)
Backend jest częścią ekosystemu Docker Compose projektu głównego.
```bash
docker-compose up -d --build backend
```

### Lokalnie (Development)
1. Aktywuj środowisko: `venv/Scripts/Activate.ps1`
2. Zainstaluj zależności: `pip install -r requirements.txt`
3. Skonfiguruj `.env` (użyj `.env.example` jako wzoru)
4. Uruchom: `uvicorn app.main:app --reload --port 8080`

---

## 🧪 Zarządzanie Danymi i Migracjami

- **Seeding**: Aby zasilić bazę testowymi danymi fizjoterapeutycznymi:
  ```bash
  python seed.py
  ```
- **Migracje bazy**:
  ```bash
  alembic upgrade head
  ```

---

## 📖 Interaktywna Dokumentacja

Po uruchomieniu serwera, pełna dokumentacja techniczna (OpenAPI) dostępna jest pod adresami:
- **Swagger UI**: [http://localhost:8080/docs](http://localhost:8080/docs)
- **ReDoc**: [http://localhost:8080/redoc](http://localhost:8080/redoc)

---

## 🛡️ Konta Testowe
- **Admin**: `admin@physioshop.pl` / `admin123`
- **Customer**: `jan.kowalski@example.com` / `customer123`

---

*Ten moduł jest częścią projektu FIZJO STORE. Więcej informacji w głównym [README.md](../README.md).*
