"use client";

import React, { useState, useEffect } from "react";
import { Globe2, CheckCircle2, Clock, AlertTriangle, ShieldCheck, ArrowRight, Layers, FileCode } from "lucide-react";
import { RegionConfig } from "../lib/types";
import { fetchRegions } from "../lib/api";

export const CountryRegistry: React.FC = () => {
  const [regions, setRegions] = useState<RegionConfig[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [selectedRegion, setSelectedRegion] = useState<RegionConfig | null>(null);

  useEffect(() => {
    fetchRegions()
      .then((data) => {
        setRegions(data);
        if (data.length > 0) setSelectedRegion(data[0]);
      })
      .catch((err) => console.error("Error loading regions:", err))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
      <div className="mb-8">
        <div className="flex items-center space-x-2 text-violet-400 text-sm font-mono uppercase tracking-wider mb-2">
          <Globe2 className="w-4 h-4" />
          <span>Extensible Market Architecture</span>
        </div>
        <h2 className="text-2xl sm:text-3xl font-bold text-white tracking-tight">
          Country & Dataset Registry
        </h2>
        <p className="text-gray-400 text-sm mt-1">
          A modular, schema-driven configuration framework allowing international markets to be onboarded without platform refactoring.
        </p>
      </div>

      {/* Grid of Registered Countries */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
        {regions.map((reg) => {
          const isActive = reg.support_status === "ACTIVE";
          const isSelected = selectedRegion?.country_code === reg.country_code;

          return (
            <div
              key={reg.country_code}
              onClick={() => setSelectedRegion(reg)}
              className={`cursor-pointer glass-panel rounded-2xl p-6 border transition-all ${
                isSelected
                  ? "border-cyan-400 shadow-cyan-glow bg-surface-high/60"
                  : "border-white/10 hover:border-white/20"
              }`}
            >
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center space-x-3">
                  <div className="w-10 h-10 rounded-xl bg-surface-low border border-white/10 flex items-center justify-center font-bold font-mono text-base text-white">
                    {reg.country_code}
                  </div>
                  <div>
                    <h3 className="font-bold text-white text-base leading-snug">{reg.country_name}</h3>
                    <p className="text-xs text-gray-400 font-mono">{reg.region}</p>
                  </div>
                </div>

                <span
                  className={`text-[10px] font-mono px-2 py-0.5 rounded-full border uppercase ${
                    isActive
                      ? "bg-emerald-500/15 text-emerald-400 border-emerald-500/30"
                      : "bg-amber-500/15 text-amber-400 border-amber-500/30"
                  }`}
                >
                  {reg.support_status}
                </span>
              </div>

              <div className="space-y-2 text-xs font-mono">
                <div className="flex justify-between py-1 border-b border-white/5">
                  <span className="text-gray-400">Currency:</span>
                  <span className="text-white font-medium">{reg.currency_code} ({reg.currency_symbol})</span>
                </div>
                <div className="flex justify-between py-1 border-b border-white/5">
                  <span className="text-gray-400">Target Column:</span>
                  <span className="text-cyan-300 font-medium">{reg.target_column}</span>
                </div>
                <div className="flex justify-between py-1 border-b border-white/5">
                  <span className="text-gray-400">Feature Count:</span>
                  <span className="text-violet-300 font-medium">{reg.feature_schema.length} Features</span>
                </div>
              </div>

              <div className="mt-4 pt-3 border-t border-white/5 flex items-center justify-between text-xs text-gray-400">
                <span>{isActive ? "Inference Active" : "Prediction Disabled"}</span>
                <ArrowRight className="w-3.5 h-3.5 text-cyan-400" />
              </div>
            </div>
          );
        })}
      </div>

      {/* Selected Region Detailed Schema Inspector */}
      {selectedRegion && (
        <div className="glass-panel rounded-2xl border border-white/10 p-6 sm:p-8">
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between pb-6 border-b border-white/10 gap-4">
            <div>
              <div className="flex items-center space-x-2">
                <span className="text-xs font-mono uppercase tracking-wider text-cyan-400">Schema Contract Specification</span>
                <span className="text-xs px-2 py-0.5 rounded bg-white/5 font-mono text-gray-300">
                  {selectedRegion.dataset_id}
                </span>
              </div>
              <h3 className="text-xl font-bold text-white mt-1">
                {selectedRegion.country_name} — {selectedRegion.dataset_name}
              </h3>
              <p className="text-xs text-gray-400 mt-1">
                Source: {selectedRegion.dataset_source} | Target: {selectedRegion.target_definition} ({selectedRegion.target_unit})
              </p>
            </div>

            <div className="flex items-center space-x-2">
              {selectedRegion.support_status === "ACTIVE" ? (
                <div className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-mono">
                  <CheckCircle2 className="w-4 h-4" />
                  <span>Model Verified & Serving</span>
                </div>
              ) : (
                <div className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-amber-500/10 border border-amber-500/30 text-amber-400 text-xs font-mono">
                  <AlertTriangle className="w-4 h-4" />
                  <span>Future Integration (Unfitted)</span>
                </div>
              )}
            </div>
          </div>

          {/* Compatibility Notice */}
          <div className="my-6 p-4 rounded-xl bg-surface-low border border-white/5 text-xs text-gray-300 leading-relaxed">
            <span className="font-bold text-white block mb-1">Market Compatibility & Guardrails:</span>
            {selectedRegion.compatibility_notes}
          </div>

          {/* Feature Schema Table */}
          <h4 className="text-sm font-bold text-white mb-3">Feature Schema Definition</h4>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs font-mono">
              <thead className="bg-[#0E1321] border-b border-white/10 text-gray-400">
                <tr>
                  <th className="px-4 py-2.5">Feature Name</th>
                  <th className="px-4 py-2.5">Label</th>
                  <th className="px-4 py-2.5">Type</th>
                  <th className="px-4 py-2.5">Unit</th>
                  <th className="px-4 py-2.5">Description</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/5">
                {selectedRegion.feature_schema.map((feat) => (
                  <tr key={feat.name} className="hover:bg-white/[0.02]">
                    <td className="px-4 py-2.5 font-bold text-cyan-300">{feat.name}</td>
                    <td className="px-4 py-2.5 text-white">{feat.label}</td>
                    <td className="px-4 py-2.5 text-violet-400">{feat.type}</td>
                    <td className="px-4 py-2.5 text-gray-400">{feat.unit || "Categorical / N/A"}</td>
                    <td className="px-4 py-2.5 text-gray-300">{feat.description}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Onboarding Workflow Guide */}
          <div className="mt-8 pt-6 border-t border-white/10">
            <h4 className="text-sm font-bold text-white mb-3">Standard 10-Step Regional Dataset Onboarding Workflow</h4>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3 text-[11px] font-mono text-gray-400">
              <div className="p-3 rounded-lg bg-surface-low border border-white/5">
                <span className="text-cyan-400 font-bold block mb-1">01. Metadata</span>
                Register country JSON in config/regions/
              </div>
              <div className="p-3 rounded-lg bg-surface-low border border-white/5">
                <span className="text-cyan-400 font-bold block mb-1">02. Licensing</span>
                Validate source distribution license
              </div>
              <div className="p-3 rounded-lg bg-surface-low border border-white/5">
                <span className="text-cyan-400 font-bold block mb-1">03. Schema</span>
                Inspect columns and missingness
              </div>
              <div className="p-3 rounded-lg bg-surface-low border border-white/5">
                <span className="text-cyan-400 font-bold block mb-1">04. Features</span>
                Map compatible units & currencies
              </div>
              <div className="p-3 rounded-lg bg-surface-low border border-white/5">
                <span className="text-cyan-400 font-bold block mb-1">05. Target</span>
                Define valuation response variable
              </div>
              <div className="p-3 rounded-lg bg-surface-low border border-white/5">
                <span className="text-violet-400 font-bold block mb-1">06. Pipeline</span>
                Build PySpark VectorAssembler stages
              </div>
              <div className="p-3 rounded-lg bg-surface-low border border-white/5">
                <span className="text-violet-400 font-bold block mb-1">07. Train</span>
                Fit separate regional Spark MLlib model
              </div>
              <div className="p-3 rounded-lg bg-surface-low border border-white/5">
                <span className="text-violet-400 font-bold block mb-1">08. Evaluate</span>
                Verify test RMSE and R² baseline
              </div>
              <div className="p-3 rounded-lg bg-surface-low border border-white/5">
                <span className="text-emerald-400 font-bold block mb-1">09. Persist</span>
                Save PipelineModel to models/ directory
              </div>
              <div className="p-3 rounded-lg bg-surface-low border border-white/5">
                <span className="text-emerald-400 font-bold block mb-1">10. Enable</span>
                Activate ACTIVE status in API registry
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

