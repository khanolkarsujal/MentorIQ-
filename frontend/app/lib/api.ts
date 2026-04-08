/// <reference types="vite/client" />
const rawUrl = (import.meta as any).env.VITE_API_URL || "http://localhost:8000";
// Professional sanitization: Remove any trailing slashes to prevent double-slash errors in fetches
const BASE_URL = rawUrl.replace(/\/+$/, "");

export interface AnalysisResult {
  status: string;
  username: string;
  avatar_url: string;
  maturity_score: number;
  subscores: Record<string, number>;
  profile_career_level: string;
  code_quality_label: string;
  project_job_readiness: string;
  activity_level: string;
  total_contributions: number;
  active_weeks: number;
  activity_overview: string;
  oss_pr_count: number;
  oss_repos: string[];
  open_source_contributions: string;
  technologies_used: string[];
  top_3_repos: string[];
  strengths: string[];
  skill_gaps: string[];
  insights: string;
  mentor_match: string;
  matched_mentor: {
    name: string;
    job_title: string;
    bio: string;
    skills: string[];
  } | null;
}

export async function analyzeProfile(username: string): Promise<AnalysisResult> {
  // We ensure the slash is exactly where it should be
  const res = await fetch(`${BASE_URL}/api/analyze?username=${encodeURIComponent(username)}`);
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Unknown error" }));
    throw new Error(err.detail || `HTTP ${res.status}`);
  }
  return res.json();
}
