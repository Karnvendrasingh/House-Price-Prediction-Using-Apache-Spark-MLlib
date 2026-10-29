"use client";

import React, { useState, useEffect } from "react";
import { Database, ChevronLeft, ChevronRight, ArrowUpDown, ExternalLink, RefreshCw, Info, CheckCircle2 } from "lucide-react";
import { DatasetSummary } from "../lib/types";
import { fetchDatasetSummary, fetchDatasetPreview } from "../lib/api";

export const DatasetExplorer: React.FC = () => {
  const [summary, setSummary] = useState<DatasetSummary | null>(null);
  const [previewData, setPreviewData] = useState<any[]>([]);
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(15);
  const [totalPages, setTotalPages] = useState(1);
  const [totalRecords, setTotalRecords] = useState(0);
  const [sortBy, setSortBy] = useState<string | undefined>("MedInc");
  const [sortDesc, setSortDesc] = useState(true);
  const [loading, setLoading] = useState(true);
  const [activeSubTab, setActiveSubTab] = useState<"table" | "stats" | "correlation">("table");

  const loadData = async () => {
    setLoading(true);
    try {
      const sum = await fetchDatasetSummary();
      setSummary(sum);

      const prev = await fetchDatasetPreview("usa_california", page, pageSize, sortBy, sortDesc);
      setPreviewData(prev.records);
      setTotalPages(prev.total_pages);
      setTotalRecords(prev.total_records);
    } catch (err) {
      console.error("Failed to load dataset explorer data:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [page, pageSize, sortBy, sortDesc]);

  const handleSort = (col: string) => {
    if (sortBy === col) {
      setSortDesc(!sortDesc);
    } else {
      setSortBy(col);
      setSortDesc(true);
    }
    setPage(1);
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-8 gap-4">
        <div>
          <div className="flex items-center space-x-2 text-cyan-400 text-sm font-mono uppercase tracking-wider mb-2">
            <Database className="w-4 h-4" />
            <span>Distributed Data Layer</span>
          </div>
          <h2 className="text-2xl sm:text-3xl font-bold text-white tracking-tight">
            California Housing Dataset Explorer
          </h2>
          <p className="text-gray-400 text-sm mt-1">
            20,640 census block group observations across 8 numerical features and median target values.
          </p>
        </div>

        <a
          href="https://scikit-learn.org/stable/datasets/real_world.html#california-housing-dataset"
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center space-x-1.5 px-3.5 py-2 rounded-xl glass-panel text-xs text-cyan-300 hover:text-white border border-cyan-500/30"
        >
          <span>Official Scikit-Learn Documentation</span>
          <ExternalLink className="w-3.5 h-3.5" />
        </a>
      </div>

      {/* Sub-tab Switcher */}
      <div className="flex space-x-2 mb-6 border-b border-white/10 pb-3">
        <button
          onClick={() => setActiveSubTab("table")}
          className={`px-4 py-2 rounded-lg text-xs font-mono font-medium transition-all ${
            activeSubTab === "table"
              ? "bg-cyan-500/20 text-cyan-300 border border-cyan-500/40"
              : "text-gray-400 hover:text-white"
          }`}
        >
          Observation Browser ({totalRecords.toLocaleString()} Rows)
        </button>
        <button
          onClick={() => setActiveSubTab("stats")}
          className={`px-4 py-2 rounded-lg text-xs font-mono font-medium transition-all ${
            activeSubTab === "stats"
              ? "bg-cyan-500/20 text-cyan-300 border border-cyan-500/40"
              : "text-gray-400 hover:text-white"
          }`}
        >
          Descriptive Statistics
        </button>
        <button
          onClick={() => setActiveSubTab("correlation")}
          className={`px-4 py-2 rounded-lg text-xs font-mono font-medium transition-all ${
            activeSubTab === "correlation"
              ? "bg-cyan-500/20 text-cyan-300 border border-cyan-500/40"
              : "text-gray-400 hover:text-white"
          }`}
        >
          Feature Correlation Matrix
        </button>
      </div>

      {/* Sub-tab 1: Paginated Table */}
      {activeSubTab === "table" && (
        <div className="glass-panel rounded-2xl border border-white/10 overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs font-mono">
              <thead className="bg-[#0E1321] border-b border-white/10 text-gray-400">
                <tr>
                  {[
                    "MedInc",
                    "HouseAge",
                    "AveRooms",
                    "AveBedrms",
                    "Population",
                    "AveOccup",
                    "Latitude",
                    "Longitude",
                    "MedHouseVal",
                    "EstimatedUSD",
                  ].map((col) => (
                    <th
                      key={col}
                      onClick={() => handleSort(col)}
                      className="px-4 py-3 cursor-pointer hover:text-cyan-400 transition-colors whitespace-nowrap"
                    >
                      <div className="flex items-center space-x-1">
                        <span>{col}</span>
                        <ArrowUpDown className="w-3 h-3 opacity-60" />
                      </div>
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody className="divide-y divide-white/5">
                {loading ? (
                  <tr>
                    <td colSpan={10} className="py-12 text-center text-gray-500">
                      <RefreshCw className="w-5 h-5 animate-spin mx-auto mb-2 text-cyan-400" />
                      Loading partitioned records from Spark / backend cache...
                    </td>
                  </tr>
                ) : (
                  previewData.map((row, idx) => (
                    <tr key={idx} className="hover:bg-white/[0.02] transition-colors">
                      <td className="px-4 py-2.5 font-semibold text-cyan-300">{row.MedInc?.toFixed(4)}</td>
                      <td className="px-4 py-2.5 text-gray-300">{row.HouseAge}</td>
                      <td className="px-4 py-2.5 text-gray-300">{row.AveRooms?.toFixed(2)}</td>
                      <td className="px-4 py-2.5 text-gray-300">{row.AveBedrms?.toFixed(2)}</td>
                      <td className="px-4 py-2.5 text-gray-300">{row.Population?.toLocaleString()}</td>
                      <td className="px-4 py-2.5 text-gray-300">{row.AveOccup?.toFixed(2)}</td>
                      <td className="px-4 py-2.5 text-sky-400">{row.Latitude?.toFixed(2)}°</td>
                      <td className="px-4 py-2.5 text-sky-400">{row.Longitude?.toFixed(2)}°</td>
                      <td className="px-4 py-2.5 font-bold text-violet-300">${row.MedHouseVal?.toFixed(4)}</td>
                      <td className="px-4 py-2.5 font-bold text-emerald-400">${row.EstimatedUSD?.toLocaleString()}</td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>

          {/* Pagination Controls */}
          <div className="px-4 py-3 bg-[#0E1321] border-t border-white/10 flex flex-col sm:flex-row items-center justify-between gap-3 text-xs font-mono text-gray-400">
            <div>
              Showing page <span className="text-white font-bold">{page}</span> of{" "}
              <span className="text-white font-bold">{totalPages}</span> ({totalRecords.toLocaleString()} total rows)
            </div>
            <div className="flex items-center space-x-2">
              <button
                onClick={() => setPage(Math.max(1, page - 1))}
                disabled={page <= 1}
                className="p-1.5 rounded-lg glass-panel text-gray-300 hover:text-white disabled:opacity-40"
              >
                <ChevronLeft className="w-4 h-4" />
              </button>
              <button
                onClick={() => setPage(Math.min(totalPages, page + 1))}
                disabled={page >= totalPages}
                className="p-1.5 rounded-lg glass-panel text-gray-300 hover:text-white disabled:opacity-40"
              >
                <ChevronRight className="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Sub-tab 2: Descriptive Statistics */}
      {activeSubTab === "stats" && summary && (
        <div className="glass-panel rounded-2xl border border-white/10 p-6 overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs font-mono">
              <thead className="bg-[#0E1321] border-b border-white/10 text-gray-400">
                <tr>
                  <th className="px-4 py-3">Feature Column</th>
                  <th className="px-4 py-3">Count</th>
                  <th className="px-4 py-3">Mean</th>
                  <th className="px-4 py-3">Std Dev</th>
                  <th className="px-4 py-3">Min</th>
                  <th className="px-4 py-3">25% (Q1)</th>
                  <th className="px-4 py-3">50% (Median)</th>
                  <th className="px-4 py-3">75% (Q3)</th>
                  <th className="px-4 py-3">Max</th>
                  <th className="px-4 py-3">Missing</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/5">
                {Object.entries(summary.statistics).map(([feat, s]) => (
                  <tr key={feat} className="hover:bg-white/[0.02]">
                    <td className="px-4 py-3 font-bold text-white">{feat}</td>
                    <td className="px-4 py-3 text-gray-400">{s.count.toLocaleString()}</td>
                    <td className="px-4 py-3 text-cyan-300 font-semibold">{s.mean.toFixed(2)}</td>
                    <td className="px-4 py-3 text-gray-300">{s.std.toFixed(2)}</td>
                    <td className="px-4 py-3 text-gray-400">{s.min.toFixed(2)}</td>
                    <td className="px-4 py-3 text-gray-400">{s.p25.toFixed(2)}</td>
                    <td className="px-4 py-3 text-violet-300 font-semibold">{s.p50_median.toFixed(2)}</td>
                    <td className="px-4 py-3 text-gray-400">{s.p75.toFixed(2)}</td>
                    <td className="px-4 py-3 text-gray-400">{s.max.toFixed(2)}</td>
                    <td className="px-4 py-3 text-emerald-400 flex items-center space-x-1">
                      <CheckCircle2 className="w-3.5 h-3.5" />
                      <span>0 (0%)</span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Sub-tab 3: Pearson Correlation Heatmap */}
      {activeSubTab === "correlation" && summary && (
        <div className="glass-panel rounded-2xl border border-white/10 p-6 overflow-hidden">
          <h3 className="text-base font-bold text-white mb-2">Pearson Correlation Coefficients</h3>
          <p className="text-xs text-gray-400 font-mono mb-6">
            Bivariate linear correlation values ranging from -1.0 (inverse correlation) to +1.0 (direct correlation).
          </p>

          <div className="overflow-x-auto">
            <table className="w-full text-center text-xs font-mono">
              <thead>
                <tr className="border-b border-white/10 text-gray-400">
                  <th className="text-left px-3 py-2">Feature</th>
                  {Object.keys(summary.full_correlation_matrix).map((c) => (
                    <th key={c} className="px-2 py-2 text-[11px] truncate max-w-[80px]">
                      {c}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody className="divide-y divide-white/5">
                {Object.entries(summary.full_correlation_matrix).map(([rowKey, rowVals]) => (
                  <tr key={rowKey}>
                    <td className="text-left px-3 py-2 font-bold text-white whitespace-nowrap">
                      {rowKey}
                    </td>
                    {Object.entries(rowVals).map(([colKey, val]) => {
                      const numVal = typeof val === "number" ? val : 0;
                      // Color cell based on correlation strength
                      let bgClass = "bg-transparent";
                      if (numVal === 1) bgClass = "bg-cyan-500/25 text-cyan-200 font-bold";
                      else if (numVal > 0.4) bgClass = "bg-cyan-500/20 text-cyan-300";
                      else if (numVal > 0.1) bgClass = "bg-cyan-500/10 text-cyan-400";
                      else if (numVal < -0.4) bgClass = "bg-rose-500/20 text-rose-300";
                      else if (numVal < -0.1) bgClass = "bg-rose-500/10 text-rose-400";

                      return (
                        <td key={colKey} className={`px-2 py-2 rounded text-[11px] ${bgClass}`}>
                          {numVal.toFixed(2)}
                        </td>
                      );
                    })}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};

