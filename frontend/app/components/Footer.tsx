import { Hexagon, Github, Twitter, Linkedin, ShieldCheck, Mail } from "lucide-react";

export default function Footer() {
  return (
    <footer className="bg-[#1E293B] text-white pt-24 pb-12 border-t border-white/5">
      <div className="max-w-[1400px] mx-auto px-6">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-16 mb-20">
          {/* Logo & Info */}
          <div className="md:col-span-2 space-y-8">
            <div className="flex items-center gap-3">
              <div className="bg-[#DB2777] p-3 rounded-2xl shadow-xl">
                <Hexagon className="w-8 h-8 text-white fill-white/20" />
              </div>
              <span className="text-3xl font-black tracking-tighter">MentorIQ</span>
            </div>
            <p className="text-gray-400 text-xl font-medium max-w-md leading-relaxed">
              We empower developers to reach their full potential through AI-driven insights and world-class mentorship. Built for the next generation of engineers.
            </p>
            <div className="flex items-center gap-6">
              {[Github, Twitter, Linkedin].map((Icon, i) => (
                <button key={i} className="text-gray-500 hover:text-white transition-colors">
                  <Icon className="w-6 h-6" />
                </button>
              ))}
            </div>
          </div>

          {/* Links 1 */}
          <div className="space-y-8">
            <h4 className="text-sm font-black uppercase tracking-widest text-[#DB2777]">Platform</h4>
            <ul className="space-y-4 text-gray-400 font-bold">
              <li><button className="hover:text-white transition-colors">How it Works</button></li>
              <li><button className="hover:text-white transition-colors">AI Analysis</button></li>
              <li><button className="hover:text-white transition-colors">Expert Mentors</button></li>
              <li><button className="hover:text-white transition-colors">Community</button></li>
            </ul>
          </div>

          {/* Links 2 */}
          <div className="space-y-8">
            <h4 className="text-sm font-black uppercase tracking-widest text-[#DB2777]">Trust & Security</h4>
            <ul className="space-y-4 text-gray-400 font-bold">
              <li className="flex items-center gap-2"><ShieldCheck className="w-4 h-4" /> Privacy Policy</li>
              <li className="flex items-center gap-2"><ShieldCheck className="w-4 h-4" /> Terms of Service</li>
              <li className="flex items-center gap-2"><Mail className="w-4 h-4" /> Support Center</li>
            </ul>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="pt-12 border-t border-white/5 flex flex-col md:flex-row items-center justify-between gap-6">
          <p className="text-gray-500 font-bold">© 2024 MentorIQ Inc. All rights reserved.</p>
          <div className="flex items-center gap-8 text-gray-500 text-sm font-black uppercase tracking-widest">
            <button className="hover:text-white transition-colors">Privacy</button>
            <button className="hover:text-white transition-colors">Terms</button>
            <button className="hover:text-white transition-colors">Cookie Policy</button>
          </div>
        </div>
      </div>
    </footer>
  );
}
