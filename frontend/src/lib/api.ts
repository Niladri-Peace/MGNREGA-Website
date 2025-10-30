import axios, { AxiosInstance, AxiosResponse, AxiosError } from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Create axios instance
const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    // Add auth token if available
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
apiClient.interceptors.response.use(
  (response: AxiosResponse) => {
    return response;
  },
  (error: AxiosError) => {
    // Handle common errors
    if (error.response?.status === 401) {
      // Unauthorized - redirect to login
      if (typeof window !== 'undefined') {
        localStorage.removeItem('token');
        window.location.href = '/login';
      }
    } else if (error.response?.status === 404) {
      console.error('Resource not found');
    } else if (error.response?.status === 500) {
      console.error('Server error');
    }
    return Promise.reject(error);
  }
);

// API methods
export const api = {
  // States
  getStates: async () => {
    const response = await apiClient.get('/api/v1/states');
    return response.data;
  },

  // Districts
  getDistricts: async (stateId: number) => {
    const response = await apiClient.get('/api/v1/districts', {
      params: { state_id: stateId },
    });
    return response.data;
  },

  // District metrics
  getDistrictMetrics: async (districtId: number, year?: number, month?: number) => {
    const response = await apiClient.get(`/api/v1/metrics/district/${districtId}`, {
      params: { year, month },
    });
    return response.data;
  },

  // District history
  getDistrictHistory: async (districtId: number, years: number = 2) => {
    const response = await apiClient.get(`/api/v1/metrics/district/${districtId}/history`, {
      params: { years },
    });
    return response.data;
  },

  // Geolocation - Detect district by coordinates
  detectDistrictByLocation: async (lat: number, lon: number) => {
    const response = await apiClient.get('/api/v1/districts/detect-by-location', {
      params: { lat, lon },
    });
    return response.data;
  },

  // Search
  searchDistricts: async (query: string) => {
    const response = await apiClient.get('/api/v1/search/districts', {
      params: { q: query },
    });
    return response.data;
  },

  // Health check
  healthCheck: async () => {
    const response = await apiClient.get('/api/v1/health');
    return response.data;
  },
};

export default apiClient;
