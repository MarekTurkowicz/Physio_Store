<template>
  <footer class="footer glass-heavy mt-3xl">
    <div class="container footer-inner py-2xl grid-4">
      <div class="footer-brand anim-fadeInUp">
        <div class="logo mb-md">
          <svg width="28" height="28" viewBox="0 0 36 36" fill="none">
            <rect width="36" height="36" rx="10" fill="#14b8a6" />
            <path d="M18 8C12.48 8 8 12.48 8 18s4.48 10 10 10 10-4.48 10-10S23.52 8 18 8zm-1 14.5v-3.07c-1.73-.44-3-2.01-3-3.93 0-2.21 1.79-4 4-4s4 1.79 4 4c0 1.92-1.27 3.49-3 3.93V22.5c0 .55-.45 1-1 1s-1-.45-1-1zM18 14c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2z" fill="white" />
          </svg>
          <span class="logo-name ml-sm">PhysioStore</span>
        </div>
        <p class="text-xs text-muted brand-copy">
          Najlepszy sprzęt rehabilitacyjny w Polsce.<br />
          Stworzony z pasji do zdrowia.
        </p>
      </div>

      <div class="footer-links anim-fadeInUp anim-delay-1">
        <h4 class="mb-lg">Sklep</h4>
        <nav class="flex flex-col gap-sm">
          <router-link to="/produkty" class="text-xs text-muted transition-all">Wszystkie produkty</router-link>
          <router-link to="/koszyk" class="text-xs text-muted transition-all">Koszyk</router-link>
        </nav>
      </div>

      <div class="footer-links anim-fadeInUp anim-delay-2">
        <h4 class="mb-lg">Pomoc</h4>
        <nav class="flex flex-col gap-sm">
          <router-link to="/kontakt" class="text-xs text-muted transition-all">Kontakt</router-link>
          <a href="#" class="text-xs text-muted transition-all">FAQ</a>
        </nav>
      </div>

      <div class="footer-newsletter anim-fadeInUp anim-delay-3">
        <h4 class="mb-lg">Bądź na bieżąco</h4>
        <div class="newsletter-form glass p-xs flex">
          <input type="email" placeholder="E-mail..." class="newsletter-input text-xs w-full" />
          <button class="btn btn-primary btn-sm">→</button>
        </div>
      </div>
    </div>

    <div class="footer-bottom">
      <div class="container py-md flex justify-between items-center text-xs text-muted">
        <span>&copy; 2026 PhysioStore Pro. Wszelkie prawa zastrzeżone.</span>
        <div class="footer-social flex gap-md">
          <span>IG</span>
          <span>FB</span>
          <span>IN</span>
        </div>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.grid-4 {
  display: grid;
  grid-template-columns: 1.5fr 1fr 1fr 1.5fr;
  gap: 48px;
}

.logo {
  display: flex;
  align-items: center;
}

.logo-name {
  font-weight: 900;
  color: white;
}

.brand-copy {
  line-height: 1.7;
}

.footer {
  border-top: 1px solid var(--border-subtle);
  background: rgba(7, 17, 31, 0.72);
}

.ml-sm {
  margin-left: 8px;
}

.gap-sm {
  gap: 8px;
}

.gap-md {
  gap: 16px;
}

.newsletter-form {
  align-items: center;
  border-radius: 18px;
}

.newsletter-input {
  background: transparent;
  border: 0;
  color: white;
  padding: 12px 14px;
  outline: none;
}

.footer-bottom {
  border-top: 1px solid var(--border-subtle);
}

@media (max-width: 768px) {
  .grid-4 {
    grid-template-columns: 1fr;
    gap: 32px;
  }

  .footer-bottom .container {
    flex-direction: column;
    gap: 12px;
    text-align: center;
  }
}
</style>
