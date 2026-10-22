import { GatewayError } from '../../application/errors'

interface RequestOptions {
  method?: 'GET' | 'POST' | 'PUT'
  body?: unknown
  headers?: Record<string, string>
}

interface ApiErrorBody {
  error?: { code?: string; message?: string; field?: string | null }
}

export class HttpClient {
  private readonly baseUrl: string

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl.replace(/\/+$/, '')
  }

  async request<T>(path: string, { method = 'GET', body, headers = {} }: RequestOptions = {}): Promise<T> {
    let response: Response
    try {
      response = await fetch(`${this.baseUrl}${path}`, {
        method,
        headers: {
          Accept: 'application/json',
          ...(body === undefined ? {} : { 'Content-Type': 'application/json' }),
          ...headers,
        },
        body: body === undefined ? undefined : JSON.stringify(body),
      })
    } catch {
      throw new GatewayError("We couldn't reach the server. Please check your connection and try again.", {
        code: 'network_error',
        status: 0,
      })
    }

    const data: unknown = await response.json().catch(() => null)

    if (!response.ok) {
      const error = (data as ApiErrorBody | null)?.error
      throw new GatewayError(error?.message || 'Something went wrong. Please try again.', {
        code: error?.code || 'http_error',
        status: response.status,
        field: error?.field ?? undefined,
      })
    }
    return data as T
  }
}
