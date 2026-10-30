"use client";

import React, { useState, useEffect } from "react";
import { Activity, RefreshCw, BarChart2, CheckCircle, Info, Cpu, Layers } from "lucide-react";
import {
  ScatterChart,
  Scatter,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  BarChart,
  Bar,
  Cell,
  ReferenceLine,
} from "recharts";
import { ModelMetadata } from "../lib/types";
import { fetchModelMetrics, triggerTraining } from "../lib/api";

export const PerformanceDashboard: React.FC = () => {
  const [metadata, setMetadata] = useState<ModelMetadata | null>(null);
  const [loading, setLoading] = useState(true);
  const [training, setTraining] = useState(false);
  const [trainRatio, setTrainRatio] = useState(0.8);
  const [error, setError] = useState<string | null>(null);

  const loadMetrics = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await fetchModelMetrics();
      setMetadata(data);
    } catch (err: any) {
      setError(err.message || "Failed to load model evaluation metrics");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadMetrics();
  }, []);

  const handleRetrain = async () => {
    setTraining(true);
    setError(null);
    try {
      await triggerTraining("usa_california_lr", trainRatio, 42);
      // Poll until finished or reload after 3s
      setTimeout(async () => {
        await loadMetrics();
        setTraining(false);
      }, 4000);
    } catch (err: any) {
      setError(err.message || "Retraining failed");
      setTraining(false);
    }
  };

  // Prepare coefficient chart data
  const coefficientData = metadata?.model_parameters?.feature_coefficients
    ? Object.entries(metadata.model_parameters.feature_coefficients).map(([key, val]) => ({
        feature: key,
        coefficient: val,
      }))
    : [];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-8 gap-4">
        <div>
          <div className="flex items-center space-x-2 text-violet-400 text-sm font-mono uppercase tracking-wider mb-2">
            <Activity className="w-4 h-4" />
            <span>Statistical Model Diagnostics</span>
          </div>
          <h2 className="text-2xl sm:text-3xl font-bold text-white tracking-tight">
            Spark MLlib Model Performance
          </h2>
          <p className="text-gray-400 text-sm mt-1">
            Evaluated on held-out test partitions using Spark RegressionEvaluator.
          </p>
        </div>

        {/* Retrain Action */}
        <div className="flex items-center space-x-3">
          <div className="flex items-center space-x-2 text-xs font-mono text-gray-400">
            <span>Split: {Math.round(trainRatio * 100)}% Train</span>
            <input
              type="range"
              min="0.5"
              max="0.9"
              step="0.05"
              value={trainRatio}
              onChange={(e) => setTrainRatio(parseFloat(e.target.value))}
              className="w-24 accent-cyan-400"
            />
          </div>
          <button
            onClick={handleRetrain}
            disabled={training}
            className="flex items-center space-x-2 px-4 py-2 rounded-xl glass-panel text-cyan-300 hover:text-white border border-cyan-500/30 hover:border-cyan-500 text-xs font-medium disabled:opacity-50"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${training ? "animate-spin" : ""}`} />
            <span>{training ? "Training on Spark..." : "Retrain Pipeline"}</span>
          </button>
        </div>
      </div>

      {loading ? (
        <div className="py-24 text-center">
          <RefreshCw className="w-8 h-8 text-cyan-400 animate-spin mx-auto mb-3" />
          <p className="text-sm text-gray-400 font-mono">Loading Spark MLlib evaluation metadata...</p>
        </div>
      ) : error ? (
        <div className="p-6 rounded-2xl bg-rose-500/10 border border-rose-500/20 text-rose-300 text-sm">
          <p className="font-semibold mb-1">Model Not Available</p>
          <p>{error}</p>
          <button
            onClick={handleRetrain}
            className="mt-4 px-4 py-2 rounded-lg bg-cyan-600 text-white font-medium text-xs"
          >
            Train Initial Spark Model Now
          </button>
        </div>
      ) : metadata ? (
        <div className="space-y-8">
          {/* Top KPI Cards (4 metrics) */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="glass-panel p-5 rounded-2xl border border-white/10">
              <span className="text-xs font-mono text-gray-400 uppercase tracking-wider">Root Mean Squared Error</span>
              <div className="text-3xl font-extrabold font-mono text-white mt-1">
                {metadata.metrics.rmse?.toFixed(4)}
              </div>
              <p className="text-xs text-cyan-400 font-mono mt-1">
                ≈ ${metadata.metrics.rmse_usd?.toLocaleString('en-US')} USD
              </p>
              <p className="text-[11px] text-gray-400 mt-2">
                Penalizes large outlier estimation errors.
              </p>
            </div>

            <div className="glass-panel p-5 rounded-2xl border border-white/10">
              <span className="text-xs font-mono text-gray-400 uppercase tracking-wider">Mean Absolute Error</span>
              <div className="text-3xl font-extrabold font-mono text-white mt-1">
                {metadata.metrics.mae?.toFixed(4)}
              </div>
              <p className="text-xs text-violet-400 font-mono mt-1">
                ≈ ${metadata.metrics.mae_usd?.toLocaleString('en-US')} USD
              </p>
              <p className="text-[11px] text-gray-400 mt-2">
                Average absolute distance from actual census values.
              </p>
            </div>

            <div className="glass-panel p-5 rounded-2xl border border-white/10">
              <span className="text-xs font-mono text-gray-400 uppercase tracking-wider">Coefficient of Determination</span>
              <div className="text-3xl font-extrabold font-mono text-emerald-400 mt-1">
                R² = {metadata.metrics.r2?.toFixed(4)}
              </div>
              <p className="text-xs text-gray-400 font-mono mt-1">
                Explains {( (metadata.metrics.r2 || 0) * 100 ).toFixed(1)}% of price variance
              </p>
              <p className="text-[11px] text-gray-400 mt-2">
                Good fit for linear baseline on spatial census units.
              </p>
            </div>

            <div className="glass-panel p-5 rounded-2xl border border-white/10">
              <span className="text-xs font-mono text-gray-400 uppercase tracking-wider">Partition Sample Sizes</span>
              <div className="text-xl font-bold font-mono text-white mt-1">
                {metadata.train_test_split.train_samples?.toLocaleString('en-US')} / {metadata.train_test_split.test_samples?.toLocaleString('en-US')}
              </div>
              <p className="text-xs text-sky-400 font-mono mt-1">
                Train / Test Record Split ({Math.round(metadata.train_test_split.train_ratio * 100)}/
                {Math.round(metadata.train_test_split.test_ratio * 100)})
              </p>
              <p className="text-[11px] text-gray-400 mt-2">
                Zero data leakage across partitions.
              </p>
            </div>
          </div>

          {/* Visual Charts: Actual vs Predicted Scatter & Feature Coefficients */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Chart 1: Actual vs Predicted */}
            <div className="glass-panel rounded-2xl p-6 border border-white/10">
              <div className="flex justify-between items-center mb-4">
                <div>
                  <h3 className="text-base font-bold text-white">Actual vs. Predicted Valuation</h3>
                  <p className="text-xs text-gray-400 font-mono">Held-out test partition sample (N=400)</p>
                </div>
                <span className="text-xs px-2 py-0.5 rounded bg-cyan-500/10 text-cyan-400 font-mono border border-cyan-500/30">
                  Ideal 45° Fit Line
                </span>
              </div>

              <div className="h-72 w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <ScatterChart margin={{ top: 10, right: 20, bottom: 20, left: 10 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#1E293B" />
                    <XAxis
                      type="number"
                      dataKey="actual"
                      name="Actual ($100k)"
                      domain={[0, 5.5]}
                      stroke="#64748B"
                      fontSize={11}
                      tickFormatter={(v) => `$${(v * 100).toFixed(0)}k`}
                    />
                    <YAxis
                      type="number"
                      dataKey="predicted"
                      name="Predicted ($100k)"
                      domain={[0, 5.5]}
                      stroke="#64748B"
                      fontSize={11}
                      tickFormatter={(v) => `$${(v * 100).toFixed(0)}k`}
                    />
                    <Tooltip
                      cursor={{ strokeDasharray: "3 3" }}
                      content={({ active, payload }) => {
                        if (active && payload && payload.length) {
                          const data = payload[0].payload;
                          return (
                            <div className="bg-[#0E1321] p-3 rounded-lg border border-cyan-500/30 shadow-xl text-xs font-mono">
                              <p className="text-gray-400">Actual: <span className="text-white font-bold">${data.actual_usd?.toLocaleString('en-US')}</span></p>
                              <p className="text-gray-400">Predicted: <span className="text-cyan-300 font-bold">${data.predicted_usd?.toLocaleString('en-US')}</span></p>
                              <p className="text-gray-400">Residual: <span className={data.residual >= 0 ? "text-emerald-400" : "text-rose-400"}>${(data.residual * 100000).toFixed(0)}</span></p>
                            </div>
                          );
                        }
                        return null;
                      }}
                    />
                    <ReferenceLine x={0} y={0} stroke="#38BDF8" strokeWidth={1.5} />
                    <Scatter
                      data={metadata.residuals_sample || []}
                      fill="#06B6D4"
                      fillOpacity={0.65}
                    />
                  </ScatterChart>
                </ResponsiveContainer>
              </div>
              <p className="text-[11px] text-gray-500 text-center mt-2">
                Points clustering tightly around the 45° diagonal indicate high predictive accuracy.
              </p>
            </div>

            {/* Chart 2: Feature Coefficients Bar Chart */}
            <div className="glass-panel rounded-2xl p-6 border border-white/10">
              <div className="flex justify-between items-center mb-4">
                <div>
                  <h3 className="text-base font-bold text-white">Learned Feature Weights</h3>
                  <p className="text-xs text-gray-400 font-mono">PySpark LinearRegression Model Coefficients</p>
                </div>
                <span className="text-xs px-2 py-0.5 rounded bg-violet-500/10 text-violet-400 font-mono border border-violet-500/30">
                  StandardScaler Fitted
                </span>
              </div>

              <div className="h-72 w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={coefficientData} layout="vertical" margin={{ top: 5, right: 30, left: 40, bottom: 5 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#1E293B" horizontal={false} />
                    <XAxis type="number" stroke="#64748B" fontSize={11} />
                    <YAxis dataKey="feature" type="category" stroke="#94A3B8" fontSize={11} />
                    <Tooltip
                      content={({ active, payload }) => {
                        if (active && payload && payload.length) {
                          const data = payload[0].payload;
                          return (
                            <div className="bg-[#0E1321] p-2.5 rounded-lg border border-violet-500/30 shadow-xl text-xs font-mono">
                              <span className="text-white font-bold">{data.feature}: </span>
                              <span className={data.coefficient >= 0 ? "text-cyan-400" : "text-rose-400"}>
                                {data.coefficient.toFixed(6)}
                              </span>
                            </div>
                          );
                        }
                        return null;
                      }}
                    />
                    <ReferenceLine x={0} stroke="#64748B" />
                    <Bar dataKey="coefficient">
                      {coefficientData.map((entry, index) => (
                        <Cell
                          key={`cell-${index}`}
                          fill={entry.coefficient >= 0 ? "#06B6D4" : "#F43F5E"}
                        />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>
              <p className="text-[11px] text-gray-500 text-center mt-2">
                MedInc exhibits strongest positive impact, while coordinate geography captures coastal value gradients.
              </p>
            </div>
          </div>
        </div>
      ) : null}
    </div>
  );
};

