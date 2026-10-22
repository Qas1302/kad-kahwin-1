import { inject, type InjectionKey } from 'vue'

import type { AppServices } from '../../application/useCases'

export const servicesKey: InjectionKey<AppServices> = Symbol('app-services')

export function useServices(): AppServices {
  const services = inject(servicesKey)
  if (!services) throw new Error('App services were not provided. See src/main.ts.')
  return services
}
