# 🏥 FIZJO STORE - Profesjonalna Platforma E-commerce dla Fizjoterapii

[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)
[![Vue.js](https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D)](https://vuejs.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com)

**FIZJO STORE** to zaawansowana aplikacja webowa typu full-stack, stworzona dla profesjonalnego sklepu z akcesoriami fizjoterapeutycznymi. Projekt łączy nowoczesny backend w FastAPI z responsywnym frontendem Vue 3, oferując wysoką wydajność, bezpieczeństwo i skalowalność dzięki konteneryzacji Docker.

---

## 🏗️ Architektura Rozwiązania

Projekt jest zorganizowany w architekturze mikro-usługowej sterowanej przez Docker Compose:

- **Frontend**: Aplikacja SPA (Single Page Application) zbudowana w Vue 3 (Vite), Pinia i Vanilla CSS.
- **Backend**: Asynchroniczne REST API oparte na FastAPI i SQLAlchemy 2.0.
- **Baza Danych**: PostgreSQL 16 zarządzający produktami, zamówieniami i użytkownikami.

Szczegółowa dokumentacja architektury znajduje się w [ARCHITECTURE.md](./ARCHITECTURE.md).

---

## 🚀 Szybki Start (Docker)

Wymagania: [Docker Desktop](https://www.docker.com/products/docker-desktop/)

1. **Klonowanie i budowanie projektu**:
   ```bash
   docker-compose up -d --build
   ```

2. **Inicjalizacja danych (Seeding)**:
   ```bash
   docker-compose exec backend python seed.py
   ```

3. **Dostęp do aplikacji**:
   - **Frontend**: [http://localhost:3000](http://localhost:3000)
   - **API Backend**: [http://localhost:8001/api](http://localhost:8001/api)
   - **API Docs (Swagger)**: [http://localhost:8001/docs](http://localhost:8001/docs)

---

## 📁 Struktura Projektu

- `/physio_shop` - Kompletny kod źródłowy backendu (FastAPI).
- `/frontend` - Kod źródłowy aplikacji klienckiej (Vue.js).
- `docker-compose.yml` - Orkiestracja całego środowiska.
- `seed.py` - Skrypt zasilający bazę danych realistycznymi danymi.

---

## 🛠️ Rozwój Projektu (Manualny)

Jeśli chcesz pracować lokalnie bez Dockera (wymaga Pythona 3.12+ i Node.js 20+):

### Backend (`/physio_shop`)
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend (`/frontend`)
```bash
npm install
npm run dev
```

---

## 📊 Zarządzanie Bazą Danych
Do zarządzania bazą PostgreSQL w kontenerze zalecamy **DataGrip** lub **DBeaver**.
- **Host**: `localhost`
- **Port**: `5434`
- **User/Pass**: `postgres` / `postgres`
- **DB Name**: `physioshop`

---

## 👨‍💻 Technologie
- **Backend**: Python 3.12, FastAPI, SQLAlchemy (Async), Pydantic, PostgreSQL.
- **Frontend**: JavaScript, Vue 3, Pinia, Vite.
- **DevOps**: Docker, Docker Compose.

---

*Wszelka profesjonalna dokumentacja techniczna znajduje się w dedykowanych folderach `/physio_shop` i `/frontend`.*
