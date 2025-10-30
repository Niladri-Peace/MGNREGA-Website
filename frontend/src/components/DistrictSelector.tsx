import React from 'react';
import { State, District } from '@/hooks/useDistrict';
import LoadingSpinner from './ui/LoadingSpinner';

interface DistrictSelectorProps {
  states: State[];
  districts: District[];
  selectedState: number | null;
  selectedDistrict: number | null;
  onStateChange: (stateId: number) => void;
  onDistrictChange: (districtId: number) => void;
  statesLoading: boolean;
  districtsLoading: boolean;
}

const DistrictSelector: React.FC<DistrictSelectorProps> = ({
  states,
  districts,
  selectedState,
  selectedDistrict,
  onStateChange,
  onDistrictChange,
  statesLoading,
  districtsLoading,
}) => {
  return (
    <div className="grid md:grid-cols-2 gap-4">
      {/* State Selection */}
      <div>
        <label
          htmlFor="state-select"
          className="block text-sm font-medium text-gray-700 mb-2"
        >
          Select State / राज्य चुनें
        </label>
        <div className="relative">
          <select
            id="state-select"
            value={selectedState || ''}
            onChange={(e) => onStateChange(Number(e.target.value))}
            disabled={statesLoading}
            className="w-full px-4 py-3 text-lg border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent appearance-none cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
            aria-label="Select state"
          >
            <option value="">Choose a state...</option>
            {states.map((state) => (
              <option key={state.id} value={state.id}>
                {state.name}
              </option>
            ))}
          </select>
          {statesLoading && (
            <div className="absolute right-3 top-1/2 transform -translate-y-1/2">
              <LoadingSpinner size="sm" />
            </div>
          )}
          <div className="absolute right-3 top-1/2 transform -translate-y-1/2 pointer-events-none">
            {!statesLoading && (
              <svg
                className="w-5 h-5 text-gray-400"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M19 9l-7 7-7-7"
                />
              </svg>
            )}
          </div>
        </div>
      </div>

      {/* District Selection */}
      <div>
        <label
          htmlFor="district-select"
          className="block text-sm font-medium text-gray-700 mb-2"
        >
          Select District / जिला चुनें
        </label>
        <div className="relative">
          <select
            id="district-select"
            value={selectedDistrict || ''}
            onChange={(e) => onDistrictChange(Number(e.target.value))}
            disabled={!selectedState || districtsLoading}
            className="w-full px-4 py-3 text-lg border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent appearance-none cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
            aria-label="Select district"
          >
            <option value="">
              {!selectedState ? 'First select a state...' : 'Choose a district...'}
            </option>
            {districts.map((district) => (
              <option key={district.id} value={district.id}>
                {district.name}
              </option>
            ))}
          </select>
          {districtsLoading && (
            <div className="absolute right-3 top-1/2 transform -translate-y-1/2">
              <LoadingSpinner size="sm" />
            </div>
          )}
          <div className="absolute right-3 top-1/2 transform -translate-y-1/2 pointer-events-none">
            {!districtsLoading && (
              <svg
                className="w-5 h-5 text-gray-400"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M19 9l-7 7-7-7"
                />
              </svg>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default DistrictSelector;
