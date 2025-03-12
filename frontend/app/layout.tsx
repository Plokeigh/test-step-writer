import './globals.css'
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import Link from 'next/link'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Tools Hub',
  description: 'Your central hub for accessing and managing various tools and utilities.',
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
                  <span className="text-xl font-bold text-gray-900">Tools Hub</span>
                </Link>
              </div>
              <div className="flex items-center space-x-4">
                <Link href="/rcm-builder" className="text-gray-600 hover:text-gray-900">
                  RCM Builder
                </Link>
                <Link href="/my-upload-app" className="text-gray-600 hover:text-gray-900">
                  Upload App
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