import { useNavigate } from "react-router";

export default function HowWeHelp() {
  const navigate = useNavigate();

  return (
    <div className="size-full min-h-screen flex items-center justify-center bg-[#FFF8E7] p-6 lg:bg-[#EADDFF]">
      <div className="premium-card max-w-[700px] w-full text-center flex flex-col items-center gap-10">
        <div className="w-full overflow-hidden rounded-[2.5rem]">
          <img 
            src="/howwehelp.jpg" 
            alt="How We Help Illustration" 
            className="w-full object-cover shadow-inner hover:scale-105 transition-transform duration-700 hover:rotate-2" 
          />
        </div>
        
        <div className="space-y-4">
          <h1 className="text-4xl md:text-5xl font-black text-[#1E293B]">
            Bridge The Skill Gap
          </h1>
          <p className="text-xl text-[#64748B] font-medium max-w-lg mx-auto leading-relaxed">
            Our app analyzes your GitHub to find your strengths and recommends the perfect path to mastery.
          </p>
        </div>
        
        <button 
          onClick={() => navigate('/github-username')}
          className="premium-button bg-gradient-to-r from-[#10B981] to-[#3B82F6] text-white text-xl"
        >
          Next Step
        </button>
      </div>
    </div>
  );
}