<template>
  <div class="page-content container">
    <div class="checkout-layout">
      <!-- Main Column -->
      <div class="checkout-main">
        <!-- Stepper -->
        <Stepper v-model:value="currentStep" linear class="checkout-stepper anim-fadeInUp">
          <StepList>
            <Step v-for="s in steps" :key="s.id" :value="s.id">{{ s.label }}</Step>
          </StepList>
          <StepPanels>
            <!-- Step 1: Shipping -->
            <StepPanel v-slot="{ activateCallback }" :value="1">
              <div class="step-content glass-heavy">
                <h2 class="text-gradient">{{ $t('checkout.shippingTitle') }}</h2>
                <form @submit.prevent="activateCallback(2)" class="shipping-form">
                  <div class="form-row">
                    <FloatLabel>
                      <InputText id="fullName" v-model="form.fullName" required class="w-full" />
                      <label for="fullName">{{ $t('checkout.fullName') }}</label>
                    </FloatLabel>
                    <FloatLabel>
                      <InputText id="phone" v-model="form.phone" required class="w-full" />
                      <label for="phone">{{ $t('checkout.phone') }}</label>
                    </FloatLabel>
                  </div>
                  <FloatLabel class="full-width">
                    <InputText id="address" v-model="form.address" required class="w-full" />
                    <label for="address">{{ $t('checkout.address') }}</label>
                  </FloatLabel>
                  <div class="form-row">
                    <FloatLabel>
                      <InputText id="zip" v-model="form.zip" required class="w-full" />
                      <label for="zip">{{ $t('checkout.zip') }}</label>
                    </FloatLabel>
                    <FloatLabel>
                      <InputText id="city" v-model="form.city" required class="w-full" />
                      <label for="city">{{ $t('checkout.city') }}</label>
                    </FloatLabel>
                  </div>
                  <div class="step-actions">
                    <Button type="submit" :label="$t('checkout.continue')" icon="pi pi-arrow-right" iconPos="right" />
                  </div>
                </form>
              </div>
            </StepPanel>

            <!-- Step 2: Payment -->
            <StepPanel v-slot="{ activateCallback }" :value="2">
              <div class="step-content glass-heavy">
                <h2 class="text-gradient">{{ $t('checkout.paymentTitle') }}</h2>
                <div class="payment-options">
                  <div
                    v-for="p in paymentMethods"
                    :key="p.id"
                    class="payment-card glass"
                    :class="{ active: form.payment === p.id }"
                    @click="form.payment = p.id"
                  >
                    <span class="p-icon">{{ p.icon }}</span>
                    <div class="p-info">
                      <h4>{{ p.name }}</h4>
                      <p class="p-desc">{{ p.desc }}</p>
                    </div>
                    <RadioButton v-model="form.payment" :value="p.id" />
                  </div>
                </div>
                <div class="step-actions between">
                  <Button @click="activateCallback(1)" :label="$t('checkout.back')" severity="secondary" icon="pi pi-arrow-left" />
                  <Button @click="activateCallback(3)" :label="$t('checkout.summaryBtn')" icon="pi pi-check" />
                </div>
              </div>
            </StepPanel>

            <!-- Step 3: Done -->
            <StepPanel :value="3">
              <div class="step-content glass-heavy success-step anim-fadeInUp">
                <div class="success-icon">🎉</div>
                <h2 class="text-gradient">{{ $t('checkout.successTitle') }}</h2>
                <p class="success-desc">{{ $t('checkout.successDesc') }}</p>
                <router-link to="/produkty">
                  <Button :label="$t('checkout.backToShop')" icon="pi pi-shopping-bag" class="back-btn" />
                </router-link>
              </div>
            </StepPanel>
          </StepPanels>
        </Stepper>
      </div>

      <!-- Summary Sidebar -->
      <aside v-if="currentStep < 3" class="checkout-summary anim-fadeInUp anim-delay-2">
        <div class="summary-card glass-heavy">
          <h3 class="summary-title">{{ $t('checkout.orderSummary') }}</h3>
          <div class="summary-list">
            <div v-for="item in cartStore.items" :key="item.id" class="summary-item">
              <span class="item-qty-name"><Tag :value="item.quantity + 'x'" severity="success" /> {{ item.name }}</span>
              <span class="item-total">{{ (item.price * item.quantity).toFixed(2) }} PLN</span>
            </div>
          </div>
          <Divider />
          <div class="total-row">
            <span>{{ $t('checkout.totalLabel') }}</span>
            <span class="text-primary-gradient">{{ cartStore.totalPrice.toFixed(2) }} PLN</span>
          </div>
          <p class="tax-note">{{ $t('checkout.taxNote') }}</p>
        </div>
      </aside>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
import FloatLabel from 'primevue/floatlabel'
import RadioButton from 'primevue/radiobutton'
import Divider from 'primevue/divider'
import Tag from 'primevue/tag'
import Stepper from 'primevue/stepper'
import StepList from 'primevue/steplist'
import Step from 'primevue/step'
import StepPanels from 'primevue/steppanels'
import StepPanel from 'primevue/steppanel'
import { useCartStore } from '../stores/cart'
import { useI18n } from 'vue-i18n'

const cartStore = useCartStore()
const { t } = useI18n()
const currentStep = ref(1)

const steps = computed(() => [
  { id: 1, label: t('checkout.step1') },
  { id: 2, label: t('checkout.step2') },
  { id: 3, label: t('checkout.step3') }
])

const paymentMethods = computed(() => [
  { id: 'blik', name: t('checkout.blik'), icon: '📱', desc: t('checkout.blikDesc') },
  { id: 'card', name: t('checkout.card'), icon: '💳', desc: t('checkout.cardDesc') },
  { id: 'transfer', name: t('checkout.transfer'), icon: '🏦', desc: t('checkout.transferDesc') }
])

const form = reactive({
  fullName: '',
  phone: '',
  address: '',
  zip: '',
  city: '',
  payment: 'blik'
})
</script>

<style scoped>
.checkout-layout {
  display: grid;
  grid-template-columns: 1fr 360px;
  gap: 40px;
}

.step-content {
  padding: 36px;
  border-radius: 28px;
  margin-top: 24px;
}

.step-content h2 {
  font-weight: 900;
  font-size: 1.75rem;
  letter-spacing: -0.03em;
  margin: 0 0 28px;
}

.shipping-form {
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

.step-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 8px;
}

.step-actions.between {
  justify-content: space-between;
}

.payment-options {
  display: flex;
  flex-direction: column;
  gap: 14px;
  margin-bottom: 28px;
}

.payment-card {
  display: flex;
  align-items: center;
  gap: 18px;
  padding: 18px 20px;
  border-radius: 18px;
  cursor: pointer;
  transition: all 0.2s;
}

.payment-card:hover {
  background: rgba(255, 255, 255, 0.06);
}

.payment-card.active {
  border-color: #14b8a6;
  background: rgba(20, 184, 166, 0.06);
}

.p-icon {
  font-size: 1.5rem;
}

.p-info {
  flex: 1;
}

.p-info h4 {
  margin: 0;
  font-weight: 700;
  color: white;
}

.p-desc {
  font-size: 0.8rem;
  color: #8aa0b8;
  margin: 2px 0 0;
}

.success-step {
  text-align: center;
}

.success-icon {
  font-size: 5rem;
  margin-bottom: 16px;
}

.success-desc {
  color: #bfd0e4;
  margin: 12px 0 32px;
}

.summary-card {
  padding: 28px;
  border-radius: 28px;
  position: sticky;
  top: 120px;
}

.summary-title {
  font-weight: 800;
  margin: 0 0 20px;
  color: white;
}

.summary-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  font-size: 0.9rem;
}

.item-qty-name {
  display: flex;
  align-items: center;
  gap: 8px;
}

.item-total {
  font-weight: 700;
}

.total-row {
  display: flex;
  justify-content: space-between;
  font-size: 1.4rem;
  font-weight: 900;
}

.tax-note {
  text-align: center;
  font-size: 0.75rem;
  color: #8aa0b8;
  margin-top: 12px;
}

@media (max-width: 1024px) {
  .checkout-layout { grid-template-columns: 1fr; }
  .checkout-summary { order: -1; }
  .form-row { grid-template-columns: 1fr; }
}
</style>
