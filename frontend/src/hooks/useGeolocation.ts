import { useState, useEffect } from 'react';
import { api } from '@/lib/api';

export interface GeolocationPosition {
  latitude: number;
  longitude: number;
  accuracy: number;
}

export interface DetectedDistrict {
  id: number;
  name: string;
  state_name: string;
  confidence: number;
}

export interface UseGeolocationReturn {
  position: GeolocationPosition | null;
  detectedDistrict: DetectedDistrict | null;
  loading: boolean;
  error: string | null;
  requestLocation: () => void;
  clearLocation: () => void;
}

/**
 * Hook to handle geolocation and district detection
 */
export const useGeolocation = (): UseGeolocationReturn => {
  const [position, setPosition] = useState<GeolocationPosition | null>(null);
  const [detectedDistrict, setDetectedDistrict] = useState<DetectedDistrict | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const requestLocation = () => {
    if (!navigator.geolocation) {
      setError('Geolocation is not supported by your browser');
      return;
    }

    setLoading(true);
    setError(null);

    navigator.geolocation.getCurrentPosition(
      async (pos) => {
        const { latitude, longitude, accuracy } = pos.coords;
        
        setPosition({
          latitude,
          longitude,
          accuracy,
        });

        // Detect district based on coordinates
        try {
          const district = await api.detectDistrictByLocation(latitude, longitude);
          setDetectedDistrict(district);
          setLoading(false);
        } catch (err) {
          console.error('Error detecting district:', err);
          setError('Could not detect district from your location');
          setLoading(false);
        }
      },
      (err) => {
        setLoading(false);
        
        switch (err.code) {
          case err.PERMISSION_DENIED:
            setError('Location permission denied. Please enable location access.');
            break;
          case err.POSITION_UNAVAILABLE:
            setError('Location information is unavailable.');
            break;
          case err.TIMEOUT:
            setError('Location request timed out.');
            break;
          default:
            setError('An unknown error occurred while getting location.');
        }
      },
      {
        enableHighAccuracy: true,
        timeout: 10000,
        maximumAge: 0,
      }
    );
  };

  const clearLocation = () => {
    setPosition(null);
    setDetectedDistrict(null);
    setError(null);
  };

  return {
    position,
    detectedDistrict,
    loading,
    error,
    requestLocation,
    clearLocation,
  };
};

/**
 * Hook to check if geolocation is available
 */
export const useGeolocationAvailable = (): boolean => {
  const [available, setAvailable] = useState<boolean>(false);

  useEffect(() => {
    setAvailable('geolocation' in navigator);
  }, []);

  return available;
};
