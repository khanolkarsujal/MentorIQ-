import { useNavigate } from "react-router";
import { ArrowLeft, Sparkles, Star, Users } from "lucide-react";

export default function Community() {
  const navigate = useNavigate();

  const stories = [
    { name: "Alex Chen", text: "Guided mentorship changed my life. I'm now a senior dev at Google.", initials: "AC", bg: "bg-blue-500" },
    { name: "Maya Rodriguez", text: "The community support is unreal. I never feel alone anymore.", initials: "MR", bg: "bg-purple-500" },
    { name: "Jordan Kim", text: "Finally understood architecture with real-world examples.", initials: "JK", bg: "bg-emerald-500" }
  ];

  return (
    <div className="size-full min-h-screen overflow-y-auto bg-[#F0FDFA] p-6 lg:p-12 pb-24">
      <button
        onClick={() => navigate('/results')}
        className="fixed top-6 left-6 bg-white p-3 rounded-full shadow-lg hover:shadow-xl transition-all focus:scale-110 z-20 border border-teal-100"
      >
        <ArrowLeft className="w-6 h-6 text-teal-900" />
      </button>

      <div className="max-w-[1200px] mx-auto space-y-12">
        {/* Simple Community Hero */}
        <div className="relative rounded-[3.5rem] overflow-hidden shadow-2xl h-[450px]">
          <img 
            src="/flowers.jpg" 
            alt="Flower hills" 
            className="w-full h-full object-cover"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-white/60 via-transparent to-transparent flex flex-col justify-end p-12">
            <h1 className="text-4xl md:text-7xl font-black text-[#1E293B] mb-2 tracking-tighter">Join Our Community</h1>
            <p className="text-xl md:text-2xl text-[#475569] font-medium max-w-xl leading-relaxed">A supportive place for developers to grow together.</p>
          </div>
        </div>

        {/* Simple Global Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
          {[["Members", "5,000+"], ["Mentors", "500+"], ["Sessions", "15k+"], ["Success", "98%"]].map(([l, v], i) => (
            <div key={i} className="premium-card p-10 text-center hover:scale-105 transition-transform">
              <p className="text-3xl font-black text-teal-600 mb-2">{v}</p>
              <p className="text-sm font-black text-gray-400 uppercase tracking-widest">{l}</p>
            </div>
          ))}
        </div>

        {/* Stories Section */}
        <div className="space-y-12 py-6">
          <div className="flex items-center justify-center gap-4">
            <div className="bg-[#F97316] p-4 rounded-2xl shadow-lg">
              <Sparkles className="w-8 h-8 text-white" />
            </div>
            <h2 className="text-4xl md:text-5xl font-black text-[#1E293B]">Success Stories</h2>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {stories.map((story, i) => (
              <div key={i} className="premium-card p-12 text-center group hover:bg-[#F8FAFC] transition-colors">
                <div className={`${story.bg} w-16 h-16 rounded-full flex items-center justify-center text-white text-xl font-black mx-auto mb-8 shadow-lg group-hover:scale-110 transition-transform`}>
                  {story.initials}
                </div>
                <h4 className="text-2xl font-black text-[#1E293B] mb-6">{story.name}</h4>
                <p className="text-[#64748B] text-lg font-medium leading-relaxed italic">"{story.text}"</p>
              </div>
            ))}
          </div>
        </div>

        {/* Final CTA */}
        <div className="text-center pt-8">
          <button 
            onClick={() => navigate('/results')}
            className="premium-button bg-[#1E293B] text-white px-16 py-6 text-xl shadow-2xl hover:bg-[#0F172A]"
          >
            Start Your Journey Today
          </button>
        </div>
      </div>
    </div>
  );
}
