'use client';

import { useState, useEffect } from 'react';
import { useStates, useDistricts } from '@/hooks/useDistrict';
import { useGeolocation } from '@/hooks/useGeolocation';
import DistrictSelector from '@/components/DistrictSelector';
import MetricsOverview from '@/components/MetricsOverview';
import HistoricalChart from '@/components/HistoricalChart';
import LoadingSpinner from '@/components/ui/LoadingSpinner';
import ErrorMessage from '@/components/ui/ErrorMessage';

export default function HomePage() {
  const [selectedState, setSelectedState] = useState<number | null>(null);
  const [selectedDistrict, setSelectedDistrict] = useState<number | null>(null);

  const { data: states, isLoading: statesLoading } = useStates();
  const { data: districts, isLoading: districtsLoading } = useDistricts(selectedState);
  const { detectedDistrict, loading: geoLoading, error: geoError, requestLocation } = useGeolocation();

  // Auto-select state and district when location is detected
  useEffect(() => {
    if (detectedDistrict && states) {
      // Find the state that matches the detected state name
      const state = states.find(s => s.name === detectedDistrict.state_name);
      if (state) {
        setSelectedState(state.id);
        // District will be set after districts are loaded
      }
    }
  }, [detectedDistrict, states]);

  // Auto-select district when districts are loaded after state selection
  useEffect(() => {
    if (detectedDistrict && districts && selectedState) {
      const district = districts.find(d => d.name === detectedDistrict.name);
      if (district) {
        setSelectedDistrict(district.id);
      }
    }
  }, [detectedDistrict, districts, selectedState]);

  const handleStateChange = (stateId: number) => {
    setSelectedState(stateId);
    setSelectedDistrict(null);
  };

  const handleDistrictChange = (districtId: number) => {
    setSelectedDistrict(districtId);
  };

  const handleUseLocation = () => {
    requestLocation();
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-primary text-white shadow-lg">
        <div className="container mx-auto px-4 py-6">
          <h1 className="text-3xl md:text-4xl font-bold">
            हमारी आवाज़, हमारे अधिकार
          </h1>
          <p className="text-lg md:text-xl mt-2 opacity-90">
            Our Voice, Our Rights - MGNREGA Dashboard
          </p>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        {/* District Selection Section */}
        <section className="bg-white rounded-lg shadow-card p-6 mb-8">
          <h2 className="text-2xl font-bold mb-4 text-gray-800">
            Select Your District
          </h2>
          
          {/* Location Detection Button */}
          <div className="mb-6">
            <button
              onClick={handleUseLocation}
              disabled={geoLoading}
              className="w-full md:w-auto bg-secondary text-white px-6 py-4 rounded-lg font-semibold text-lg shadow-md hover:bg-secondary-dark transition-all tap-target flex items-center justify-center gap-2"
            >
              {geoLoading ? (
                <>
                  <LoadingSpinner size="sm" />
                  Detecting Location...
                </>
              ) : (
                <>
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                  Use My Location
                </>
              )}
            </button>
            
            {geoError && (
              <ErrorMessage message={geoError} className="mt-2" />
            )}
            
            {detectedDistrict && (
              <div className="mt-3 p-4 bg-green-50 border border-green-200 rounded-lg">
                <p className="text-green-800 font-medium">
                  📍 Detected: {detectedDistrict.name}, {detectedDistrict.state_name}
                </p>
              </div>
            )}
          </div>

          <div className="border-t pt-6">
            <p className="text-gray-600 mb-4 text-center">OR</p>
            
            <DistrictSelector
              states={states || []}
              districts={districts || []}
              selectedState={selectedState}
              selectedDistrict={selectedDistrict}
              onStateChange={handleStateChange}
              onDistrictChange={handleDistrictChange}
              statesLoading={statesLoading}
              districtsLoading={districtsLoading}
            />
          </div>
        </section>

        {/* Metrics Display */}
        {selectedDistrict && (
          <>
            <MetricsOverview districtId={selectedDistrict} />
            <HistoricalChart districtId={selectedDistrict} />
          </>
        )}

        {/* Information Section for First-Time Users */}
        {!selectedDistrict && (
          <section className="bg-blue-50 rounded-lg p-6 mt-8">
            <h3 className="text-xl font-bold text-blue-900 mb-3">
              What is MGNREGA?
            </h3>
            <p className="text-blue-800 leading-relaxed mb-4">
              MGNREGA (Mahatma Gandhi National Rural Employment Guarantee Act) guarantees 100 days of wage employment 
              in a financial year to rural households. This dashboard helps you understand how your district is performing.
            </p>
            
            <div className="grid md:grid-cols-3 gap-4 mt-6">
              <div className="bg-white p-4 rounded-lg">
                <div className="text-3xl mb-2">👥</div>
                <h4 className="font-semibold text-gray-900 mb-1">Employment</h4>
                <p className="text-sm text-gray-600">Track how many families got work</p>
              </div>
              
              <div className="bg-white p-4 rounded-lg">
                <div className="text-3xl mb-2">💰</div>
                <h4 className="font-semibold text-gray-900 mb-1">Wages</h4>
                <p className="text-sm text-gray-600">See total wages paid to workers</p>
              </div>
              
              <div className="bg-white p-4 rounded-lg">
                <div className="text-3xl mb-2">🔨</div>
                <h4 className="font-semibold text-gray-900 mb-1">Works</h4>
                <p className="text-sm text-gray-600">View completed infrastructure projects</p>
              </div>
            </div>
          </section>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-gray-800 text-white py-6 mt-12">
        <div className="container mx-auto px-4 text-center">
          <p className="text-sm opacity-75">
            Data source: <a href="https://data.gov.in" className="underline hover:opacity-100">data.gov.in</a>
          </p>
          <p className="text-xs mt-2 opacity-60">
            This is a citizen initiative to make MGNREGA data accessible to everyone
          </p>
        </div>
      </footer>
    </div>
  );
}
