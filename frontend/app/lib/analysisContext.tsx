import { createContext, useContext, useState, ReactNode } from "react";
import type { AnalysisResult } from "./api";

interface AnalysisState {
  username: string;
  setUsername: (u: string) => void;
  result: AnalysisResult | null;
  setResult: (r: AnalysisResult | null) => void;
  error: string | null;
  setError: (e: string | null) => void;
}

const AnalysisContext = createContext<AnalysisState | null>(null);

export function AnalysisProvider({ children }: { children: ReactNode }) {
  const [username, setUsername] = useState("");
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  return (
    <AnalysisContext.Provider value={{ username, setUsername, result, setResult, error, setError }}>
      {children}
    </AnalysisContext.Provider>
  );
}

export function useAnalysis() {
  const ctx = useContext(AnalysisContext);
  if (!ctx) throw new Error("useAnalysis must be used within AnalysisProvider");
  return ctx;
}
