<template>
  <div class="home-page">
    <!-- Hero Section -->
    <section class="hero">
      <div class="hero-orb orb-1"></div>
      <div class="hero-orb orb-2"></div>

      <div class="container hero-inner">
        <div class="hero-content anim-fadeInUp">
          <Tag :value="$t('home.tag')" severity="success" rounded class="hero-tag" />

          <h1 class="hero-title text-gradient">
            {{ $t('home.title') }}
            <br />
            <span class="text-primary-gradient">{{ $t('home.titleAccent') }}</span>
          </h1>

          <p class="hero-subtitle">
            {{ $t('home.subtitle') }}
          </p>

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

    <!-- Features Section -->
    <section class="container features-section anim-fadeInUp">
      <div class="features-header">
        <h2 class="text-gradient">{{ $t('home.whyTitle') }}</h2>
        <p class="features-sub">{{ $t('home.whySub') }}</p>
      </div>
      <div class="feature-grid">
        <Card v-for="feature in features" :key="feature.title" class="feature-card">
          <template #content>
            <div class="f-icon">{{ feature.icon }}</div>
            <h3 class="feature-title">{{ feature.title }}</h3>
            <p class="feature-desc">{{ feature.desc }}</p>
          </template>
        </Card>
      </div>
    </section>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import Button from 'primevue/button'
import Tag from 'primevue/tag'
import Card from 'primevue/card'

const { t } = useI18n()

const features = computed(() => [
  { icon: '🛡️', title: t('home.feat1title'), desc: t('home.feat1desc') },
  { icon: '🚚', title: t('home.feat2title'), desc: t('home.feat2desc') },
  { icon: '💎', title: t('home.feat3title'), desc: t('home.feat3desc') }
])
</script>

<style scoped>
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
}

.hero-tag {
  margin-bottom: 20px;
}

.hero-title {
  font-size: clamp(3.2rem, 8vw, 5.8rem);
  font-weight: 900;
  line-height: 1.05;
  letter-spacing: -0.04em;
  margin: 0;
}

.hero-subtitle {
  max-width: 620px;
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
  width: 460px;
  height: 460px;
  border-radius: 999px;
  filter: blur(40px);
  pointer-events: none;
}

.orb-1 {
  top: 40px;
  right: -120px;
  background: radial-gradient(circle, rgba(20, 184, 166, 0.16), transparent 70%);
}

.orb-2 {
  bottom: 80px;
  left: -120px;
  background: radial-gradient(circle, rgba(245, 158, 11, 0.14), transparent 70%);
}

.hero-stats {
  display: flex;
  gap: 18px;
  margin-top: 48px;
}

.stat-card {
  min-width: 160px;
  padding: 16px;
  border-radius: 22px;
  text-align: center;
}

.stat-val {
  display: block;
  font-size: 1.6rem;
  font-weight: 900;
  color: #5eead4;
}

.stat-lbl {
  color: #8aa0b8;
  font-size: 0.72rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.hero-card {
  position: relative;
  overflow: hidden;
  min-height: 420px;
  border-radius: 34px;
  padding: 32px;
}

.card-inner-blur {
  position: absolute;
  inset: auto -50px -90px auto;
  width: 220px;
  height: 220px;
  border-radius: 999px;
  background: radial-gradient(circle, rgba(245, 158, 11, 0.24), transparent 70%);
  filter: blur(22px);
  pointer-events: none;
}

.bestseller-tag {
  position: absolute;
  top: 24px;
  right: 24px;
  z-index: 2;
}

.product-visual {
  height: 220px;
  border-radius: 24px;
  margin-top: 48px;
}

.hero-card-info {
  margin-top: 24px;
}

.hero-card-info h3 {
  font-weight: 800;
  font-size: 1.25rem;
  color: white;
  margin: 0;
}

.hero-card-desc {
  color: #8aa0b8;
  font-size: 0.9rem;
  margin-top: 8px;
}

/* Features */
.features-section {
  padding: 80px 0;
}

.features-header {
  text-align: center;
  margin-bottom: 48px;
}

.features-header h2 {
  font-weight: 900;
  font-size: 2.5rem;
  letter-spacing: -0.04em;
  margin: 0;
}

.features-sub {
  color: #bfd0e4;
  margin-top: 8px;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 24px;
}

.feature-card :deep(.p-card) {
  background: rgba(14, 27, 44, 0.92);
  border: 1px solid rgba(148, 163, 184, 0.18);
  border-radius: 26px;
}

.f-icon {
  display: inline-grid;
  place-items: center;
  width: 52px;
  height: 52px;
  border-radius: 16px;
  background: rgba(20, 184, 166, 0.1);
  font-size: 1.4rem;
}

.feature-title {
  font-weight: 800;
  margin-top: 16px;
  margin-bottom: 0;
  color: white;
}

.feature-desc {
  color: #8aa0b8;
  font-size: 0.9rem;
  margin-top: 8px;
}

@media (max-width: 1024px) {
  .hero-inner {
    grid-template-columns: 1fr;
    text-align: center;
    gap: 52px;
  }

  .hero-actions,
  .hero-stats {
    justify-content: center;
  }

  .hero-visual {
    display: flex;
    justify-content: center;
  }

  .feature-grid {
    grid-template-columns: 1fr;
  }
}
</style>
