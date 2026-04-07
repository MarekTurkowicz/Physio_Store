# PhysioStore — Dokumentacja projektu

## Stack technologiczny

### Frontend
| Technologia | Wersja | Rola |
|---|---|---|
| Vue 3 | 3.5.30 | Framework UI (Composition API) |
| Vite | 8.0.1 | Build tool / dev server |
| Pinia | 3.0.4 | State management |
| Vue Router | 4.6.4 | Routing po stronie klienta |
| PrimeVue | 4.5.4 | Biblioteka komponentów UI |
| PrimeIcons | 7.0.0 | Ikony |
| Vue i18n | 11.3.0 | Wielojęzyczność |
| @vueuse/core | 14.2.1 | Composable utilities |

### Backend
| Technologia | Wersja | Rola |
|---|---|---|
| FastAPI | 0.115+ | Framework API (async) |
| Uvicorn | 0.30+ | ASGI server |
| SQLAlchemy[asyncio] | 2.0.30+ | ORM (async) |
| asyncpg | 0.29+ | Driver PostgreSQL (async) |
| Alembic | 1.13+ | Migracje bazy danych |
| Pydantic v2 | 2.x | Walidacja danych |
| python-jose | 3.3+ | JWT tokeny |
| passlib[bcrypt] | 1.7.4+ | Hashowanie haseł |
| redis[hiredis] | 5.0+ | Cache client |
| pytest + httpx | 8.0+ | Testy |

### Infrastruktura
| Usługa | Obraz | Port |
|---|---|---|
| PostgreSQL | postgres:16-alpine | 5434 |
| Redis | redis:7-alpine | 6379 |
| Backend | custom Dockerfile | 8001 |
| Frontend | node:20-alpine | 3000 |

---

## Funkcjonalności

### Strony / Widoki (Frontend)

**`/` — Strona główna**
- Hero section z tagline, tytułem i dwoma przyciskami CTA
- Statystyki (12k+ klientów, 24h dostawa)
- Sekcja "Dlaczego PhysioStore?" z 3 kartami cech

**`/produkty` — Katalog produktów**
- Sidebar z polem wyszukiwania i listą kategorii
- Siatka produktów z paginacją (10/20/30/50 na stronie)
- Stany ładowania (skeleton cards)
- Stan pustego wyniku z resetem filtrów

**`/produkt/:id` — Szczegóły produktu**
- Galeria zdjęć z placeholderem, tag jakości
- Ocena gwiazdkowa (Rating), kategoria, cena z VAT-notą
- Wybór ilości (InputNumber) i przycisk "Dodaj do koszyka"
- Info o darmowej dostawie
- Breadcrumb nawigacja

**`/koszyk` — Koszyk**
- Lista pozycji z edycją ilości i usuwaniem
- Sidebar z podsumowaniem (suma, dostawa, razem)
- Przycisk przejścia do kasy
- Stan pustego koszyka z linkiem do sklepu

**`/zamowienie` — Zamówienie (checkout)**
- 3-krokowy wizard (Stepper):
  1. **Wysyłka** — formularz z imieniem, telefonem, adresem, kodem, miastem
  2. **Płatność** — wybór metody (BLIK, karta, przelew)
  3. **Gotowe** — potwierdzenie z powrotem do sklepu
- Sidebar z podsumowaniem zamówienia (znika po kroku 3)

**`/kontakt` — Kontakt**
- 3 karty kontaktowe (sprzedaż, wsparcie, infolinia)
- Formularz szybkiej wiadomości (FloatLabel, Textarea)
- Placeholder mapy z adresem HQ

**`/logowanie` — Logowanie**
- Formularz email + hasło (z toggle widoczności)
- Wyświetlanie błędów z backendu
- Link do rejestracji

**`/rejestracja` — Rejestracja**
- Formularz imię + email + hasło
- Wyświetlanie błędów
- Link do logowania

**`/dashboard` — Panel klienta**
- Powitanie z awatarem
- Historia zamówień (aktualnie pusta z info)
- Profil (email, rola)
- Przycisk wylogowania

**`/manager` — Panel managera**
- Statystyki sprzedaży (karty)
- Alerty niskiego stanu magazynowego
- Lista nowych zamówień

**`/admin` — Panel admina**
- Tabela użytkowników z rolami i statusami
- Akcje zarządzania (menu kontekstowe)

---

### Backend API (`/api/v1/`)

#### Auth
| Metoda | Endpoint | Opis |
|---|---|---|
| POST | `/auth/register` | Rejestracja (email, password, full_name) |
| POST | `/auth/login` | Logowanie → JWT token |

#### Użytkownicy
| Metoda | Endpoint | Auth | Opis |
|---|---|---|---|
| GET | `/clients/me` | ✓ | Pobierz własny profil |
| GET | `/clients/` | Admin | Lista wszystkich użytkowników (paginacja) |

#### Produkty
| Metoda | Endpoint | Auth | Opis |
|---|---|---|---|
| GET | `/products/` | — | Lista / wyszukiwanie (query, category_id, skip, limit) |
| GET | `/products/{id}` | — | Szczegóły produktu |
| POST | `/products/` | Manager+ | Utwórz produkt |
| PUT | `/products/{id}` | Manager+ | Aktualizuj produkt |
| DELETE | `/products/{id}` | Manager+ | Miękkie usunięcie (is_active=False) |

#### Kategorie
| Metoda | Endpoint | Auth | Opis |
|---|---|---|---|
| GET | `/categories/` | — | Lista wszystkich kategorii |
| POST | `/categories/` | Manager+ | Utwórz kategorię (auto-slug) |

#### Zamówienia
| Metoda | Endpoint | Auth | Opis |
|---|---|---|---|
| POST | `/orders/` | ✓ | Złóż zamówienie (walidacja stanu magazynu) |
| GET | `/orders/` | ✓ | Lista zamówień (klient: własne, manager: wszystkie) |
| GET | `/orders/{id}` | ✓ | Szczegóły zamówienia |
| PATCH | `/orders/{id}/status` | Manager+ | Zmień status (state machine) |
| DELETE | `/orders/{id}` | ✓ | Anuluj zamówienie |

---

### Modele danych

**User** — `id, email, hashed_password, full_name, role (admin/manager/customer), created_at`

**Category** — `id, name, slug, description`

**Product** — `id, name, description, price, stock_quantity, sku, is_active, category_id, timestamps`

**Order** — `id, status, total_amount, shipping_address, user_id, timestamps`
- Statusy: `pending → confirmed → shipped → delivered` / `→ cancelled`

**OrderItem** — `id, quantity, unit_price, order_id, product_id`

---

### Autoryzacja i bezpieczeństwo

- **JWT HS256** — 30-minutowe tokeny, payload: `{ sub: email, role }`
- **Bcrypt** — hashowanie haseł
- **3 role:** `admin`, `manager`, `customer`
- **Guards w routerze Vue** — przekierowania zależne od roli
- **Guards w FastAPI** — `get_current_user()`, `require_manager()`, `require_admin()`
- **Walidacja Pydantic** — wszystkie żądania walidowane schematami
- **SQLAlchemy** — parametryzowane zapytania (ochrona przed SQL injection)

---

### Cache (Redis)

- Produkty (lista/search): klucz `products:q=...:cat=...:s=...:l=...` TTL 300s
- Produkt (szczegóły): klucz `product:{id}` TTL 300s
- Inwalidacja przy create/update/delete produktu
- Graceful degradation — jeśli Redis niedostępny, działa bez cache

---

### Wielojęzyczność (i18n)

Obsługiwane języki: PL (domyślny), EN, DE, ES, FR

- Przełącznik języków w nagłówku (dropdown z flagami)
- Wybór zapisywany w `localStorage`
- Klucze tłumaczeń dla wszystkich widoków: `nav.*`, `home.*`, `products.*`, `cart.*`, `checkout.*`, `contact.*`, `auth.*`, `dashboard.*`

---

### Design System

- **Motyw:** Dark mode wyłącznie (klasa `.dark-mode` na `<html>`)
- **Kolory:** Teal accent `#14b8a6`, tła `#07111f` – `#0f172a`
- **Efekty:** Glass morphism (`.glass`, `.glass-heavy`), gradient tekst (`.text-gradient`)
- **Animacje:** `anim-fadeInUp`, `anim-float`, `anim-glow`, `anim-delay-{1-3}`
- **Responsywność:** CSS Grid + Flexbox, breakpointy 768px / 1024px

---

### Porty i dostęp

| Usługa | URL |
|---|---|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:8001/api/v1 |
| Swagger docs | http://localhost:8001/docs |
| PostgreSQL | localhost:5434 (postgres/postgres/physioshop) |
| Redis | localhost:6379 |
