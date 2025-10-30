import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import '@/styles/globals.css';
import { Providers } from './providers';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'MGNREGA Dashboard - Track District Performance',
  description: 'View MGNREGA performance data for your district. Track employment, wages, and works completed in an easy-to-understand format.',
  keywords: 'MGNREGA, rural employment, India, district performance, employment guarantee',
  authors: [{ name: 'MGNREGA Dashboard Team' }],
  manifest: '/manifest.json',
  themeColor: '#2563eb',
  icons: {
    icon: '/favicon.ico',
    apple: '/apple-touch-icon.png',
  },
  openGraph: {
    type: 'website',
    locale: 'en_IN',
    url: 'https://mgnrega-dashboard.com',
    title: 'MGNREGA Dashboard - Track District Performance',
    description: 'View MGNREGA performance data for your district',
    siteName: 'MGNREGA Dashboard',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'MGNREGA Dashboard',
    description: 'View MGNREGA performance data for your district',
  },
};

export const viewport = {
  width: 'device-width',
  initialScale: 1,
  maximumScale: 1,
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className}>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
