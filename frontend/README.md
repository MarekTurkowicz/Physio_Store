# 🎨 FIZJO STORE Frontend (Vue 3 + Vite)

Profesjonalna, responsywna i nowoczesna platforma e-commerce stworzona w Vue 3. Sklep dla fizjoterapeutów z naciskiem na user experience (UX) i nowoczesne wzorce projektowe (Glassmorphism, Dark Mode).

---

## 🚀 Technologie

- **Framework**: [Vue 3](https://vuejs.org) (Composition API)
- **State Management**: [Pinia](https://pinia.vuejs.org) (Obsługa koszyka i sesji)
- **Build Tool**: [Vite](https://vitejs.dev)
- **Stylizja**: Vanilla CSS (Modern CSS Custom Properties/Variables)
- **Routing**: Vue Router

---

## 🏗️ Struktura Projektu

- **`src/components/`**: Ponad-używalne komponenty UI (np. ProductCard, Navbar, Cart drawer).
- **`src/views/`**: Główne strony aplikacji (Home, Catalog, Checkout, Login, Contact).
- **`src/stores/`**: Magazyny stanu Pinia (np. store koszyka, obsługa autentykacji).
- **`src/assets/`**: Statyczne zasoby i globalne style CSS.

---

## 🛠️ Uruchomienie i Rozwój

### W Kontenerze (Zalecane)
Aplikacja jest automatycznie serwowana przez Docker Compose.
```bash
docker-compose up -d --build frontend
```
Dostęp: [http://localhost:3000](http://localhost:3000)

### Lokalnie (Manualnie)
1. Zainstaluj pakiety: `npm install`
2. Uruchom serwer deweloperski: `npm run dev`
3. Budowa produkcyjna: `npm run build`

---

## 📡 Konfiguracja Proxy

System korzysta z `vite.config.js` do automatycznego przekierowywania zapytań `/api` do backendu FastAPI. W kontenerze Docker, target ustawiony jest na `http://backend:8080`, co umożliwia integrację bez problemów z polityką CORS.

---

## ✨ Kluczowe Funkcje
- **Dynamiczny koszyk**: Real-time aktualizacja produktów i kwoty całkowitej pod kontrolą Pinia.
- **Wyszukiwarka produktów**: Interaktywna filtracja katalogu.
- **Premium UI**: Płynne animacje i stylowy ciemny motyw.

---

*Ten moduł jest częścią projektu FIZJO STORE. Więcej informacji w głównym [README.md](../README.md).*
