import { useNavigate } from "react-router";
import { ArrowLeft, Star, TrendingUp, Users, Sparkles, AlertCircle, Zap, Code2, GitBranch, Activity } from "lucide-react";
import { useAnalysis } from "../lib/analysisContext";

export default function Results() {
  const navigate = useNavigate();
  const { result, error, username } = useAnalysis();

  // Error state
  if (error) {
    return (
      <div className="size-full min-h-screen flex items-center justify-center bg-gradient-to-br from-[#1A0B2E] via-[#3B0764] to-[#701A75] p-6">
        <div className="premium-card max-w-lg w-full text-center flex flex-col items-center gap-8 p-16">
          <AlertCircle className="w-20 h-20 text-red-400" />
          <h1 className="text-3xl font-black text-[#1E293B]">Analysis Failed</h1>
          <p className="text-lg text-[#64748B] font-medium">{error}</p>
          <button
            onClick={() => navigate('/github-username')}
            className="premium-button bg-[#7C3AED] text-white text-lg"
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  // No data yet
  if (!result) {
    return (
      <div className="size-full min-h-screen flex items-center justify-center bg-gradient-to-br from-[#1A0B2E] via-[#3B0764] to-[#701A75] p-6">
        <div className="premium-card max-w-lg w-full text-center flex flex-col items-center gap-8 p-16">
          <h1 className="text-3xl font-black text-[#1E293B]">No Results Found</h1>
          <p className="text-lg text-[#64748B]">Please analyze a GitHub profile first.</p>
          <button
            onClick={() => navigate('/github-username')}
            className="premium-button bg-[#7C3AED] text-white text-lg"
          >
            Analyze Profile
          </button>
        </div>
      </div>
    );
  }

  const scoreColor = result.maturity_score >= 7.5 ? "#10B981" : result.maturity_score >= 5.0 ? "#F59E0B" : "#EF4444";

  return (
    <div className="size-full min-h-screen overflow-y-auto bg-gradient-to-br from-[#1A0B2E] via-[#3B0764] to-[#701A75] pb-20">
      <button
        onClick={() => navigate('/github-username')}
        className="fixed top-6 left-6 bg-white/20 backdrop-blur-md p-3 rounded-full shadow-lg hover:bg-white/30 transition-all hover:scale-110 z-20 border border-white/20"
      >
        <ArrowLeft className="w-6 h-6 text-white" />
      </button>

      <div className="max-w-[1200px] mx-auto px-6 pt-16 space-y-10">

        {/* Hero profile card */}
        <div className="premium-card p-10 flex flex-col md:flex-row items-center gap-10">
          <img
            src={result.avatar_url}
            alt={result.username}
            className="w-32 h-32 rounded-full border-4 border-[#7C3AED] shadow-xl object-cover"
          />
          <div className="flex-1 text-center md:text-left">
            <h1 className="text-4xl md:text-5xl font-black text-[#1E293B]">@{result.username}</h1>
            <p className="text-lg text-[#64748B] font-medium mt-2">{result.profile_career_level} · {result.code_quality_label}</p>
            <div className="flex flex-wrap gap-3 mt-4 justify-center md:justify-start">
              {result.technologies_used.slice(0, 8).map((tech, i) => (
                <span key={i} className="px-4 py-1.5 rounded-full text-sm font-bold bg-[#7C3AED]/10 text-[#7C3AED] border border-[#7C3AED]/20">
                  {tech}
                </span>
              ))}
            </div>
          </div>
          {/* Maturity Score */}
          <div className="flex flex-col items-center gap-2">
            <div
              className="w-28 h-28 rounded-full flex items-center justify-center text-5xl font-black border-4 shadow-xl"
              style={{ borderColor: scoreColor, color: scoreColor, backgroundColor: `${scoreColor}15` }}
            >
              {result.maturity_score}
            </div>
            <span className="text-sm font-bold text-[#64748B] uppercase tracking-widest">Maturity Score</span>
          </div>
        </div>

        {/* Stats row */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
          {[
            { icon: <Activity className="w-6 h-6" />, label: "Activity Level", value: result.activity_level, color: "#10B981" },
            { icon: <GitBranch className="w-6 h-6" />, label: "Contributions/yr", value: result.total_contributions.toLocaleString(), color: "#3B82F6" },
            { icon: <Code2 className="w-6 h-6" />, label: "Active Weeks", value: result.active_weeks, color: "#F59E0B" },
            { icon: <Zap className="w-6 h-6" />, label: "OSS PRs", value: result.oss_pr_count, color: "#D946EF" },
          ].map((stat, i) => (
            <div key={i} className="premium-card p-8 flex flex-col items-center gap-3 transition-transform hover:-translate-y-1">
              <div className="w-12 h-12 rounded-2xl flex items-center justify-center shadow-md" style={{ backgroundColor: `${stat.color}20`, color: stat.color }}>
                {stat.icon}
              </div>
              <p className="text-3xl font-black text-[#1E293B]">{stat.value}</p>
              <p className="text-sm font-bold text-[#64748B] uppercase tracking-wide text-center">{stat.label}</p>
            </div>
          ))}
        </div>

        {/* Strengths + Skill Gaps */}
        <div className="grid md:grid-cols-2 gap-8">
          <div className="premium-card p-10">
            <div className="flex items-center gap-3 mb-6">
              <div className="bg-[#10B981] w-12 h-12 rounded-2xl flex items-center justify-center shadow-md">
                <Star className="w-6 h-6 text-white" />
              </div>
              <h2 className="text-2xl font-black text-[#1E293B]">Strengths</h2>
            </div>
            <ul className="space-y-3">
              {(result.strengths.length ? result.strengths : ["No strengths data"]).map((s, i) => (
                <li key={i} className="flex items-start gap-3 text-[#64748B] font-semibold text-base">
                  <span className="text-[#10B981] mt-0.5 flex-shrink-0">✦</span> {s}
                </li>
              ))}
            </ul>
          </div>

          <div className="premium-card p-10">
            <div className="flex items-center gap-3 mb-6">
              <div className="bg-[#F59E0B] w-12 h-12 rounded-2xl flex items-center justify-center shadow-md">
                <TrendingUp className="w-6 h-6 text-white" />
              </div>
              <h2 className="text-2xl font-black text-[#1E293B]">Skill Gaps to Fill</h2>
            </div>
            <ul className="space-y-3">
              {(result.skill_gaps.length ? result.skill_gaps : ["No skill gaps identified"]).map((g, i) => (
                <li key={i} className="flex items-start gap-3 text-[#64748B] font-semibold text-base">
                  <span className="text-[#F59E0B] mt-0.5 flex-shrink-0">→</span> {g}
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Top repos + AI Insights */}
        <div className="grid md:grid-cols-2 gap-8">
          <div className="premium-card p-10">
            <h2 className="text-2xl font-black text-[#1E293B] mb-6">🏆 Top Repositories</h2>
            <ul className="space-y-4">
              {result.top_3_repos.map((repo, i) => (
                <li key={i}>
                  <a
                    href={`https://github.com/${result.username}/${repo}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center gap-3 text-[#7C3AED] font-bold text-lg hover:underline underline-offset-4"
                  >
                    <GitBranch className="w-5 h-5 flex-shrink-0" /> {repo}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          <div className="premium-card p-10">
            <div className="flex items-center gap-3 mb-6">
              <Sparkles className="w-7 h-7 text-[#FB923C] animate-pulse" />
              <h2 className="text-2xl font-black text-[#1E293B]">AI Insights</h2>
            </div>
            <p className="text-[#64748B] font-medium leading-relaxed text-base">
              {result.insights || "No additional insights available."}
            </p>
          </div>
        </div>

        {/* Matched Mentor */}
        {result.matched_mentor && (
          <div className="premium-card p-0 overflow-hidden border-0">
            <div className="grid md:grid-cols-2">
              <div className="p-12 md:p-16 flex flex-col justify-center gap-6">
                <div className="flex items-center gap-3">
                  <Users className="w-8 h-8 text-[#7C3AED]" />
                  <h2 className="text-3xl font-black text-[#1E293B]">Your Mentor Match</h2>
                </div>
                <div>
                  <p className="text-2xl font-black text-[#1E293B]">{result.matched_mentor.name}</p>
                  <p className="text-lg font-bold text-[#7C3AED] mt-1">{result.matched_mentor.job_title}</p>
                  <p className="text-[#64748B] font-medium mt-4 leading-relaxed">{result.matched_mentor.bio}</p>
                </div>
                <div className="flex flex-wrap gap-2">
                  {result.matched_mentor.skills?.map((skill, i) => (
                    <span key={i} className="px-3 py-1 rounded-full text-sm font-bold bg-[#7C3AED]/10 text-[#7C3AED] border border-[#7C3AED]/20">
                      {skill}
                    </span>
                  ))}
                </div>
                <button
                  onClick={() => navigate('/community')}
                  className="premium-button bg-gradient-to-r from-[#8B5CF6] to-[#DB2777] text-white text-lg w-fit"
                >
                  Meet Your Mentor →
                </button>
              </div>
              <div className="bg-gradient-to-br from-[#7C3AED]/10 to-[#DB2777]/10 flex items-center justify-center p-12">
                <img
                  src="/knights.jpg"
                  alt="Mentor community"
                  className="w-full max-w-sm hover:scale-105 transition-transform duration-700 rounded-3xl"
                />
              </div>
            </div>
          </div>
        )}

        {/* No mentor fallback */}
        {!result.matched_mentor && (
          <div className="premium-card p-10 text-center">
            <h2 className="text-2xl font-black text-[#1E293B] mb-4">Join Our Mentor Community</h2>
            <p className="text-[#64748B] mb-6">Connect with expert mentors who match your stack and goals.</p>
            <button
              onClick={() => navigate('/community')}
              className="premium-button bg-gradient-to-r from-[#8B5CF6] to-[#DB2777] text-white text-lg"
            >
              Explore Community
            </button>
          </div>
        )}

      </div>
    </div>
  );
}