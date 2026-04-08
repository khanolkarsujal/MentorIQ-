import { useNavigate } from "react-router";
import { ArrowLeft, Trophy, BookOpen, Code, TrendingUp } from "lucide-react";

export default function Journey() {
  const navigate = useNavigate();

  const roadmap = [
    { week: "Week 1-2", task: "Testing Mastery", status: "Done" },
    { week: "Week 3-4", task: "System Design", status: "Done" },
    { week: "Week 5-6", task: "Cloud Scaling", status: "Next" },
    { week: "Week 7-8", task: "Engineering Ethics", status: "Wait" }
  ];

  return (
    <div className="size-full min-h-screen overflow-y-auto bg-[#FFFBEB] p-6 lg:p-12 pb-24">
      <button
        onClick={() => navigate('/results')}
        className="fixed top-6 left-6 bg-white p-3 rounded-full shadow-lg hover:shadow-xl transition-all focus:scale-110 z-20 border border-amber-100"
      >
        <ArrowLeft className="w-6 h-6 text-amber-900" />
      </button>

      <div className="max-w-[1100px] mx-auto space-y-12">
        {/* Simple Journey Hero */}
        <div className="relative rounded-[3.5rem] overflow-hidden shadow-2xl h-[400px]">
          <img 
            src="/journey_hero.jpg" 
            alt="Journey Hero" 
            className="w-full h-full object-cover"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-black/70 to-transparent flex flex-col justify-end p-12">
            <h1 className="text-5xl md:text-6xl font-black text-white">Your Learning Path</h1>
            <p className="text-xl text-white/90 font-medium">Follow your curated roadmap to mastery.</p>
          </div>
        </div>

        <div className="grid lg:grid-cols-[1fr_2fr] gap-12 items-start">
          {/* Simple Stats Card */}
          <div className="premium-card p-12 bg-white space-y-12 border-4 border-amber-100">
            <div className="flex items-center gap-4">
              <div className="bg-[#A855F7] p-4 rounded-2xl shadow-lg">
                <Trophy className="w-8 h-8 text-white" />
              </div>
              <h2 className="text-3xl font-black text-gray-900 leading-none">Your Progress</h2>
            </div>
            <div className="space-y-6">
              {[["Sessions", "12"], ["Hours", "24"], ["Skills", "8"]].map(([l, v], i) => (
                <div key={i} className="flex justify-between items-center group">
                  <span className="text-gray-500 font-bold text-lg group-hover:text-gray-900 transition-colors uppercase tracking-widest">{l}</span>
                  <span className="text-3xl font-black text-purple-600 group-hover:scale-110 transition-transform">{v}</span>
                </div>
              ))}
            </div>
            <div className="pt-8 border-t border-amber-50">
              <div className="flex items-center gap-2 text-emerald-600 font-black text-lg mb-2">
                <TrendingUp className="w-6 h-6" />
                <span>On Track!</span>
              </div>
              <p className="text-gray-500 font-medium">You're 25% ahead of your goal.</p>
            </div>
          </div>

          {/* Simple Timeline Card */}
          <div className="premium-card p-12 bg-white space-y-12">
            <div className="flex items-center gap-4">
              <div className="bg-[#10B981] p-4 rounded-2xl shadow-lg">
                <BookOpen className="w-8 h-8 text-white" />
              </div>
              <h2 className="text-3xl font-black text-gray-900 leading-none">The Roadmap</h2>
            </div>
            <div className="space-y-8">
              {roadmap.map((item, i) => (
                <div key={i} className={`flex items-center gap-8 p-10 rounded-[2.5rem] border transition-all ${
                  item.status === "Done" ? 'bg-emerald-50 border-emerald-100' : 'bg-gray-50 border-gray-100'
                }`}>
                  <div className={`w-14 h-14 rounded-full flex items-center justify-center font-black text-2xl shadow-sm ${
                    item.status === "Done" ? 'bg-emerald-500 text-white shadow-emerald-100' : 'bg-white text-gray-300'
                  }`}>
                    {item.status === "Done" ? "✓" : i + 1}
                  </div>
                  <div className="flex-1">
                    <p className={`text-xs font-black uppercase tracking-widest mb-1 ${
                      item.status === "Done" ? 'text-emerald-500' : 'text-gray-400'
                    }`}>{item.week}</p>
                    <h4 className={`text-2xl font-black ${
                      item.status === "Done" ? 'text-emerald-900' : 'text-gray-700'
                    }`}>{item.task}</h4>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
