'use client';

import React from 'react';
import { useDistrictMetrics } from '@/hooks/useDistrict';
import { useSpeech } from '@/hooks/useSpeech';
import { formatLargeCurrency, formatIndianNumber, getTrendIndicator, getTrendColor } from '@/utils/format';
import LoadingSpinner from './ui/LoadingSpinner';
import ErrorMessage from './ui/ErrorMessage';

interface MetricsOverviewProps {
  districtId: number;
}

interface MetricCardProps {
  title: string;
  value: string;
  icon: string;
  color: string;
  description: string;
  audioText: string;
  trend?: 'up' | 'down' | 'flat';
}

const MetricCard: React.FC<MetricCardProps> = ({
  title,
  value,
  icon,
  color,
  description,
  audioText,
  trend,
}) => {
  const { speak, speaking } = useSpeech();

  const handleSpeak = () => {
    speak(audioText, 'hi-IN');
  };

  return (
    <div className={`bg-white rounded-xl shadow-card hover:shadow-card-hover transition-all p-6 border-l-4 ${color}`}>
      <div className="flex items-start justify-between mb-4">
        <div className="text-4xl">{icon}</div>
        <button
          onClick={handleSpeak}
          disabled={speaking}
          className="p-2 rounded-full bg-blue-50 hover:bg-blue-100 transition-colors tap-target"
          aria-label={`Listen to ${title}`}
        >
          <svg
            className={`w-6 h-6 text-blue-600 ${speaking ? 'animate-pulse' : ''}`}
            fill="currentColor"
            viewBox="0 0 20 20"
          >
            <path
              fillRule="evenodd"
              d="M9.383 3.076A1 1 0 0110 4v12a1 1 0 01-1.707.707L4.586 13H2a1 1 0 01-1-1V8a1 1 0 011-1h2.586l3.707-3.707a1 1 0 011.09-.217zM14.657 2.929a1 1 0 011.414 0A9.972 9.972 0 0119 10a9.972 9.972 0 01-2.929 7.071 1 1 0 01-1.414-1.414A7.971 7.971 0 0017 10c0-2.21-.894-4.208-2.343-5.657a1 1 0 010-1.414zm-2.829 2.828a1 1 0 011.415 0A5.983 5.983 0 0115 10a5.984 5.984 0 01-1.757 4.243 1 1 0 01-1.415-1.415A3.984 3.984 0 0013 10a3.983 3.983 0 00-1.172-2.828 1 1 0 010-1.415z"
              clipRule="evenodd"
            />
          </svg>
        </button>
      </div>

      <h3 className="text-sm font-medium text-gray-600 mb-1">{title}</h3>
      <div className="flex items-end justify-between">
        <p className="text-3xl font-bold text-gray-900">{value}</p>
        {trend && (
          <div className={`flex items-center ${getTrendColor(trend)}`}>
            {trend === 'up' && (
              <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fillRule="evenodd"
                  d="M5.293 9.707a1 1 0 010-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L11 7.414V15a1 1 0 11-2 0V7.414L6.707 9.707a1 1 0 01-1.414 0z"
                  clipRule="evenodd"
                />
              </svg>
            )}
            {trend === 'down' && (
              <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fillRule="evenodd"
                  d="M14.707 10.293a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 111.414-1.414L9 12.586V5a1 1 0 012 0v7.586l2.293-2.293a1 1 0 011.414 0z"
                  clipRule="evenodd"
                />
              </svg>
            )}
          </div>
        )}
      </div>
      <p className="text-sm text-gray-500 mt-2">{description}</p>
    </div>
  );
};

const MetricsOverview: React.FC<MetricsOverviewProps> = ({ districtId }) => {
  const { data: metrics, isLoading, error } = useDistrictMetrics(districtId);

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
        message="Failed to load district metrics. Please try again later."
        className="my-8"
      />
    );
  }

  if (!metrics) {
    return null;
  }

  const metricsData: MetricCardProps[] = [
    {
      title: 'Households / परिवार',
      value: formatIndianNumber(metrics.households.total),
      icon: '👥',
      color: 'border-blue-500',
      description: 'Total families that received employment',
      audioText: `कुल ${metrics.households.total} परिवारों को रोज़गार मिला। इसमें ${metrics.households.women} महिला परिवार शामिल हैं।`,
      trend: 'up',
    },
    {
      title: 'Person Days / व्यक्ति दिवस',
      value: formatIndianNumber(metrics.person_days.total),
      icon: '📅',
      color: 'border-green-500',
      description: 'Total days of work provided',
      audioText: `कुल ${metrics.person_days.total} व्यक्ति दिवस का रोज़गार दिया गया।`,
      trend: 'up',
    },
    {
      title: 'Wages Paid / मज़दूरी',
      value: formatLargeCurrency(metrics.finances.wage_expenditure),
      icon: '💰',
      color: 'border-yellow-500',
      description: 'Total wages paid to workers',
      audioText: `मज़दूरों को कुल ${formatLargeCurrency(metrics.finances.wage_expenditure)} मज़दूरी दी गई।`,
      trend: 'up',
    },
    {
      title: 'Works Completed / पूर्ण कार्य',
      value: formatIndianNumber(metrics.works.completed),
      icon: '🔨',
      color: 'border-purple-500',
      description: 'Infrastructure projects completed',
      audioText: `कुल ${metrics.works.completed} परियोजनाएं पूरी हुईं।`,
      trend: 'flat',
    },
  ];

  return (
    <section className="mb-8">
      <div className="bg-white rounded-lg shadow-card p-6 mb-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-2xl font-bold text-gray-800">
            Performance Overview / प्रदर्शन सारांश
          </h2>
          <div className="text-sm text-gray-500">
            Updated: {new Date(metrics.metadata.updated_at).toLocaleDateString('en-IN')}
          </div>
        </div>
        <p className="text-gray-600 mb-2">
          Data for {metrics.year} - Month {metrics.month}
        </p>
      </div>

      <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
        {metricsData.map((metric, index) => (
          <MetricCard key={index} {...metric} />
        ))}
      </div>

      {/* Additional Details */}
      <div className="bg-white rounded-lg shadow-card p-6 mt-6">
        <h3 className="text-xl font-bold text-gray-800 mb-4">
          Detailed Breakdown / विस्तृत विवरण
        </h3>
        
        <div className="grid md:grid-cols-2 gap-6">
          {/* Social Categories */}
          <div>
            <h4 className="text-lg font-semibold text-gray-700 mb-3">
              Social Categories / सामाजिक श्रेणियाँ
            </h4>
            <div className="space-y-2">
              <div className="flex justify-between items-center p-3 bg-gray-50 rounded">
                <span className="text-gray-600">SC Households</span>
                <span className="font-semibold">{formatIndianNumber(metrics.households.sc)}</span>
              </div>
              <div className="flex justify-between items-center p-3 bg-gray-50 rounded">
                <span className="text-gray-600">ST Households</span>
                <span className="font-semibold">{formatIndianNumber(metrics.households.st)}</span>
              </div>
              <div className="flex justify-between items-center p-3 bg-gray-50 rounded">
                <span className="text-gray-600">Women Households</span>
                <span className="font-semibold">{formatIndianNumber(metrics.households.women)}</span>
              </div>
            </div>
          </div>

          {/* Financial Details */}
          <div>
            <h4 className="text-lg font-semibold text-gray-700 mb-3">
              Financial Details / वित्तीय विवरण
            </h4>
            <div className="space-y-2">
              <div className="flex justify-between items-center p-3 bg-gray-50 rounded">
                <span className="text-gray-600">Total Funds</span>
                <span className="font-semibold">{formatLargeCurrency(metrics.finances.total_funds)}</span>
              </div>
              <div className="flex justify-between items-center p-3 bg-gray-50 rounded">
                <span className="text-gray-600">Utilized</span>
                <span className="font-semibold">{formatLargeCurrency(metrics.finances.funds_utilized)}</span>
              </div>
              <div className="flex justify-between items-center p-3 bg-gray-50 rounded">
                <span className="text-gray-600">Material Cost</span>
                <span className="font-semibold">{formatLargeCurrency(metrics.finances.material_expenditure)}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default MetricsOverview;
