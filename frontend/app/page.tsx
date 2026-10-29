"use client";

import React, { useState, useEffect } from "react";
import { Header } from "../components/Header";
import { HeroSection } from "../components/HeroSection";
import { QuickEstimator } from "../components/QuickEstimator";
import { PerformanceDashboard } from "../components/PerformanceDashboard";
import { DatasetExplorer } from "../components/DatasetExplorer";
import { ScalabilityLab } from "../components/ScalabilityLab";
import { CountryRegistry } from "../components/CountryRegistry";
import { AboutMethodology } from "../components/AboutMethodology";
import { Footer } from "../components/Footer";
import { fetchHealth } from "../lib/api";

export default function Home() {
  const [activeTab, setActiveTab] = useState<string>("dashboard");
  const [sparkActive, setSparkActive] = useState<boolean>(true);

  useEffect(() => {
    fetchHealth()
      .then((data) => {
        setSparkActive(data.subsystems?.spark_runtime?.is_active ?? true);
      })
      .catch(() => {
        // Fallback gracefully
        setSparkActive(true);
      });
  }, []);

  return (
    <div className="min-h-screen flex flex-col bg-[#0A0F1D]">
      {/* Top Application Header */}
      <Header activeTab={activeTab} setActiveTab={setActiveTab} sparkActive={sparkActive} />

      {/* Main Screen Content */}
      <main className="flex-1">
        {activeTab === "dashboard" && (
          <div>
            <HeroSection
              onEstimateClick={() => setActiveTab("predict")}
              onExploreClick={() => setActiveTab("performance")}
            />
            <QuickEstimator />
            <PerformanceDashboard />
            <ScalabilityLab />
          </div>
        )}

        {activeTab === "predict" && <QuickEstimator />}

        {activeTab === "performance" && <PerformanceDashboard />}

        {activeTab === "explorer" && <DatasetExplorer />}

        {activeTab === "scalability" && <ScalabilityLab />}

        {activeTab === "registry" && <CountryRegistry />}

        {activeTab === "about" && <AboutMethodology />}
      </main>

      {/* Global Application Footer */}
      <Footer />
    </div>
  );
}

