# PhysioStore System Architecture (V2 — Pro Edition)

Niniejszy dokument opisuje architekturę systemu po migracji na profesjonalny stos technologiczny (PrimeVue 4 + Tailwind CSS). Jest to standard "Corporate Grade" zapewniający czysty kod (Clean Code) i łatwą rozbudowę.

## 1. Technologia (Tech Stack)

### Frontend
- **Framework**: Vue 3 (Composition API, `<script setup>`)
- **UI Component Library**: **PrimeVue 4** (V4-Aura Preset)
- **Styling**: **Tailwind CSS v3** (Utility-first approach)
- **Icons**: **PrimeIcons** (System icons)
- **Narzędzia budowania**: Vite 8 + **unplugin-vue-components** (Auto-import komponentów PrimeVue)
- **Stan (State Management)**: Pinia 3
- **Komunikacja**: Natywne `fetch` API z centralnym interceptorem (`src/services/api.js`)

---

## 2. Standardy Dokumentacji i Kodowania

### Zero Custom CSS Policy
W nowej architekturze dążymy do **0 linii ręcznego CSS w blokach `<style>`**.
- Używamy klas **Tailwind CSS** bezpośrednio w template'ach dla układu (Flex, Grid, Spacing).
- Wykorzystujemy gotowe komponenty **PrimeVue** (np. `InputText`, `Button`, `DataTable`) do logiki UI.
- Globalne modyfikacje motywu znajdują się w `assets/main.css` i korzystają z warstw `@tailwind`.

### Auto-Import (Clean Code)
Komponenty PrimeVue (np. `<Button>`, `<Card>`) **nie wymagają ręcznego importu** w skryptach `.vue`. Są one automatycznie wykrywane i rejestrowane przez `unplugin-vue-components` zgodnie z konfiguracją w `vite.config.js`.

---

## 3. Autoryzacja i Zarządzanie Sesją

### Przepływ pracy (Workflow)
- **Interceptor**: Każde żądanie z `api.js` automatycznie wstrzykuje nagłówek `Authorization: Bearer <token>` z `localStorage`.
- **Route Guards**: `router.beforeEach` zabezpiecza trasy i synchronizuje stan ról z `authStore`.

### System Ról
- `admin` -> Panel `/admin` (Czerwona kolorystyka, zarządzanie użytkownikami przez `DataTable`).
- `manager` -> Panel `/manager` (Bursztynowa kolorystyka, zarządzanie sklepem i stanami).
- `customer` -> Panel `/dashboard` (Tealowa kolorystyka, profil i historia).

---

## 4. UI/UX Design System (Physio Pro)

Projekt korzysta z motywu **Sleek Dark**, inspirowanego nowoczesnymi aplikacjami medycznymi:
- **Główne kolory**: 
  - `primary-500` (#0aad92) – Physio Teal.
  - `accent-500` (#f99b07) – Physio Amber.
  - `slate-950` – Głębia tła.
- **Efekty**: Glassmorphism (szronione szkło) realizowane przez `!bg-slate-900/40 !backdrop-blur-xl`.
- **Komponenty**: Zaawansowane komponenty PrimeVue zapewniają wsparcie dla klawiatury, dostępność (A11y) oraz animacje (Transitions).
