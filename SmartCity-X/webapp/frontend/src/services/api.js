export const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:5000'

async function request(path, options = {}) {
  const controller = new AbortController()
  const timer = setTimeout(() => controller.abort(), 30000)
  try {
    const response = await fetch(`${API_BASE}${path}`, { ...options, signal: controller.signal, headers: { Accept: 'application/json', ...(options.headers || {}) } })
    const body = await response.json().catch(() => ({}))
    const message = body.error?.message || body.message || (typeof body.error === 'string' ? body.error : null)
    if (!response.ok || body.status === 'error') throw new Error(message || `HTTP ${response.status}`)
    return body.data ?? body
  } catch (error) {
    if (error.name === 'AbortError') throw new Error('Backend request timed out', { cause: error })
    if (error instanceof TypeError) throw new Error('Backend unavailable', { cause: error })
    throw error
  } finally { clearTimeout(timer) }
}

export const api = {
  attack: (id) => request(`/api/attacks/${id}`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: '{}' }),
  health: () => request('/api/health'),
  camera: (id) => request(`/api/cctv/${id}`),
  resetCamera: (id) => request(`/api/cctv/${id}/reset`, { method: 'POST' }),
  resetScada: () => request('/api/scada/reset', { method: 'POST' }),
}
