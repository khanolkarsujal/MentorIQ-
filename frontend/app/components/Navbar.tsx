import { useNavigate, useLocation } from "react-router";
import { User, Bell, Search, Hexagon } from "lucide-react";

export default function Navbar() {
  const navigate = useNavigate();
  const location = useLocation();

  const navLinks = [
    { label: "Dashboard", path: "/results" },
    { label: "Community", path: "/community" },
    { label: "Your Path", path: "/journey" },
  ];

  // Hide nav on splash/login
  if (location.pathname === '/' || location.pathname === '/loading') return null;

  return (
    <nav className="fixed top-0 left-0 w-full z-50 bg-white/70 backdrop-blur-xl border-b border-gray-100 px-6 py-4">
      <div className="max-w-[1400px] mx-auto flex items-center justify-between">
        {/* Logo */}
        <div 
          onClick={() => navigate('/')}
          className="flex items-center gap-2 cursor-pointer group transition-transform hover:scale-105"
        >
          <div className="bg-[#DB2777] p-2 rounded-xl shadow-lg shadow-pink-100">
            <Hexagon className="w-6 h-6 text-white fill-white/20" />
          </div>
          <span className="text-2xl font-black text-[#1E293B] tracking-tighter">MentorIQ</span>
        </div>

        {/* Links */}
        <div className="hidden md:flex items-center gap-8">
          {navLinks.map((link) => (
            <button
              key={link.path}
              onClick={() => navigate(link.path)}
              className={`text-sm font-black uppercase tracking-widest transition-colors ${
                location.pathname === link.path ? 'text-[#DB2777]' : 'text-gray-400 hover:text-gray-900'
              }`}
            >
              {link.label}
            </button>
          ))}
        </div>

        {/* Icons / Profile */}
        <div className="flex items-center gap-6">
          <div className="hidden sm:flex items-center gap-4 text-gray-400">
            <button className="hover:text-gray-900 transition-colors"><Search className="w-5 h-5" /></button>
            <button className="hover:text-gray-900 transition-colors relative">
              <Bell className="w-5 h-5" />
              <div className="absolute top-0 right-0 w-2 h-2 bg-pink-500 rounded-full border-2 border-white"></div>
            </button>
          </div>
          <div 
            onClick={() => navigate('/')}
            className="w-10 h-10 rounded-full bg-gradient-to-br from-pink-400 to-purple-500 flex items-center justify-center text-white cursor-pointer hover:scale-110 transition-transform shadow-lg"
          >
            <User className="w-5 h-5" />
          </div>
        </div>
      </div>
    </nav>
  );
}
