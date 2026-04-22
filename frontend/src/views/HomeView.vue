<template>
  <div class="home-page" ref="pageRef">

    <!-- ═══ HERO ═══ -->
    <section class="hero">
      <div class="hero-orb orb-1"></div>
      <div class="hero-orb orb-2"></div>
      <div class="hero-orb orb-3"></div>

      <div class="container hero-inner">
        <div class="hero-content anim-fadeInUp">
          <Tag :value="$t('home.tag')" severity="success" rounded class="hero-tag" />

          <h1 class="hero-title text-gradient">
            {{ $t('home.title') }}<br />
            <div class="hero-typed-wrapper">
              <span class="text-primary-gradient">{{ typedText }}<span class="typing-cursor"></span></span>
            </div>
          </h1>

          <p class="hero-subtitle">{{ $t('home.subtitle') }}</p>

          <div class="hero-actions">
            <router-link to="/produkty">
              <Button :label="$t('home.cta')" icon="pi pi-shopping-bag" size="large" />
            </router-link>
            <router-link to="/kontakt">
              <Button :label="$t('home.ctaSecondary')" icon="pi pi-phone" severity="secondary" size="large" outlined />
            </router-link>
          </div>

          <div class="hero-stats anim-fadeInUp anim-delay-3">
            <div class="stat-card glass">
              <span class="stat-val">{{ $t('home.stat1val') }}</span>
              <span class="stat-lbl">{{ $t('home.stat1lbl') }}</span>
            </div>
            <div class="stat-card glass">
              <span class="stat-val">{{ $t('home.stat2val') }}</span>
              <span class="stat-lbl">{{ $t('home.stat2lbl') }}</span>
            </div>
          </div>
        </div>

        <div class="hero-visual anim-fadeInUp anim-delay-2">
          <div class="hero-card glass-heavy anim-float anim-glow">
            <div class="card-inner-blur"></div>
            <Tag :value="$t('home.bestseller')" severity="warn" class="bestseller-tag" />
            <div class="product-visual skeleton"></div>
            <div class="hero-card-info">
              <h3>{{ $t('home.heroCardTitle') }}</h3>
              <p class="hero-card-desc">{{ $t('home.heroCardDesc') }}</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <hr class="section-divider" />

    <!-- ═══ ANIMATED COUNTERS ═══ -->
    <section class="container counters-section" ref="countersRef">
      <div class="counters-grid">
        <div
          v-for="(stat, i) in counterStats"
          :key="i"
          class="counter-item"
          data-reveal
          :data-reveal-delay="i * 90"
        >
          <span class="counter-val text-primary-gradient">{{ stat.display }}</span>
          <span class="counter-label">{{ stat.label }}</span>
        </div>
      </div>
    </section>

    <hr class="section-divider" />

    <!-- ═══ FEATURES — BENTO GRID ═══ -->
    <section class="container features-section">
      <div class="features-header" data-reveal>
        <h2 class="text-gradient">{{ $t('home.whyTitle') }}</h2>
        <p class="features-sub">{{ $t('home.whySub') }}</p>
      </div>

      <div class="bento-grid">
        <div class="bento-card bento-large glass-heavy" data-reveal="left">
          <div class="bento-glow teal-glow"></div>
          <div class="bento-icon">🛡️</div>
          <h3 class="bento-title">{{ features[0].title }}</h3>
          <p class="bento-desc">{{ features[0].desc }}</p>
        </div>
        <div class="bento-card glass-heavy" data-reveal data-reveal-delay="150">
          <div class="bento-glow amber-glow"></div>
          <div class="bento-icon">🚚</div>
          <h3 class="bento-title">{{ features[1].title }}</h3>
          <p class="bento-desc">{{ features[1].desc }}</p>
        </div>
        <div class="bento-card glass-heavy" data-reveal data-reveal-delay="260">
          <div class="bento-glow teal-glow"></div>
          <div class="bento-icon">💎</div>
          <h3 class="bento-title">{{ features[2].title }}</h3>
          <p class="bento-desc">{{ features[2].desc }}</p>
        </div>
      </div>
    </section>

    <hr class="section-divider" />

    <!-- ═══ FEATURED PRODUCTS ═══ -->
    <section class="container featured-section">
      <div class="features-header" data-reveal>
        <h2 class="text-gradient">{{ $t('home.featuredTitle') }}</h2>
        <p class="features-sub">{{ $t('home.featuredSub') }}</p>
      </div>

      <div class="featured-grid">
        <div
          v-for="(p, i) in featuredProducts"
          :key="i"
          class="featured-card glass-heavy"
          data-reveal
          :data-reveal-delay="i * 80"
        >
          <div class="featured-media">
            <div class="featured-img skeleton"></div>
            <Tag :value="p.badge" :severity="p.badgeSeverity" class="featured-badge" />
          </div>
          <div class="featured-body">
            <h4 class="featured-name">{{ p.name }}</h4>
            <p class="featured-desc">{{ p.desc }}</p>
            <div class="featured-footer">
              <span class="featured-price">{{ p.price }} PLN</span>
              <router-link to="/produkty">
                <Button :label="$t('home.buyBtn')" icon="pi pi-arrow-right" size="small" severity="primary" />
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </section>

    <hr class="section-divider" />

    <!-- ═══ TESTIMONIALS ═══ -->
    <section class="container testimonials-section">
      <div class="features-header" data-reveal>
        <h2 class="text-gradient">{{ $t('home.testimonialsTitle') }}</h2>
        <p class="features-sub">{{ $t('home.testimonialsSub') }}</p>
      </div>

      <div class="testimonials-grid">
        <div
          v-for="(t, i) in testimonials"
          :key="i"
          class="testimonial-card glass-heavy"
          data-reveal
          :data-reveal-delay="i * 110"
        >
          <div class="testimonial-stars">
            <i v-for="s in 5" :key="s" class="pi pi-star-fill"></i>
          </div>
          <p class="testimonial-text">"{{ t.text }}"</p>
          <div class="testimonial-author">
            <div class="testimonial-avatar">{{ t.initials }}</div>
            <div>
              <div class="testimonial-name">{{ t.name }}</div>
              <div class="testimonial-role">{{ t.role }}</div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <hr class="section-divider" />

    <!-- ═══ NEWSLETTER CTA ═══ -->
    <section class="container cta-section">
      <div class="cta-inner glass-heavy" data-reveal="scale">
        <div class="cta-orb"></div>
        <h2 class="text-gradient cta-title">{{ $t('home.ctaTitle') }}</h2>
        <p class="features-sub">{{ $t('home.ctaSub') }}</p>
        <div class="newsletter-row">
          <input
            v-model="email"
            type="email"
            :placeholder="$t('home.ctaPlaceholder')"
            class="newsletter-field"
          />
          <Button
            :label="$t('home.ctaBtn')"
            icon="pi pi-send"
            severity="primary"
            :disabled="!email"
            @click="subscribe"
          />
        </div>
      </div>
    </section>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useScrollReveal } from '../composables/useScrollReveal'
import Button from 'primevue/button'
import Tag from 'primevue/tag'

const { t } = useI18n()
const pageRef = ref(null)
const countersRef = ref(null)
useScrollReveal(pageRef)

// ─── Typing effect ───────────────────────────────────────────────
const typingWords = computed(() => [
  t('home.typedWord1'),
  t('home.typedWord2'),
  t('home.typedWord3'),
])
const typedText = ref('')
let wordIdx = 0
let typingTimer = null

const runTyping = () => {
  const word = typingWords.value[wordIdx % typingWords.value.length]
  let ci = 0

  const type = () => {
    typedText.value = word.slice(0, ++ci)
    typingTimer = ci < word.length
      ? setTimeout(type, 80)
      : setTimeout(erase, 2500)
  }
  const erase = () => {
    if (typedText.value.length > 0) {
      typedText.value = typedText.value.slice(0, -1)
      typingTimer = setTimeout(erase, 35)
    } else {
      wordIdx++
      typingTimer = setTimeout(runTyping, 400)
    }
  }
  type()
}

// ─── Animated counters ───────────────────────────────────────────
const cv = ref([0, 0, 0, 0])
let countersStarted = false

const counterStats = computed(() => [
  { display: cv.value[0] + 'k+', label: t('home.counter1lbl') },
  { display: cv.value[1] + '+',  label: t('home.counter2lbl') },
  { display: (cv.value[2] / 10).toFixed(1) + '/5', label: t('home.counter3lbl') },
  { display: cv.value[3] + 'h', label: t('home.counter4lbl') },
])

const animateCounter = (idx, target, duration) => {
  const start = Date.now()
  const tick = () => {
    const p = Math.min((Date.now() - start) / duration, 1)
    cv.value[idx] = Math.round((1 - (1 - p) ** 3) * target)
    if (p < 1) requestAnimationFrame(tick)
  }
  requestAnimationFrame(tick)
}

const startCounters = () => {
  if (countersStarted) return
  countersStarted = true
  animateCounter(0, 12, 900)
  setTimeout(() => animateCounter(1, 580, 900), 80)
  setTimeout(() => animateCounter(2, 49, 900), 160)
  setTimeout(() => animateCounter(3, 24, 700), 240)
}

// ─── Features ────────────────────────────────────────────────────
const features = computed(() => [
  { icon: '🛡️', title: t('home.feat1title'), desc: t('home.feat1desc') },
  { icon: '🚚', title: t('home.feat2title'), desc: t('home.feat2desc') },
  { icon: '💎', title: t('home.feat3title'), desc: t('home.feat3desc') },
])

// ─── Featured products (placeholder) ─────────────────────────────
const featuredProducts = computed(() => [
  { name: t('home.prod1name'), desc: t('home.prod1desc'), price: '149', badge: t('home.prod1badge'), badgeSeverity: 'warn' },
  { name: t('home.prod2name'), desc: t('home.prod2desc'), price: '89',  badge: t('home.prod2badge'), badgeSeverity: 'success' },
  { name: t('home.prod3name'), desc: t('home.prod3desc'), price: '119', badge: t('home.prod3badge'), badgeSeverity: 'danger' },
  { name: t('home.prod4name'), desc: t('home.prod4desc'), price: '59',  badge: t('home.prod4badge'), badgeSeverity: 'info' },
])

// ─── Testimonials ─────────────────────────────────────────────────
const testimonials = computed(() => [
  { text: t('home.t1text'), name: 'Anna K.',  role: t('home.t1role'), initials: 'AK' },
  { text: t('home.t2text'), name: 'Marek W.', role: t('home.t2role'), initials: 'MW' },
  { text: t('home.t3text'), name: 'Piotr R.', role: t('home.t3role'), initials: 'PR' },
])

// ─── Newsletter ───────────────────────────────────────────────────
const email = ref('')
const subscribe = () => { email.value = '' }

// ─── Lifecycle ───────────────────────────────────────────────────
onMounted(() => {
  runTyping()

  const obs = new IntersectionObserver(
    (entries) => { if (entries[0].isIntersecting) { startCounters(); obs.disconnect() } },
    { threshold: 0.25 }
  )
  if (countersRef.value) obs.observe(countersRef.value)
})

onUnmounted(() => { clearTimeout(typingTimer) })
</script>

<style scoped>
/* ── Hero ── */
.hero {
  position: relative;
  min-height: 100vh;
  display: flex;
  align-items: center;
  overflow: hidden;
}

.hero-inner {
  display: grid;
  grid-template-columns: 1.15fr 0.85fr;
  gap: 64px;
  align-items: center;
  padding: calc(var(--header-height) + var(--banner-height, 0px) + 24px) 0 80px;
}

.hero-tag { margin-bottom: 20px; }

.hero-title {
  font-size: clamp(3rem, 7.5vw, 5.6rem);
  font-weight: 900;
  line-height: 1.05;
  letter-spacing: -0.04em;
  margin: 0;
}

.hero-typed-wrapper {
  height: 2.2em;
  overflow: hidden;
  display: block;
}

.hero-subtitle {
  max-width: 600px;
  margin-top: 24px;
  font-size: 1.08rem;
  color: #bfd0e4;
  line-height: 1.7;
}

.hero-actions {
  display: flex;
  gap: 16px;
  margin-top: 32px;
}

.hero-orb {
  position: absolute;
  border-radius: 999px;
  filter: blur(50px);
  pointer-events: none;
}
.orb-1 { width: 500px; height: 500px; top: -60px; right: -140px; background: radial-gradient(circle, rgba(20,184,166,.15), transparent 70%); }
.orb-2 { width: 380px; height: 380px; bottom: 60px; left: -120px; background: radial-gradient(circle, rgba(245,158,11,.13), transparent 70%); }
.orb-3 { width: 280px; height: 280px; top: 50%; left: 40%; background: radial-gradient(circle, rgba(20,184,166,.07), transparent 70%); }

.hero-stats { display: flex; gap: 18px; margin-top: 48px; }

.stat-card { min-width: 156px; padding: 16px; border-radius: 22px; text-align: center; }
.stat-val { display: block; font-size: 1.6rem; font-weight: 900; color: #5eead4; }
.stat-lbl { color: #8aa0b8; font-size: 0.72rem; letter-spacing: .08em; text-transform: uppercase; }

.hero-card {
  position: relative;
  overflow: hidden;
  min-height: 400px;
  border-radius: 34px;
  padding: 32px;
}

.card-inner-blur {
  position: absolute;
  inset: auto -50px -90px auto;
  width: 220px; height: 220px;
  border-radius: 999px;
  background: radial-gradient(circle, rgba(245,158,11,.22), transparent 70%);
  filter: blur(22px);
  pointer-events: none;
}
.bestseller-tag { position: absolute; top: 24px; right: 24px; z-index: 2; }
.product-visual { height: 200px; border-radius: 24px; margin-top: 48px; }
.hero-card-info { margin-top: 24px; }
.hero-card-info h3 { font-weight: 800; font-size: 1.2rem; color: white; margin: 0; }
.hero-card-desc { color: #8aa0b8; font-size: .875rem; margin-top: 8px; }

/* ── Counters ── */
.counters-section { padding: 72px 0; }

.counters-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  text-align: center;
}

.counter-item {
  padding: 32px 16px;
  border-radius: 24px;
  background: rgba(14, 27, 44, 0.55);
  border: 1px solid var(--border-subtle);
  transition: transform 0.3s ease;
}
.counter-item:hover { transform: translateY(-4px); }

.counter-val {
  display: block;
  font-size: clamp(2.2rem, 4vw, 3rem);
  font-weight: 900;
  line-height: 1;
}

.counter-label {
  display: block;
  color: var(--color-text-muted);
  font-size: 0.8rem;
  margin-top: 10px;
  text-transform: uppercase;
  letter-spacing: 0.06em;
}

/* ── Features — Bento Grid ── */
.features-section { padding: 80px 0; }

.features-header { text-align: center; margin-bottom: 48px; }
.features-header h2 { font-weight: 900; font-size: clamp(1.8rem, 4vw, 2.6rem); letter-spacing: -0.04em; margin: 0; }
.features-sub { color: #bfd0e4; margin-top: 8px; }

.bento-grid {
  display: grid;
  grid-template-columns: 1.45fr 1fr;
  grid-template-rows: auto auto;
  gap: 20px;
}

.bento-large { grid-row: 1 / 3; }

.bento-card {
  position: relative;
  overflow: hidden;
  border-radius: 28px;
  padding: 36px 32px;
  transition: transform 0.35s var(--transition-spring);
}
.bento-card:hover { transform: translateY(-6px); }

.bento-glow {
  position: absolute;
  inset: auto -60px -80px auto;
  width: 240px; height: 240px;
  border-radius: 999px;
  pointer-events: none;
  filter: blur(50px);
}
.teal-glow  { background: radial-gradient(circle, rgba(20,184,166,.2), transparent 70%); }
.amber-glow { background: radial-gradient(circle, rgba(245,158,11,.18), transparent 70%); }

.bento-icon {
  display: inline-grid;
  place-items: center;
  width: 56px; height: 56px;
  border-radius: 18px;
  background: rgba(20, 184, 166, 0.1);
  font-size: 1.5rem;
  margin-bottom: 20px;
}
.bento-title { font-weight: 800; font-size: 1.2rem; color: white; margin: 0 0 10px; }
.bento-desc  { color: #8aa0b8; font-size: .9rem; line-height: 1.6; margin: 0; }

/* ── Featured Products ── */
.featured-section { padding: 80px 0; }

.featured-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 18px;
}

.featured-card {
  border-radius: 22px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  transition: transform 0.35s var(--transition-spring), box-shadow 0.35s ease;
}
.featured-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 24px 50px -16px rgba(0,0,0,.5), 0 0 0 1px rgba(20,184,166,.18);
}

.featured-media { position: relative; aspect-ratio: 4/3; overflow: hidden; }
.featured-img {
  width: 100%; height: 100%;
  transition: transform 0.5s var(--transition-spring);
}
.featured-card:hover .featured-img { transform: scale(1.07); }
.featured-badge { position: absolute; top: 12px; right: 12px; }

.featured-body { padding: 18px; display: flex; flex-direction: column; gap: 6px; flex: 1; }
.featured-name { font-weight: 800; font-size: .95rem; color: white; margin: 0; }
.featured-desc { font-size: .8rem; color: var(--color-text-muted); margin: 0; flex: 1; }

.featured-footer { display: flex; justify-content: space-between; align-items: center; margin-top: 12px; }
.featured-price { font-weight: 900; font-size: 1.1rem; color: white; }

/* ── Testimonials ── */
.testimonials-section { padding: 80px 0; }

.testimonials-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-top: 48px;
}

.testimonial-card {
  border-radius: 24px;
  padding: 32px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  transition: transform 0.35s var(--transition-spring);
}
.testimonial-card:hover { transform: translateY(-5px); }

.testimonial-stars { display: flex; gap: 4px; }
.testimonial-stars .pi { font-size: 0.85rem; color: #fbbf24; }

.testimonial-text {
  font-size: 0.9rem;
  color: #bfd0e4;
  line-height: 1.7;
  margin: 0;
  flex: 1;
}

.testimonial-author { display: flex; align-items: center; gap: 12px; margin-top: 4px; }

.testimonial-avatar {
  width: 40px; height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--color-teal-500), var(--color-amber-400));
  display: grid;
  place-items: center;
  font-weight: 800;
  font-size: 0.8rem;
  color: white;
  flex-shrink: 0;
}

.testimonial-name { font-weight: 700; font-size: 0.875rem; color: white; }
.testimonial-role { font-size: 0.75rem; color: var(--color-text-muted); }

/* ── Newsletter CTA ── */
.cta-section { padding: 80px 0 100px; }

.cta-inner {
  border-radius: 36px;
  padding: 72px 48px;
  text-align: center;
  position: relative;
  overflow: hidden;
}

.cta-orb {
  position: absolute;
  width: 500px; height: 500px;
  top: -160px; right: -160px;
  border-radius: 999px;
  background: radial-gradient(circle, rgba(20,184,166,.12), transparent 65%);
  pointer-events: none;
}

.cta-title { font-size: clamp(1.8rem, 4vw, 2.8rem); font-weight: 900; letter-spacing: -0.04em; margin: 0 0 12px; }

.newsletter-row {
  display: flex;
  justify-content: center;
  gap: 12px;
  margin-top: 32px;
  max-width: 540px;
  margin-left: auto;
  margin-right: auto;
}

.newsletter-field {
  flex: 1;
  padding: 14px 18px;
  border-radius: 16px;
  border: 1px solid var(--border-subtle);
  background: rgba(255,255,255,.04);
  color: white;
  font-size: 0.9rem;
  font-family: inherit;
  outline: none;
  transition: border-color 0.2s;
}
.newsletter-field:focus { border-color: var(--color-teal-500); }
.newsletter-field::placeholder { color: var(--color-text-muted); }

/* ── Responsive ── */
@media (max-width: 1024px) {
  .hero-inner { grid-template-columns: 1fr; text-align: center; gap: 48px; padding-top: calc(var(--header-height) + 16px); }
  .hero-actions, .hero-stats { justify-content: center; }
  .hero-visual { display: flex; justify-content: center; }
  .counters-grid { grid-template-columns: repeat(2, 1fr); }
  .bento-grid { grid-template-columns: 1fr; }
  .bento-large { grid-row: auto; }
  .featured-grid { grid-template-columns: repeat(2, 1fr); }
  .testimonials-grid { grid-template-columns: 1fr; }
}

@media (max-width: 640px) {
  .featured-grid { grid-template-columns: 1fr; }
  .testimonials-grid { grid-template-columns: 1fr; }
  .counters-grid { grid-template-columns: repeat(2, 1fr); }
  .cta-inner { padding: 48px 24px; }
  .newsletter-row { flex-direction: column; }
}
</style>
