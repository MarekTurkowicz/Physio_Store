import { createI18n } from 'vue-i18n'
import pl from './locales/pl.json'
import en from './locales/en.json'
import de from './locales/de.json'
import es from './locales/es.json'
import fr from './locales/fr.json'

export const SUPPORTED_LOCALES = [
  { code: 'pl', label: 'Polski',   countryCode: 'pl' },
  { code: 'en', label: 'English',  countryCode: 'us' },
  { code: 'de', label: 'Deutsch',  countryCode: 'de' },
  { code: 'es', label: 'Español',  countryCode: 'es' },
  { code: 'fr', label: 'Français', countryCode: 'fr' },
]

const i18n = createI18n({
  legacy: false,
  globalInjection: true,
  locale: 'pl',
  fallbackLocale: 'en',
  messages: { pl, en, de, es, fr }
})

export default i18n
