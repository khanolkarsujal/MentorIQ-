import { useEffect, useState } from "react";
import { useNavigate } from "react-router";
import { Loader2 } from "lucide-react";
import { useAnalysis } from "../lib/analysisContext";
import { analyzeProfile } from "../lib/api";

export default function Loading() {
  const navigate = useNavigate();
  const [dots, setDots] = useState("");
  const [statusMsg, setStatusMsg] = useState("Fetching GitHub data");
  const { username, setResult, setError } = useAnalysis();

  useEffect(() => {
    // Animate dots
    const dotInterval = setInterval(() => {
      setDots(prev => prev.length >= 3 ? "" : prev + ".");
    }, 500);

    // Cycle status messages for UX feedback
    const messages = [
      "Fetching GitHub data",
      "Analyzing repositories",
      "Running AI audit",
      "Matching mentors",
      "Finalizing results",
    ];
    let msgIdx = 0;
    const msgInterval = setInterval(() => {
      msgIdx = (msgIdx + 1) % messages.length;
      setStatusMsg(messages[msgIdx]);
    }, 2000);

    // If username is missing (e.g. direct navigation), go back
    if (!username) {
      navigate('/github-username');
      return;
    }

    // Call the real backend
    analyzeProfile(username)
      .then((data) => {
        setResult(data);
        navigate('/results');
      })
      .catch((err: Error) => {
        setError(err.message || "Analysis failed. Please try again.");
        navigate('/results');
      });

    return () => {
      clearInterval(dotInterval);
      clearInterval(msgInterval);
    };
  }, [username, navigate, setResult, setError]);

  return (
    <div className="size-full min-h-screen flex items-center justify-center bg-[#F3F4F6] p-6 lg:bg-[#EADDFF]">
      <div className="premium-card max-w-[650px] w-full text-center flex flex-col items-center gap-10">
        <div className="w-full overflow-hidden rounded-[2.5rem]">
          <img 
            src="/loading.jpg" 
            alt="Loading Illustration" 
            className="w-full object-cover shadow-inner hover:scale-105 transition-transform duration-700" 
          />
        </div>
        
        <div className="space-y-4">
          <h1 className="text-4xl md:text-5xl font-black text-[#1E293B]">
            Analyzing Profile{dots}
          </h1>
          <p className="text-xl text-[#64748B] font-medium max-w-sm mx-auto leading-relaxed">
            {statusMsg} for <span className="font-bold text-[#7C3AED]">@{username}</span>
          </p>
        </div>
        
        <div className="flex items-center justify-center gap-4 py-4">
          <Loader2 className="w-10 h-10 text-[#3B82F6] animate-spin" />
        </div>
      </div>
    </div>
  );
}