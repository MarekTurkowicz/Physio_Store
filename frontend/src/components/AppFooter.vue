<template>
  <footer class="footer">
    <div class="footer-gradient-top"></div>

    <div class="container footer-inner">

      <!-- Brand -->
      <div class="footer-brand" data-reveal="left">
        <div class="footer-logo">
          <svg width="30" height="30" viewBox="0 0 36 36" fill="none">
            <rect width="36" height="36" rx="10" fill="#14b8a6" />
            <path d="M18 8C12.48 8 8 12.48 8 18s4.48 10 10 10 10-4.48 10-10S23.52 8 18 8zm-1 14.5v-3.07c-1.73-.44-3-2.01-3-3.93 0-2.21 1.79-4 4-4s4 1.79 4 4c0 1.92-1.27 3.49-3 3.93V22.5c0 .55-.45 1-1 1s-1-.45-1-1zM18 14c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2z" fill="white" />
          </svg>
          <span class="footer-logo-name">PhysioStore</span>
        </div>
        <p class="footer-copy">{{ $t('footer.copy') }}</p>
        <div class="social-links">
          <a href="#" class="social-btn" aria-label="Instagram">
            <i class="pi pi-instagram"></i>
          </a>
          <a href="#" class="social-btn" aria-label="Facebook">
            <i class="pi pi-facebook"></i>
          </a>
          <a href="#" class="social-btn" aria-label="LinkedIn">
            <i class="pi pi-linkedin"></i>
          </a>
        </div>
      </div>

      <!-- Sklep -->
      <div class="footer-col" data-reveal data-reveal-delay="100">
        <h4 class="footer-heading">{{ $t('footer.shopHeading') }}</h4>
        <nav class="footer-nav">
          <router-link to="/produkty" class="footer-link">{{ $t('footer.allProducts') }}</router-link>
          <router-link to="/koszyk" class="footer-link">{{ $t('footer.cart') }}</router-link>
          <a href="#" class="footer-link">{{ $t('footer.newArrivals') }}</a>
          <a href="#" class="footer-link">{{ $t('footer.promotions') }}</a>
        </nav>
      </div>

      <!-- Pomoc -->
      <div class="footer-col" data-reveal data-reveal-delay="200">
        <h4 class="footer-heading">{{ $t('footer.helpHeading') }}</h4>
        <nav class="footer-nav">
          <router-link to="/kontakt" class="footer-link">{{ $t('footer.contact') }}</router-link>
          <a href="#" class="footer-link">{{ $t('footer.faq') }}</a>
          <a href="#" class="footer-link">{{ $t('footer.returns') }}</a>
          <a href="#" class="footer-link">{{ $t('footer.delivery') }}</a>
        </nav>
      </div>

      <!-- Newsletter -->
      <div class="footer-col footer-newsletter" data-reveal data-reveal-delay="300">
        <h4 class="footer-heading">{{ $t('footer.newsletterTitle') }}</h4>
        <p class="footer-newsletter-desc">{{ $t('footer.newsletterDesc') }}</p>
        <div class="footer-newsletter-form glass">
          <input type="email" :placeholder="$t('footer.newsletterPlaceholder')" class="footer-newsletter-input" />
          <button class="footer-newsletter-btn">
            <i class="pi pi-send"></i>
          </button>
        </div>
      </div>
    </div>

    <!-- Bottom bar -->
    <div class="footer-bottom">
      <div class="container footer-bottom-inner">
        <span class="footer-copyright">{{ $t('footer.copyright') }}</span>
        <div class="footer-bottom-links">
          <a href="#" class="footer-bottom-link">{{ $t('footer.privacy') }}</a>
          <a href="#" class="footer-bottom-link">{{ $t('footer.terms') }}</a>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { useI18n } from 'vue-i18n'
const { t } = useI18n()
</script>

<style scoped>
.footer {
  position: relative;
  background: rgba(5, 12, 24, 0.85);
  border-top: 1px solid var(--border-subtle);
  overflow: hidden;
}

/* subtle gradient accent at the top edge */
.footer-gradient-top {
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent 0%, rgba(20,184,166,.5) 40%, rgba(245,158,11,.3) 70%, transparent 100%);
}

.footer-inner {
  display: grid;
  grid-template-columns: 1.6fr 1fr 1fr 1.5fr;
  gap: 48px;
  padding: 72px 0 56px;
}

/* ── Brand ── */
.footer-brand { display: flex; flex-direction: column; gap: 16px; }

.footer-logo { display: flex; align-items: center; gap: 10px; }
.footer-logo-name { font-size: 1.2rem; font-weight: 900; color: white; }

.footer-copy { font-size: 0.83rem; color: var(--color-text-muted); line-height: 1.7; margin: 0; }

.social-links { display: flex; gap: 10px; }

.social-btn {
  display: inline-grid;
  place-items: center;
  width: 38px; height: 38px;
  border-radius: 12px;
  border: 1px solid var(--border-subtle);
  color: var(--color-text-muted);
  font-size: 1rem;
  transition: background 0.25s, color 0.25s, border-color 0.25s, transform 0.25s var(--transition-spring);
}
.social-btn:hover {
  background: rgba(20,184,166,.12);
  border-color: rgba(20,184,166,.35);
  color: var(--color-teal-400);
  transform: translateY(-3px);
}

/* ── Columns ── */
.footer-col { display: flex; flex-direction: column; gap: 12px; }

.footer-heading {
  font-size: 0.8rem;
  font-weight: 700;
  color: white;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin: 0;
}

.footer-nav { display: flex; flex-direction: column; gap: 8px; }

.footer-link {
  font-size: 0.85rem;
  color: var(--color-text-muted);
  transition: color 0.2s, transform 0.2s;
  display: inline-block;
}
.footer-link:hover { color: white; transform: translateX(4px); }

/* ── Newsletter ── */
.footer-newsletter { gap: 14px; }
.footer-newsletter-desc { font-size: 0.83rem; color: var(--color-text-muted); margin: 0; }

.footer-newsletter-form {
  display: flex;
  align-items: center;
  border-radius: 16px;
  overflow: hidden;
  padding: 4px 4px 4px 14px;
}

.footer-newsletter-input {
  flex: 1;
  background: transparent;
  border: none;
  outline: none;
  color: white;
  font-size: 0.83rem;
  font-family: inherit;
}
.footer-newsletter-input::placeholder { color: var(--color-text-muted); }

.footer-newsletter-btn {
  display: grid;
  place-items: center;
  width: 36px; height: 36px;
  border-radius: 12px;
  border: none;
  background: var(--color-teal-600);
  color: white;
  cursor: pointer;
  transition: background 0.2s, transform 0.2s;
}
.footer-newsletter-btn:hover { background: var(--color-teal-500); transform: scale(1.08); }

/* ── Bottom bar ── */
.footer-bottom {
  border-top: 1px solid var(--border-subtle);
}

.footer-bottom-inner {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 0;
}

.footer-copyright { font-size: 0.78rem; color: var(--color-text-muted); }

.footer-bottom-links { display: flex; gap: 20px; }
.footer-bottom-link { font-size: 0.78rem; color: var(--color-text-muted); transition: color 0.2s; }
.footer-bottom-link:hover { color: white; }

/* ── Responsive ── */
@media (max-width: 900px) {
  .footer-inner { grid-template-columns: 1fr 1fr; gap: 36px; }
}

@media (max-width: 576px) {
  .footer-inner { grid-template-columns: 1fr; gap: 32px; padding: 48px 0 40px; }
  .footer-bottom-inner { flex-direction: column; gap: 12px; text-align: center; }
  .footer-bottom-links { justify-content: center; }
}
</style>
