"use client";

import React from "react";
import { Sparkles, BarChart3, Database, Cpu, ArrowRight } from "lucide-react";

interface HeroSectionProps {
  onEstimateClick: () => void;
  onExploreClick: () => void;
}

export const HeroSection: React.FC<HeroSectionProps> = ({ onEstimateClick, onExploreClick }) => {
  return (
    <div className="relative overflow-hidden pt-10 pb-12 sm:pb-16 border-b border-white/5">
      {/* Background Radial Glows */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[700px] h-[350px] bg-gradient-to-b from-cyan-600/15 via-violet-600/10 to-transparent blur-3xl pointer-events-none" />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <div className="text-center max-w-3xl mx-auto">
          {/* Badge */}
          <div className="inline-flex items-center space-x-2 px-3.5 py-1.5 rounded-full bg-cyan-500/10 border border-cyan-500/30 mb-6">
            <span className="w-2 h-2 rounded-full bg-cyan-400 animate-pulse"></span>
            <span className="text-xs font-mono font-medium tracking-wide text-cyan-300 uppercase">
              Apache Spark MLlib — Distributed Regression Platform
            </span>
          </div>

          {/* Headline */}
          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight text-white mb-6 leading-tight">
            Scalable Real Estate Valuation Powered by{" "}
            <span className="text-gradient-cyan">Apache Spark</span>
          </h1>

          {/* Subtitle */}
          <p className="text-base sm:text-lg text-gray-300 mb-8 leading-relaxed">
            A high-throughput distributed regression platform trained on California census spatial data.
            Engineered with PySpark pipelines, VectorAssembler feature scaling, and future-ready
            international dataset support.
          </p>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-12">
            <button
              onClick={onEstimateClick}
              className="w-full sm:w-auto flex items-center justify-center space-x-2 px-7 py-3.5 rounded-xl btn-primary-cyan text-white font-semibold text-sm"
            >
              <Sparkles className="w-4 h-4" />
              <span>Estimate Property Value</span>
              <ArrowRight className="w-4 h-4 ml-1" />
            </button>

            <button
              onClick={onExploreClick}
              className="w-full sm:w-auto flex items-center justify-center space-x-2 px-6 py-3.5 rounded-xl glass-panel text-gray-300 hover:text-white font-medium text-sm glass-panel-hover"
            >
              <BarChart3 className="w-4 h-4 text-cyan-400" />
              <span>Explore Analytics & Benchmarks</span>
            </button>
          </div>

          {/* Quick Metrics KPI Bar */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 max-w-4xl mx-auto text-left">
            <div className="glass-panel p-4 rounded-xl border border-white/5">
              <div className="flex items-center space-x-2 text-cyan-400 mb-1">
                <Database className="w-4 h-4" />
                <span className="text-xs font-mono uppercase tracking-wider text-gray-400">Records</span>
              </div>
              <p className="text-xl font-bold font-mono text-white">20,640</p>
              <p className="text-[11px] text-gray-400">California Census Blocks</p>
            </div>

            <div className="glass-panel p-4 rounded-xl border border-white/5">
              <div className="flex items-center space-x-2 text-violet-400 mb-1">
                <BarChart3 className="w-4 h-4" />
                <span className="text-xs font-mono uppercase tracking-wider text-gray-400">Features</span>
              </div>
              <p className="text-xl font-bold font-mono text-white">8 Features</p>
              <p className="text-[11px] text-gray-400">VectorAssembler Scaled</p>
            </div>

            <div className="glass-panel p-4 rounded-xl border border-white/5">
              <div className="flex items-center space-x-2 text-emerald-400 mb-1">
                <Cpu className="w-4 h-4" />
                <span className="text-xs font-mono uppercase tracking-wider text-gray-400">Cluster</span>
              </div>
              <p className="text-xl font-bold font-mono text-white">Local[*]</p>
              <p className="text-[11px] text-gray-400">Multi-threaded RDDs</p>
            </div>

            <div className="glass-panel p-4 rounded-xl border border-white/5">
              <div className="flex items-center space-x-2 text-sky-400 mb-1">
                <Sparkles className="w-4 h-4" />
                <span className="text-xs font-mono uppercase tracking-wider text-gray-400">Model</span>
              </div>
              <p className="text-xl font-bold font-mono text-white">LinearRegression</p>
              <p className="text-[11px] text-gray-400">Spark ML Pipeline</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

