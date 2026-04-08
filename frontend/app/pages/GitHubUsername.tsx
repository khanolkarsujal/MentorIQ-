import { useState } from "react";
import { useNavigate } from "react-router";
import { useAnalysis } from "../lib/analysisContext";

export default function GitHubUsername() {
  const navigate = useNavigate();
  const [inputValue, setInputValue] = useState("");
  const { setUsername, setResult, setError } = useAnalysis();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const trimmed = inputValue.trim();
    if (trimmed) {
      setUsername(trimmed);
      setResult(null);
      setError(null);
      navigate('/loading');
    }
  };

  return (
    <div className="size-full min-h-screen flex items-center justify-center bg-[#FFF8E7] p-6 lg:bg-[#EADDFF]">
      <div className="premium-card max-w-[650px] w-full text-center flex flex-col items-center gap-10">
        <div className="w-full overflow-hidden rounded-[2.5rem]">
          <img 
            src="/github.jpg" 
            alt="GitHub Illustration" 
            className="w-full object-cover shadow-inner hover:scale-105 transition-transform duration-700" 
          />
        </div>
        
        <div className="space-y-4">
          <h1 className="text-4xl md:text-5xl font-black text-[#1E293B]">
            Start Your Journey
          </h1>
          <p className="text-xl text-[#64748B] font-medium max-w-md mx-auto leading-relaxed">
            Enter your GitHub username to unlock your personalized analysis.
          </p>
        </div>
        
        <form onSubmit={handleSubmit} className="w-full max-w-sm space-y-6">
          <input
            type="text"
            placeholder="e.g. g-lin001"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            className="w-full px-8 py-5 rounded-2xl bg-white border-2 border-[#FCD34D] text-[#1E293B] text-xl font-bold focus:outline-none focus:ring-4 focus:ring-amber-200 transition-all text-center"
            required
          />
          <button 
            type="submit"
            className="premium-button bg-[#FB923C] text-white text-xl w-full"
          >
            Connect Account
          </button>
        </form>
      </div>
    </div>
  );
}