import './globals.css'
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import Link from 'next/link'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'RA Tools Hub',
  description: 'Your central hub for accessing and managing various AI-powered tools and utilities.',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <nav className="bg-white shadow-sm">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between h-16">
              <div className="flex">
                <Link href="/" className="flex items-center">
                  <span className="text-xl font-bold text-gray-900">RA Tools Hub</span>
                </Link>
              </div>
              <div className="flex items-center space-x-4">
                <Link href="/resources" className="px-3 py-2 rounded-md bg-orange-100 text-orange-700 hover:bg-orange-200 font-medium transition-colors">
                  Resources
                </Link>
                <Link href="/my-upload-app" className="px-3 py-2 rounded-md bg-green-100 text-green-700 hover:bg-green-200 font-medium transition-colors">
                  Scoping Doc Builder
                </Link>
                <Link href="/rcm-builder" className="px-3 py-2 rounded-md bg-blue-100 text-blue-700 hover:bg-blue-200 font-medium transition-colors">
                  RCM Builder
                </Link>
                <Link href="/gap-builder" className="px-3 py-2 rounded-md bg-red-100 text-red-700 hover:bg-red-200 font-medium transition-colors">
                  Gap Builder
                </Link>
                <Link href="/rcm-testing" className="px-3 py-2 rounded-md bg-purple-100 text-purple-700 hover:bg-purple-200 font-medium transition-colors">
                  RCM Testing Generator
                </Link>
                <Link href="/rcm-converter" className="px-3 py-2 rounded-md bg-teal-100 text-teal-700 hover:bg-teal-200 font-medium transition-colors">
                  RCM Converter
                </Link>
              </div>
            </div>
          </div>
        </nav>
        {children}
      </body>
    </html>
  )
} 