import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
// import 'bootstrap/dist/css/bootstrap.min.css';
import "./globals.css";
import NavBar from "@/components/NavBar";
import "bootstrap/dist/css/bootstrap.min.css";
import type { AppProps } from "next/app";
import Footer from "@/components/Footer";
import 'bootstrap/dist/css/bootstrap.min.css';

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Create Next App",
  description: "Generated by create next app",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const links = [
    { name: "Modules", path: "/modules" },
  ];

  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <NavBar app_name="My App" links={links} />
          {children}
        <Footer />
      </body>
    </html>
  );
}
