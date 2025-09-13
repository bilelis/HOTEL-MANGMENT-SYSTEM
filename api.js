/**
 * Hotel Management System - API Service Configuration
 * Handles all API communications between frontend and backend
 */

// API Configuration
const API_CONFIG = {
  BASE_URL: process.env.NODE_ENV === 'production' 
    ? 'https://your-hotel-api.com/api/v1' 
    : 'http://localhost:8000/api/v1',
  TIMEOUT: 10000,
  HEADERS: {
    'Content-Type': 'application/json',
  }
}

// API Client Class
class ApiClient {
  constructor() {
    this.baseURL = API_CONFIG.BASE_URL
    this.timeout = API_CONFIG.TIMEOUT
    this.headers = API_CONFIG.HEADERS
    this.token = localStorage.getItem('auth_token')
  }

  // Set authentication token
  setAuthToken(token) {
    this.token = token
    localStorage.setItem('auth_token', token)
  }

  // Remove authentication token
  removeAuthToken() {
    this.token = null
    localStorage.removeItem('auth_token')
  }

  // Get headers with authentication
  getHeaders() {
    const headers = { ...this.headers }
    if (this.token) {
      headers.Authorization = `Bearer ${this.token}`
    }
    return headers
  }

  // Generic request method
  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`
    const config = {
      timeout: this.timeout,
      headers: this.getHeaders(),
      ...options
    }

    try {
      const response = await fetch(url, config)
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      return await response.json()
    } catch (error) {
      console.error('API request failed:', error)
      throw error
    }
  }

  // GET request
  async get(endpoint) {
    return this.request(endpoint, { method: 'GET' })
  }

  // POST request
  async post(endpoint, data) {
    return this.request(endpoint, {
      method: 'POST',
      body: JSON.stringify(data)
    })
  }

  // PUT request
  async put(endpoint, data) {
    return this.request(endpoint, {
      method: 'PUT',
      body: JSON.stringify(data)
    })
  }

  // DELETE request
  async delete(endpoint) {
    return this.request(endpoint, { method: 'DELETE' })
  }
}

// Create API client instance
const apiClient = new ApiClient()

// Analytics API methods
export const analyticsAPI = {
  getRevenueToday: () => apiClient.get('/analytics/revenue-today'),
  getOccupancyRate: () => apiClient.get('/analytics/occupancy-rate'),
  getTopItems: () => apiClient.get('/analytics/top-items'),
  getGuestSpending: () => apiClient.get('/analytics/guest-spending'),
  getRevenueSplit: () => apiClient.get('/analytics/revenue-split'),
  getARPR: () => apiClient.get('/analytics/arpr'),
}

// Reception API methods
export const receptionAPI = {
  getReservations: () => apiClient.get('/reservations'),
  createReservation: (data) => apiClient.post('/reservations', data),
  updateReservation: (id, data) => apiClient.put(`/reservations/${id}`, data),
  checkIn: (id) => apiClient.put(`/reservations/${id}/checkin`),
  checkOut: (id) => apiClient.put(`/reservations/${id}/checkout`),
  getRoomStatus: () => apiClient.get('/rooms/status'),
  updateRoomStatus: (id, status) => apiClient.put(`/rooms/${id}/status`, { status }),
}

// F&B API methods
export const fnbAPI = {
  getMenuItems: () => apiClient.get('/items'),
  createOrder: (data) => apiClient.post('/orders', data),
  getActiveOrders: () => apiClient.get('/orders/active'),
  updateOrderStatus: (id, status) => apiClient.put(`/orders/${id}/status`, { status }),
  getOrderHistory: () => apiClient.get('/orders/history'),
}

// Authentication API methods
export const authAPI = {
  login: (credentials) => apiClient.post('/auth/login', credentials),
  logout: () => {
    apiClient.removeAuthToken()
    return Promise.resolve()
  },
  getCurrentUser: () => apiClient.get('/auth/me'),
  refreshToken: () => apiClient.post('/auth/refresh'),
}

// Export API client for direct use
export default apiClient

// Mock data fallback (for development/demo)
export const mockData = {
  revenueToday: {
    total_revenue: 15420.50,
    room_revenue: 9800.00,
    fnb_revenue: 5620.50,
    date: new Date().toISOString().split('T')[0]
  },
  occupancyRate: {
    total_rooms: 50,
    occupied_rooms: 38,
    available_rooms: 10,
    maintenance_rooms: 1,
    cleaning_rooms: 1,
    occupancy_rate: 79.17
  },
  topItems: {
    items: [
      { item_name: "Grilled Salmon", outlet_name: "Grand Restaurant", quantity_sold: 15, revenue: 480.00 },
      { item_name: "Signature Martini", outlet_name: "Sky Bar", quantity_sold: 12, revenue: 192.00 },
      { item_name: "Caesar Salad", outlet_name: "Grand Restaurant", quantity_sold: 10, revenue: 180.00 },
      { item_name: "Cappuccino", outlet_name: "Lobby Café", quantity_sold: 25, revenue: 137.50 },
      { item_name: "Beef Tenderloin", outlet_name: "Grand Restaurant", quantity_sold: 8, revenue: 360.00 }
    ]
  },
  guestSpending: {
    guests: [
      { guest_name: "John Smith", room_number: "102", total_spending: 1250.00, room_charges: 720.00, fnb_charges: 530.00 },
      { guest_name: "Ahmed Al-Rashid", room_number: "203", total_spending: 980.00, room_charges: 700.00, fnb_charges: 280.00 },
      { guest_name: "Maria Garcia", room_number: "201", total_spending: 650.00, room_charges: 480.00, fnb_charges: 170.00 }
    ]
  },
  revenueSplit: {
    total_revenue: 15420.50,
    split: [
      { category: "Rooms", amount: 9800.00, percentage: 63.5 },
      { category: "F&B", amount: 5620.50, percentage: 36.5 }
    ]
  },
  arpr: {
    arpr: 257.89,
    total_revenue: 9800.00,
    occupied_rooms: 38
  }
}

// Utility function to use mock data in development
export const useMockData = process.env.NODE_ENV === 'development' && !process.env.REACT_APP_USE_REAL_API

