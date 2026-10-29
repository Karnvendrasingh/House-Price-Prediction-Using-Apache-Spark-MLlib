"use client";

import React from "react";
import { BookOpen, Cpu, Database, Award, ShieldAlert, GitBranch, Layers, CheckCircle } from "lucide-react";

export const AboutMethodology: React.FC = () => {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-10">
      <div>
        <div className="flex items-center space-x-2 text-cyan-400 text-sm font-mono uppercase tracking-wider mb-2">
          <BookOpen className="w-4 h-4" />
          <span>INT315 Academic Report & Viva Reference</span>
        </div>
        <h2 className="text-2xl sm:text-3xl font-bold text-white tracking-tight">
          System Architecture & Methodology
        </h2>
        <p className="text-gray-400 text-sm mt-1">
          Technical specifications for course INT315: Cluster Computing project evaluation.
        </p>
      </div>

      {/* Grid: Problem Statement & Objectives */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="glass-panel rounded-2xl p-6 sm:p-8 border border-white/10">
          <h3 className="text-lg font-bold text-white mb-3 flex items-center space-x-2">
            <Cpu className="w-5 h-5 text-cyan-400" />
            <span>Problem Statement & Motivation</span>
          </h3>
          <div className="space-y-3 text-sm text-gray-300 leading-relaxed">
            <p>
              Traditional property valuation systems rely on centralized single-node analytics (Scikit-Learn, Pandas).
              As spatial datasets scale to millions of sensor readings and historical property transfers, centralized
              in-memory computing encounters severe vertical bottlenecks and out-of-memory (OOM) failures.
            </p>
            <p>
              Estimating property value is fundamentally a continuous supervised regression problem. Apache Spark MLlib
              solves vertical scaling constraints by partitioning geospatial DataFrames across worker nodes and computing
              gradient vectors and cost functions in parallel via distributed Stochastic Gradient Descent (SGD) and L-BFGS.
            </p>
          </div>
        </div>

        <div className="glass-panel rounded-2xl p-6 sm:p-8 border border-white/10">
          <h3 className="text-lg font-bold text-white mb-3 flex items-center space-x-2">
            <Award className="w-5 h-5 text-violet-400" />
            <span>Core Project Objectives</span>
          </h3>
          <ul className="space-y-2 text-xs font-mono text-gray-300">
            <li className="flex items-start space-x-2">
              <CheckCircle className="w-4 h-4 text-emerald-400 flex-shrink-0 mt-0.5" />
              <span><b>Resilient SparkSession:</b> Local multi-threaded cluster simulation with Catalyst query engine.</span>
            </li>
            <li className="flex items-start space-x-2">
              <CheckCircle className="w-4 h-4 text-emerald-400 flex-shrink-0 mt-0.5" />
              <span><b>Distributed Ingestion:</b> 20,640 census records ingested with verified DoubleType schema.</span>
            </li>
            <li className="flex items-start space-x-2">
              <CheckCircle className="w-4 h-4 text-emerald-400 flex-shrink-0 mt-0.5" />
              <span><b>Feature Pipeline:</b> VectorAssembler and StandardScaler stages without data leakage.</span>
            </li>
            <li className="flex items-start space-x-2">
              <CheckCircle className="w-4 h-4 text-emerald-400 flex-shrink-0 mt-0.5" />
              <span><b>MLlib LinearRegression:</b> Distributed continuous model training with persistent artifacts.</span>
            </li>
            <li className="flex items-start space-x-2">
              <CheckCircle className="w-4 h-4 text-emerald-400 flex-shrink-0 mt-0.5" />
              <span><b>Empirical Scalability:</b> Partition benchmarking across 25%, 50%, and 100% subsets.</span>
            </li>
            <li className="flex items-start space-x-2">
              <CheckCircle className="w-4 h-4 text-emerald-400 flex-shrink-0 mt-0.5" />
              <span><b>Multi-Country Registry:</b> Extensible schema-first configuration preventing invalid cross-country inference.</span>
            </li>
          </ul>
        </div>
      </div>

      {/* Spark Architecture & Pipeline Diagram Card */}
      <div className="glass-panel rounded-2xl p-6 sm:p-8 border border-white/10">
        <h3 className="text-lg font-bold text-white mb-4 flex items-center space-x-2">
          <Layers className="w-5 h-5 text-sky-400" />
          <span>Apache Spark Machine Learning Pipeline Flow</span>
        </h3>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 text-xs font-mono">
          <div className="p-4 rounded-xl bg-surface-low border border-white/5 space-y-2">
            <span className="text-cyan-400 font-bold block">1. Ingestion & RDD Partitioning</span>
            <p className="text-gray-400">
              CSV data ingested into Spark DataFrame with explicit StructType schema. Partitions distributed across local worker threads.
            </p>
          </div>

          <div className="p-4 rounded-xl bg-surface-low border border-white/5 space-y-2">
            <span className="text-cyan-400 font-bold block">2. VectorAssembler</span>
            <p className="text-gray-400">
              Combines 8 feature columns (MedInc, HouseAge, AveRooms, AveBedrms, Population, AveOccup, Lat, Long) into a single DenseVector.
            </p>
          </div>

          <div className="p-4 rounded-xl bg-surface-low border border-white/5 space-y-2">
            <span className="text-violet-400 font-bold block">3. StandardScaler</span>
            <p className="text-gray-400">
              Scales feature vectors to zero mean and unit variance across partitions to ensure balanced gradient descent convergence.
            </p>
          </div>

          <div className="p-4 rounded-xl bg-surface-low border border-white/5 space-y-2">
            <span className="text-emerald-400 font-bold block">4. MLlib LinearRegression</span>
            <p className="text-gray-400">
              Fits weights for MedHouseVal target. Evaluated on test partition with RegressionEvaluator (RMSE, MAE, R²).
            </p>
          </div>
        </div>
      </div>

      {/* Scientific Limitations & Guardrails */}
      <div className="glass-panel rounded-2xl p-6 sm:p-8 border border-white/10">
        <h3 className="text-lg font-bold text-white mb-3 flex items-center space-x-2">
          <ShieldAlert className="w-5 h-5 text-amber-400" />
          <span>Scientific Limitations & Academic Guardrails</span>
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 text-sm text-gray-300 leading-relaxed">
          <div>
            <h4 className="font-semibold text-white mb-1">Census Block Aggregates vs Individual Parcels</h4>
            <p className="text-xs text-gray-400">
              The California Housing dataset represents median aggregates across census block groups (averaging 600 to 3,000 residents).
              Predictions represent district housing price levels rather than an appraisal of a single property parcel.
            </p>
          </div>

          <div>
            <h4 className="font-semibold text-white mb-1">Single-Node vs Multi-Node Scaling</h4>
            <p className="text-xs text-gray-400">
              In this INT315 demonstration, Spark executes in <code className="text-cyan-300">local[*]</code> mode across CPU cores.
              While this benchmarks Spark&apos;s parallel partition scheduling and Catalyst optimizations, multi-node network shuffle scaling
              requires physical distributed cluster worker daemons.
            </p>
          </div>
        </div>
      </div>

      {/* References */}
      <div className="glass-panel rounded-2xl p-6 border border-white/10">
        <h4 className="text-sm font-bold text-white mb-3 font-mono">Academic References & Citations</h4>
        <ol className="list-decimal list-inside space-y-1.5 text-xs text-gray-400 font-mono">
          <li>Pace, R. Kelley, and Ronald Barry. &ldquo;Sparse spatial autoregressions.&rdquo; <i>Statistics &amp; Probability Letters</i> 33.3 (1997): 291-297.</li>
          <li>Zaharia, Matei, et al. &ldquo;Apache Spark: a unified engine for big data processing.&rdquo; <i>Communications of the ACM</i> 59.11 (2016): 56-65.</li>
          <li>Meng, Xiangrui, et al. &ldquo;MLlib: Machine learning in Apache Spark.&rdquo; <i>Journal of Machine Learning Research</i> 17.34 (2016): 1-7.</li>
          <li>INT315 – Cluster Computing Curriculum, School of Computer Science &amp; Engineering, Lovely Professional University (2025–2026).</li>
        </ol>
      </div>
    </div>
  );
};

