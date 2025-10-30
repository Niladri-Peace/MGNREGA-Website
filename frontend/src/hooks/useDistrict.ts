import { useQuery, UseQueryResult } from '@tanstack/react-query';
import { api } from '@/lib/api';

export interface District {
  id: number;
  name: string;
  code: string;
  state_id: number;
  centroid: {
    lat: number;
    lon: number;
  } | null;
}

export interface State {
  id: number;
  name: string;
  code: string;
}

export interface DistrictMetrics {
  district_id: number;
  state_id: number;
  year: number;
  month: number;
  households: {
    total: number;
    sc: number;
    st: number;
    women: number;
  };
  works: {
    total: number;
    completed: number;
    in_progress: number;
  };
  finances: {
    total_funds: number;
    funds_utilized: number;
    wage_expenditure: number;
    material_expenditure: number;
  };
  person_days: {
    total: number;
    sc: number;
    st: number;
    women: number;
  };
  metadata: {
    is_latest: boolean;
    source_url: string;
    updated_at: string;
  };
}

export interface HistoricalMetric {
  year: number;
  month: number;
  households: number;
  person_days: number;
  works_completed: number;
  funds_utilized: number;
}

/**
 * Hook to fetch all states
 */
export const useStates = (): UseQueryResult<State[], Error> => {
  return useQuery({
    queryKey: ['states'],
    queryFn: api.getStates,
    staleTime: 24 * 60 * 60 * 1000, // 24 hours
    cacheTime: 7 * 24 * 60 * 60 * 1000, // 7 days
  });
};

/**
 * Hook to fetch districts by state
 */
export const useDistricts = (stateId: number | null): UseQueryResult<District[], Error> => {
  return useQuery({
    queryKey: ['districts', stateId],
    queryFn: () => api.getDistricts(stateId!),
    enabled: !!stateId,
    staleTime: 24 * 60 * 60 * 1000, // 24 hours
    cacheTime: 7 * 24 * 60 * 60 * 1000, // 7 days
  });
};

/**
 * Hook to fetch district metrics
 */
export const useDistrictMetrics = (
  districtId: number | null,
  year?: number,
  month?: number
): UseQueryResult<DistrictMetrics, Error> => {
  return useQuery({
    queryKey: ['districtMetrics', districtId, year, month],
    queryFn: () => api.getDistrictMetrics(districtId!, year, month),
    enabled: !!districtId,
    staleTime: 1 * 60 * 60 * 1000, // 1 hour
    cacheTime: 24 * 60 * 60 * 1000, // 24 hours
  });
};

/**
 * Hook to fetch district historical data
 */
export const useDistrictHistory = (
  districtId: number | null,
  years: number = 2
): UseQueryResult<HistoricalMetric[], Error> => {
  return useQuery({
    queryKey: ['districtHistory', districtId, years],
    queryFn: () => api.getDistrictHistory(districtId!, years),
    enabled: !!districtId,
    staleTime: 1 * 60 * 60 * 1000, // 1 hour
    cacheTime: 24 * 60 * 60 * 1000, // 24 hours
  });
};

/**
 * Hook to search districts
 */
export const useSearchDistricts = (query: string): UseQueryResult<District[], Error> => {
  return useQuery({
    queryKey: ['searchDistricts', query],
    queryFn: () => api.searchDistricts(query),
    enabled: query.length >= 2,
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
};
