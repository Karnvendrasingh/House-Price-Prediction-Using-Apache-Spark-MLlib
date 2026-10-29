"use client";

import React from "react";
import { Sparkles, ExternalLink, Github, Heart } from "lucide-react";

export const Footer: React.FC = () => {
  return (
    <footer className="border-t border-white/10 bg-[#090E1C] py-8 mt-16 text-xs font-mono text-gray-500">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="flex items-center space-x-2">
          <Sparkles className="w-4 h-4 text-cyan-400" />
          <span className="text-gray-300 font-bold">GlobalEstate AI</span>
          <span>— INT315 Cluster Computing Project</span>
        </div>

        <div className="flex items-center space-x-6">
          <span className="text-gray-400">Apache Spark 3.5.3 MLlib</span>
          <span>•</span>
          <span className="text-gray-400">FastAPI</span>
          <span>•</span>
          <span className="text-gray-400">Next.js 14</span>
          <span>•</span>
          <a
            href="http://localhost:4040"
            target="_blank"
            rel="noopener noreferrer"
            className="text-cyan-400 hover:underline flex items-center space-x-1"
          >
            <span>Spark Web UI (:4040)</span>
            <ExternalLink className="w-3 h-3" />
          </a>
        </div>

        <div>
          <span>Lovely Professional University</span>
        </div>
      </div>
    </footer>
  );
};

