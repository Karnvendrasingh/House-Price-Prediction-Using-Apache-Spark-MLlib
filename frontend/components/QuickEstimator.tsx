"use client";

import React, { useState } from "react";
import { Sparkles, RefreshCw, AlertCircle, CheckCircle2, TrendingUp, Clock, Info } from "lucide-react";
import { CaliforniaFeatures, PredictionResult } from "../lib/types";
import { predictHousing } from "../lib/api";

const PRESETS: Record<string, { label: string; values: CaliforniaFeatures; desc: string }> = {
  berkeley: {
    label: "Berkeley Hills Prime",
    desc: "Affluent residential hill district with high median income and mature housing stock.",
    values: {
      MedInc: 8.3252,
      HouseAge: 41.0,
      AveRooms: 6.9841,
      AveBedrms: 1.0238,
      Population: 322.0,
      AveOccup: 2.5555,
      Latitude: 37.88,
      Longitude: -122.23,
    },
  },
  silicon_valley: {
    label: "Silicon Valley Hub",
    desc: "High income technology corridor, modern houses, medium-high population density.",
    values: {
      MedInc: 10.45,
      HouseAge: 22.0,
      AveRooms: 7.15,
      AveBedrms: 1.05,
      Population: 1650.0,
      AveOccup: 2.75,
      Latitude: 37.38,
      Longitude: -122.08,
    },
  },
  socal_coastal: {
    label: "SoCal Coastal District",
    desc: "Los Angeles county coastal community with balanced household metrics.",
    values: {
      MedInc: 6.12,
      HouseAge: 32.0,
      AveRooms: 5.85,
      AveBedrms: 1.04,
      Population: 1350.0,
      AveOccup: 2.85,
      Latitude: 34.02,
      Longitude: -118.49,
    },
  },
  central_valley: {
    label: "Central Valley Rural",
    desc: "Inland agricultural district with modest income and higher household occupancy.",
    values: {
      MedInc: 2.85,
      HouseAge: 25.0,
      AveRooms: 4.95,
      AveBedrms: 1.02,
      Population: 2200.0,
      AveOccup: 3.65,
      Latitude: 36.74,
      Longitude: -119.78,
    },
  },
};

export const QuickEstimator: React.FC = () => {
  const [features, setFeatures] = useState<CaliforniaFeatures>(PRESETS.berkeley.values);
  const [selectedPreset, setSelectedPreset] = useState<string>("berkeley");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<PredictionResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleInputChange = (field: keyof CaliforniaFeatures, value: number) => {
    setFeatures((prev) => ({ ...prev, [field]: value }));
    setSelectedPreset("");
  };

  const handleSelectPreset = (key: string) => {
    setSelectedPreset(key);
    setFeatures(PRESETS[key].values);
  };

  const handlePredict = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const res = await predictHousing(features, "USA");
      setResult(res);
    } catch (err: any) {
      setError(err.message || "Failed to generate prediction. Check backend status.");
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    handleSelectPreset("berkeley");
    setResult(null);
    setError(null);
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
      <div className="mb-8">
        <div className="flex items-center space-x-2 text-cyan-400 text-sm font-mono uppercase tracking-wider mb-2">
          <Sparkles className="w-4 h-4" />
          <span>Interactive Valuation Engine</span>
        </div>
        <h2 className="text-2xl sm:text-3xl font-bold text-white tracking-tight">
          Property Value Estimation
        </h2>
        <p className="text-gray-400 text-sm mt-1">
          Predict district median property values using the trained PySpark MLlib Linear Regression pipeline.
        </p>
      </div>

      {/* Preset Buttons */}
      <div className="mb-6">
        <label className="text-xs font-mono text-gray-400 uppercase tracking-wider mb-2 block">
          Select Standard Regional Profile:
        </label>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
          {Object.entries(PRESETS).map(([key, item]) => (
            <button
              key={key}
              onClick={() => handleSelectPreset(key)}
              className={`px-3 py-2 rounded-lg text-xs font-medium text-left transition-all border ${
                selectedPreset === key
                  ? "bg-cyan-500/20 text-cyan-300 border-cyan-500/50 shadow-cyan-glow"
                  : "bg-surface-low text-gray-400 border-white/5 hover:border-white/10 hover:text-gray-200"
              }`}
            >
              <div className="font-semibold text-white truncate">{item.label}</div>
              <div className="text-[10px] text-gray-400 truncate mt-0.5">{item.desc}</div>
            </button>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Input Form Column (7 cols) */}
        <div className="lg:col-span-7 glass-panel rounded-2xl p-6 border border-white/10">
          <form onSubmit={handlePredict} className="space-y-4">
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {/* MedInc */}
              <div>
                <div className="flex justify-between items-center mb-1">
                  <label className="text-xs font-medium text-gray-300 flex items-center space-x-1">
                    <span>Median Income (MedInc)</span>
                    <Info className="w-3 h-3 text-gray-400" />
                  </label>
                  <span className="text-xs font-mono text-cyan-400">${(features.MedInc * 10000).toLocaleString('en-US')}/yr</span>
                </div>
                <input
                  type="number"
                  step="0.05"
                  value={features.MedInc}
                  onChange={(e) => handleInputChange("MedInc", parseFloat(e.target.value) || 0)}
                  className="w-full bg-[#0E1321] border border-white/10 rounded-lg px-3 py-2 text-sm text-white font-mono focus:outline-none focus:border-cyan-400"
                  required
                />
                <span className="text-[10px] text-gray-500">Expressed in $10,000 units (e.g., 8.32 = $83,200)</span>
              </div>

              {/* HouseAge */}
              <div>
                <div className="flex justify-between items-center mb-1">
                  <label className="text-xs font-medium text-gray-300">Median House Age</label>
                  <span className="text-xs font-mono text-cyan-400">{features.HouseAge} Years</span>
                </div>
                <input
                  type="number"
                  step="1"
                  value={features.HouseAge}
                  onChange={(e) => handleInputChange("HouseAge", parseFloat(e.target.value) || 0)}
                  className="w-full bg-[#0E1321] border border-white/10 rounded-lg px-3 py-2 text-sm text-white font-mono focus:outline-none focus:border-cyan-400"
                  required
                />
                <span className="text-[10px] text-gray-500">Median age of structures in census block</span>
              </div>

              {/* AveRooms */}
              <div>
                <div className="flex justify-between items-center mb-1">
                  <label className="text-xs font-medium text-gray-300">Average Rooms</label>
                  <span className="text-xs font-mono text-violet-400">{features.AveRooms} Rooms</span>
                </div>
                <input
                  type="number"
                  step="0.1"
                  value={features.AveRooms}
                  onChange={(e) => handleInputChange("AveRooms", parseFloat(e.target.value) || 0)}
                  className="w-full bg-[#0E1321] border border-white/10 rounded-lg px-3 py-2 text-sm text-white font-mono focus:outline-none focus:border-cyan-400"
                  required
                />
                <span className="text-[10px] text-gray-500">Average total rooms per household</span>
              </div>

              {/* AveBedrms */}
              <div>
                <div className="flex justify-between items-center mb-1">
                  <label className="text-xs font-medium text-gray-300">Average Bedrooms</label>
                  <span className="text-xs font-mono text-violet-400">{features.AveBedrms} Bedrms</span>
                </div>
                <input
                  type="number"
                  step="0.05"
                  value={features.AveBedrms}
                  onChange={(e) => handleInputChange("AveBedrms", parseFloat(e.target.value) || 0)}
                  className="w-full bg-[#0E1321] border border-white/10 rounded-lg px-3 py-2 text-sm text-white font-mono focus:outline-none focus:border-cyan-400"
                  required
                />
                <span className="text-[10px] text-gray-500">Average bedrooms per household</span>
              </div>

              {/* Population */}
              <div>
                <div className="flex justify-between items-center mb-1">
                  <label className="text-xs font-medium text-gray-300">Block Population</label>
                  <span className="text-xs font-mono text-emerald-400">{features.Population.toLocaleString('en-US')} Residents</span>
                </div>
                <input
                  type="number"
                  step="10"
                  value={features.Population}
                  onChange={(e) => handleInputChange("Population", parseFloat(e.target.value) || 0)}
                  className="w-full bg-[#0E1321] border border-white/10 rounded-lg px-3 py-2 text-sm text-white font-mono focus:outline-none focus:border-cyan-400"
                  required
                />
                <span className="text-[10px] text-gray-500">Total residents in the census block group</span>
              </div>

              {/* AveOccup */}
              <div>
                <div className="flex justify-between items-center mb-1">
                  <label className="text-xs font-medium text-gray-300">Average Occupants</label>
                  <span className="text-xs font-mono text-emerald-400">{features.AveOccup} People</span>
                </div>
                <input
                  type="number"
                  step="0.1"
                  value={features.AveOccup}
                  onChange={(e) => handleInputChange("AveOccup", parseFloat(e.target.value) || 0)}
                  className="w-full bg-[#0E1321] border border-white/10 rounded-lg px-3 py-2 text-sm text-white font-mono focus:outline-none focus:border-cyan-400"
                  required
                />
                <span className="text-[10px] text-gray-500">Average household members</span>
              </div>

              {/* Latitude */}
              <div>
                <div className="flex justify-between items-center mb-1">
                  <label className="text-xs font-medium text-gray-300">Latitude (°N)</label>
                  <span className="text-xs font-mono text-sky-400">{features.Latitude}° N</span>
                </div>
                <input
                  type="number"
                  step="0.01"
                  value={features.Latitude}
                  onChange={(e) => handleInputChange("Latitude", parseFloat(e.target.value) || 0)}
                  className="w-full bg-[#0E1321] border border-white/10 rounded-lg px-3 py-2 text-sm text-white font-mono focus:outline-none focus:border-cyan-400"
                  required
                />
                <span className="text-[10px] text-gray-500">California span: 32.54° to 41.95° N</span>
              </div>

              {/* Longitude */}
              <div>
                <div className="flex justify-between items-center mb-1">
                  <label className="text-xs font-medium text-gray-300">Longitude (°W)</label>
                  <span className="text-xs font-mono text-sky-400">{features.Longitude}° W</span>
                </div>
                <input
                  type="number"
                  step="0.01"
                  value={features.Longitude}
                  onChange={(e) => handleInputChange("Longitude", parseFloat(e.target.value) || 0)}
                  className="w-full bg-[#0E1321] border border-white/10 rounded-lg px-3 py-2 text-sm text-white font-mono focus:outline-none focus:border-cyan-400"
                  required
                />
                <span className="text-[10px] text-gray-500">California span: -124.35° to -114.31° W</span>
              </div>
            </div>

            {/* Form Actions */}
            <div className="flex items-center space-x-3 pt-4 border-t border-white/10">
              <button
                type="submit"
                disabled={loading}
                className="flex-1 flex items-center justify-center space-x-2 py-3 px-4 rounded-xl btn-primary-cyan text-white font-semibold text-sm disabled:opacity-50"
              >
                {loading ? (
                  <>
                    <RefreshCw className="w-4 h-4 animate-spin" />
                    <span>Executing Spark Inference...</span>
                  </>
                ) : (
                  <>
                    <Sparkles className="w-4 h-4" />
                    <span>Estimate Property Value</span>
                  </>
                )}
              </button>
              <button
                type="button"
                onClick={handleReset}
                className="py-3 px-4 rounded-xl glass-panel text-gray-400 hover:text-white text-sm"
              >
                Reset
              </button>
            </div>
          </form>
        </div>

        {/* Prediction Results Display (5 cols) */}
        <div className="lg:col-span-5 flex flex-col justify-between glass-panel rounded-2xl p-6 border border-white/10">
          <div>
            <div className="flex items-center justify-between pb-4 border-b border-white/10">
              <span className="text-xs font-mono text-gray-400 uppercase tracking-wider">Spark Inference Output</span>
              <span className="text-xs font-mono px-2 py-0.5 rounded bg-emerald-500/15 text-emerald-400 border border-emerald-500/30">
                PySpark MLlib
              </span>
            </div>

            {error ? (
              <div className="mt-6 p-4 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-300 text-xs flex items-start space-x-2">
                <AlertCircle className="w-5 h-5 flex-shrink-0 text-rose-400" />
                <div>
                  <p className="font-semibold mb-1">Inference Error</p>
                  <p>{error}</p>
                </div>
              </div>
            ) : result ? (
              <div className="mt-6 space-y-6">
                <div>
                  <span className="text-xs text-gray-400 uppercase font-mono tracking-wider">Estimated Median Value</span>
                  <div className="text-4xl sm:text-5xl font-extrabold font-mono text-gradient-cyan tracking-tight mt-1">
                    {result.formatted_usd}
                  </div>
                  <div className="flex items-center space-x-2 mt-2">
                    <span className="text-xs font-mono text-gray-400">Target Raw Value:</span>
                    <span className="text-xs font-mono text-cyan-300 font-bold">
                      {result.predicted_target_value.toFixed(4)} ($100k USD)
                    </span>
                  </div>
                </div>

                <div className="p-4 rounded-xl bg-surface-lowest border border-white/5 space-y-2">
                  <div className="flex justify-between text-xs">
                    <span className="text-gray-400">95% Confidence Interval:</span>
                    <span className="font-mono text-white font-medium">
                      {result.confidence_interval_95_usd.formatted}
                    </span>
                  </div>
                  <div className="flex justify-between text-xs">
                    <span className="text-gray-400">Inference Latency:</span>
                    <span className="font-mono text-emerald-400">
                      {result.execution_metadata.inference_latency_ms.toFixed(2)} ms
                    </span>
                  </div>
                  <div className="flex justify-between text-xs">
                    <span className="text-gray-400">Spark Master:</span>
                    <span className="font-mono text-violet-300">
                      {result.execution_metadata.spark_master}
                    </span>
                  </div>
                </div>

                <div className="p-3 rounded-lg bg-cyan-500/5 border border-cyan-500/20 text-[11px] text-gray-400 flex items-start space-x-2">
                  <Info className="w-4 h-4 text-cyan-400 flex-shrink-0 mt-0.5" />
                  <span>{result.disclaimer}</span>
                </div>
              </div>
            ) : (
              <div className="mt-12 text-center py-10">
                <div className="w-16 h-16 mx-auto mb-4 rounded-2xl bg-white/5 border border-white/10 flex items-center justify-center text-cyan-400">
                  <TrendingUp className="w-8 h-8 opacity-60" />
                </div>
                <h4 className="text-base font-semibold text-white">Ready for Inference</h4>
                <p className="text-xs text-gray-400 max-w-xs mx-auto mt-1">
                  Adjust features on the left or select a preset, then click &ldquo;Estimate Property Value&rdquo; to execute the PySpark regression pipeline.
                </p>
              </div>
            )}
          </div>

          <div className="pt-4 border-t border-white/10 text-[11px] font-mono text-gray-500 flex justify-between items-center">
            <span>Model: California MLlib LR v1.0</span>
            <span>20,640 Training Observations</span>
          </div>
        </div>
      </div>
    </div>
  );
};

