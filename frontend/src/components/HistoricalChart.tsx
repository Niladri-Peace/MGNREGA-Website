'use client';

import React from 'react';
import { useDistrictHistory } from '@/hooks/useDistrict';
import { formatMonthYear, formatIndianNumber, formatLargeCurrency } from '@/utils/format';
import LoadingSpinner from './ui/LoadingSpinner';
import ErrorMessage from './ui/ErrorMessage';

interface HistoricalChartProps {
  districtId: number;
}

const HistoricalChart: React.FC<HistoricalChartProps> = ({ districtId }) => {
  const { data: history, isLoading, error } = useDistrictHistory(districtId, 1);

  if (isLoading) {
    return (
      <div className="flex justify-center items-center py-12">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  if (error) {
    return (
      <ErrorMessage
        message="Failed to load historical data. Please try again later."
        className="my-8"
      />
    );
  }

  if (!history || history.length === 0) {
    return null;
  }

  // Calculate max values for scaling
  const maxHouseholds = Math.max(...history.map(h => h.households));
  const maxPersonDays = Math.max(...history.map(h => h.person_days));

  return (
    <section className="mb-8">
      <div className="bg-white rounded-lg shadow-card p-6">
        <h2 className="text-2xl font-bold text-gray-800 mb-6">
          Historical Trends / ऐतिहासिक रुझान
        </h2>

        {/* Simple Bar Chart for Households */}
        <div className="mb-8">
          <h3 className="text-lg font-semibold text-gray-700 mb-4">
            Households Employed / परिवारों को रोज़गार
          </h3>
          <div className="space-y-3">
            {history.map((item, index) => {
              const percentage = (item.households / maxHouseholds) * 100;
              return (
                <div key={index} className="flex items-center gap-3">
                  <div className="w-24 text-sm text-gray-600 font-medium">
                    {formatMonthYear(item.year, item.month)}
                  </div>
                  <div className="flex-1">
                    <div className="h-8 bg-gray-100 rounded-lg overflow-hidden relative">
                      <div
                        className="h-full bg-gradient-to-r from-blue-500 to-blue-600 transition-all duration-500 flex items-center justify-end pr-2"
                        style={{ width: `${percentage}%` }}
                      >
                        {percentage > 20 && (
                          <span className="text-white text-xs font-semibold">
                            {formatIndianNumber(item.households)}
                          </span>
                        )}
                      </div>
                    </div>
                  </div>
                  {percentage <= 20 && (
                    <div className="w-20 text-sm text-gray-700 font-semibold">
                      {formatIndianNumber(item.households)}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </div>

        {/* Simple Bar Chart for Person Days */}
        <div className="mb-8">
          <h3 className="text-lg font-semibold text-gray-700 mb-4">
            Person Days Generated / व्यक्ति दिवस
          </h3>
          <div className="space-y-3">
            {history.map((item, index) => {
              const percentage = (item.person_days / maxPersonDays) * 100;
              return (
                <div key={index} className="flex items-center gap-3">
                  <div className="w-24 text-sm text-gray-600 font-medium">
                    {formatMonthYear(item.year, item.month)}
                  </div>
                  <div className="flex-1">
                    <div className="h-8 bg-gray-100 rounded-lg overflow-hidden relative">
                      <div
                        className="h-full bg-gradient-to-r from-green-500 to-green-600 transition-all duration-500 flex items-center justify-end pr-2"
                        style={{ width: `${percentage}%` }}
                      >
                        {percentage > 20 && (
                          <span className="text-white text-xs font-semibold">
                            {formatIndianNumber(item.person_days)}
                          </span>
                        )}
                      </div>
                    </div>
                  </div>
                  {percentage <= 20 && (
                    <div className="w-20 text-sm text-gray-700 font-semibold">
                      {formatIndianNumber(item.person_days)}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </div>

        {/* Summary Table */}
        <div className="mt-8">
          <h3 className="text-lg font-semibold text-gray-700 mb-4">
            Monthly Summary / मासिक सारांश
          </h3>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-4 py-3 text-left font-semibold text-gray-700">Month</th>
                  <th className="px-4 py-3 text-right font-semibold text-gray-700">Households</th>
                  <th className="px-4 py-3 text-right font-semibold text-gray-700">Person Days</th>
                  <th className="px-4 py-3 text-right font-semibold text-gray-700">Works Completed</th>
                  <th className="px-4 py-3 text-right font-semibold text-gray-700">Funds Utilized</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {history.map((item, index) => (
                  <tr key={index} className="hover:bg-gray-50 transition-colors">
                    <td className="px-4 py-3 text-gray-700">
                      {formatMonthYear(item.year, item.month)}
                    </td>
                    <td className="px-4 py-3 text-right text-gray-900 font-medium">
                      {formatIndianNumber(item.households)}
                    </td>
                    <td className="px-4 py-3 text-right text-gray-900 font-medium">
                      {formatIndianNumber(item.person_days)}
                    </td>
                    <td className="px-4 py-3 text-right text-gray-900 font-medium">
                      {formatIndianNumber(item.works_completed)}
                    </td>
                    <td className="px-4 py-3 text-right text-gray-900 font-medium">
                      {formatLargeCurrency(item.funds_utilized)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Insights */}
        <div className="mt-6 p-4 bg-blue-50 rounded-lg">
          <h4 className="font-semibold text-blue-900 mb-2">💡 Key Insights</h4>
          <ul className="text-sm text-blue-800 space-y-1">
            <li>• Total households in last {history.length} months: {formatIndianNumber(history.reduce((sum, h) => sum + h.households, 0))}</li>
            <li>• Total person days generated: {formatIndianNumber(history.reduce((sum, h) => sum + h.person_days, 0))}</li>
            <li>• Total works completed: {formatIndianNumber(history.reduce((sum, h) => sum + h.works_completed, 0))}</li>
          </ul>
        </div>
      </div>
    </section>
  );
};

export default HistoricalChart;
