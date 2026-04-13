const API_BASE = 'http://127.0.0.1:8000'

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers || {}),
    },
    ...options,
  })

  const data = await response.json().catch(() => ({}))
  if (!response.ok) {
    throw new Error(data.detail || data.message || 'Request failed')
  }
  return data
}

export const api = {
  getProducts: (category) => request(`/api/products${category ? `?category=${category}` : ''}`),
  getAuctions: () => request('/api/auctions'),
  signup: (payload) => request('/api/auth/signup', { method: 'POST', body: JSON.stringify(payload) }),
  login: (payload) => request('/api/auth/login', { method: 'POST', body: JSON.stringify(payload) }),
  logout: () => request('/api/auth/logout', { method: 'POST' }),
  me: () => request('/api/auth/me'),
  subscribe: (payload) => request('/api/newsletter/subscribe', { method: 'POST', body: JSON.stringify(payload) }),
}
