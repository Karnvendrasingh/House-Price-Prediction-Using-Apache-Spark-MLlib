import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "GlobalEstate AI — Scalable Real Estate Price Prediction Platform",
  description:
    "Distributed geospatial property valuation engine powered by Apache Spark MLlib & PySpark.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="bg-[#0A0F1D] text-[#DEE2F6] antialiased min-h-screen selection:bg-cyan-500/20 selection:text-cyan-300">
        {children}
      </body>
    </html>
  );
}

