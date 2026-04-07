<template>
  <div class="page-content container anim-fadeInUp">
    <header class="contact-header">
      <Tag :value="$t('contact.tag')" severity="success" rounded />
      <h1 class="text-gradient">{{ $t('contact.title') }}</h1>
      <p class="contact-desc">
        {{ $t('contact.subtitle') }}
      </p>
    </header>

    <div class="contact-cards">
      <Card v-for="card in contactCards" :key="card.title" class="contact-card">
        <template #content>
          <div class="card-icon">{{ card.icon }}</div>
          <h3 class="card-title">{{ card.title }}</h3>
          <p class="card-desc">{{ card.desc }}</p>
          <a :href="card.href" class="card-link text-primary-gradient">{{ card.linkText }}</a>
        </template>
      </Card>
    </div>

    <!-- Contact Form -->
    <div class="contact-form-section glass anim-fadeInUp anim-delay-2">
      <div class="form-layout">
        <div class="form-side">
          <h2 class="text-gradient">{{ $t('contact.formTitle') }}</h2>
          <form @submit.prevent="handleSubmit" class="contact-form">
            <div class="form-row">
              <FloatLabel>
                <InputText id="cName" v-model="formData.name" required class="w-full" />
                <label for="cName">{{ $t('contact.name') }}</label>
              </FloatLabel>
              <FloatLabel>
                <InputText id="cEmail" v-model="formData.email" type="email" required class="w-full" />
                <label for="cEmail">{{ $t('contact.email') }}</label>
              </FloatLabel>
            </div>
            <FloatLabel>
              <Textarea id="cMessage" v-model="formData.message" rows="5" required class="w-full" />
              <label for="cMessage">{{ $t('contact.message') }}</label>
            </FloatLabel>
            <Button
              type="submit"
              :label="sent ? $t('contact.sent') : $t('contact.send')"
              :icon="sent ? 'pi pi-check' : 'pi pi-send'"
              :disabled="sent"
              :severity="sent ? 'success' : 'primary'"
              class="w-full"
            />
          </form>
        </div>

        <div class="map-side glass-heavy">
          <i class="pi pi-map-marker map-icon"></i>
          <h4>{{ $t('contact.hq') }}</h4>
          <p class="map-address">ul. Rehabilitacyjna 12<br />00-950 Warszawa</p>
          <Tag value="Map Placeholder" severity="info" rounded />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import Card from 'primevue/card'
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
import FloatLabel from 'primevue/floatlabel'
import Textarea from 'primevue/textarea'
import Tag from 'primevue/tag'
import { useToast } from 'primevue/usetoast'
import { useI18n } from 'vue-i18n'

const toast = useToast()
const { t } = useI18n()
const sent = ref(false)
const formData = reactive({ name: '', email: '', message: '' })

const contactCards = computed(() => [
  { icon: '📧', title: t('contact.sales'), desc: t('contact.salesDesc'), href: 'mailto:sklep@physiostore.pl', linkText: 'sklep@physiostore.pl' },
  { icon: '🎧', title: t('contact.support'), desc: t('contact.supportDesc'), href: 'mailto:wsparcie@physiostore.pl', linkText: 'wsparcie@physiostore.pl' },
  { icon: '📞', title: t('contact.hotline'), desc: t('contact.hotlineDesc'), href: 'tel:+48123456789', linkText: '+48 123 456 789' }
])

const handleSubmit = () => {
  sent.value = true
  toast.add({ severity: 'success', summary: t('contact.sentToast'), detail: t('contact.sentDetail'), life: 4000 })
}
</script>

<style scoped>
.contact-header {
  text-align: center;
  margin-bottom: 48px;
}

.contact-header h1 {
  font-weight: 900;
  font-size: 2.8rem;
  letter-spacing: -0.04em;
  margin: 16px 0 0;
}

.contact-desc {
  color: #bfd0e4;
  margin-top: 12px;
  max-width: 560px;
  margin-left: auto;
  margin-right: auto;
}

.contact-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px;
}

.contact-card :deep(.p-card) {
  background: rgba(14, 27, 44, 0.92);
  border: 1px solid rgba(148, 163, 184, 0.18);
  border-radius: 26px;
}

.card-icon {
  font-size: 2rem;
  margin-bottom: 12px;
}

.card-title {
  font-weight: 800;
  color: white;
  margin: 0;
}

.card-desc {
  font-size: 0.82rem;
  color: #8aa0b8;
  margin: 8px 0 16px;
}

.card-link {
  font-weight: 700;
  font-size: 0.9rem;
}

.contact-form-section {
  padding: 48px;
  border-radius: 32px;
  margin-top: 48px;
}

.form-layout {
  display: grid;
  grid-template-columns: 1fr 300px;
  gap: 40px;
}

.form-side h2 {
  font-weight: 900;
  font-size: 1.75rem;
  letter-spacing: -0.03em;
  margin: 0 0 28px;
}

.contact-form {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.w-full {
  width: 100%;
}

.map-side {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 32px;
  border-radius: 24px;
  min-height: 280px;
}

.map-icon {
  font-size: 2.5rem;
  color: #5eead4;
  margin-bottom: 16px;
}

.map-side h4 {
  margin: 0;
  font-weight: 800;
  color: white;
}

.map-address {
  font-size: 0.82rem;
  color: #8aa0b8;
  margin: 8px 0 16px;
}

@media (max-width: 1024px) {
  .form-layout { grid-template-columns: 1fr; }
  .form-row { grid-template-columns: 1fr; }
  .map-side { display: none; }
}
</style>
