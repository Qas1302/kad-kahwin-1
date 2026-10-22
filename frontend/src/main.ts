/* Composition root: builds the infrastructure adapters and hands the use cases to the Vue app. */
import { createApp } from 'vue'

import { createAppServices } from './application/useCases'
import { HttpEventGateway } from './infrastructure/http/eventApi'
import { HttpClient } from './infrastructure/http/httpClient'
import { HttpRsvpGateway } from './infrastructure/http/rsvpApi'
import { LocalReceiptStore } from './infrastructure/storage/localReceiptStore'
import App from './presentation/App.vue'
import { servicesKey } from './presentation/composables/useServices'
import './presentation/styles/base.css'

const http = new HttpClient(import.meta.env.VITE_API_BASE_URL || '/api/v1')

const services = createAppServices({
  events: new HttpEventGateway(http),
  rsvps: new HttpRsvpGateway(http),
  receipts: new LocalReceiptStore(),
})

createApp(App).provide(servicesKey, services).mount('#app')
