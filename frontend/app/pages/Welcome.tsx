import { useState } from "react";
import { useNavigate } from "react-router";
import { Mail, Lock, User, Github } from "lucide-react";

export default function Welcome() {
  const navigate = useNavigate();
  const [isLogin, setIsLogin] = useState(true);
  const [loading, setLoading] = useState(false);
  
  // Form State
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [fullName, setFullName] = useState("");
  const [errorMsg, setErrorMsg] = useState("");

  const handleAuth = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setErrorMsg("");

    // Developer Mode: Bypass real authentication for now so limits don't block development
    setTimeout(() => {
      setLoading(false);
      navigate('/how-we-help');
    }, 600);
  };

  const signInWithGithub = async () => {
    // Navigate immediately for testing purposes
    navigate('/how-we-help');
  };

  const signInWithGoogle = async () => {
    // Navigate immediately for testing purposes
    navigate('/how-we-help');
  };

  return (
    <div className="size-full min-h-screen flex items-center justify-center bg-[#EADDFF] p-6">
      <div className="premium-card max-w-[950px] w-full grid md:grid-cols-2 overflow-hidden p-0 shadow-3xl">
        {/* Left Side: Branding */}
        <div className="bg-[#F8FAFC] p-12 flex flex-col justify-center items-center text-center gap-8 border-r border-gray-100/50">
          <div className="w-full overflow-hidden rounded-[2.5rem] shadow-xl">
            <img 
              src="/cats.jpg" 
              alt="Welcome Illustration" 
              className="w-full object-cover hover:scale-105 transition-transform duration-700" 
            />
          </div>
          <div className="space-y-3">
            <h1 className="text-3xl font-black text-[#1E293B]">MentorIQ</h1>
            <p className="text-lg text-[#64748B] font-medium leading-relaxed">
              Your personal AI-powered coding journey starts here.
            </p>
          </div>
        </div>

        {/* Right Side: Auth */}
        <div className="p-12 md:p-16 flex flex-col justify-center bg-white">
          <div className="mb-8">
            <div className="inline-block bg-purple-100 text-purple-700 font-bold px-3 py-1 rounded-full text-xs mb-4">
              Development Mode Active
            </div>
            <h2 className="text-4xl font-black text-[#1E293B] mb-2">
              {isLogin ? "Welcome Back!" : "Get Started"}
            </h2>
            <p className="text-[#64748B] font-medium">
              Join thousands of engineers accelerating their careers.
            </p>
          </div>

          {/* Social Auth Buttons */}
          <div className="grid grid-cols-2 gap-4 mb-6">
            <button 
              type="button"
              onClick={signInWithGoogle}
              className="flex items-center justify-center gap-3 border-2 border-gray-100 py-4 rounded-2xl font-black text-[#1E293B] hover:bg-gray-50 transition-all text-sm group cursor-pointer"
            >
              <img src="https://www.google.com/favicon.ico" className="w-4 h-4 group-hover:scale-110 transition-transform" alt="Google" />
              Google
            </button>
            <button 
              type="button"
              onClick={signInWithGithub}
              className="flex items-center justify-center gap-3 border-2 border-gray-100 py-4 rounded-2xl font-black text-[#1E293B] hover:bg-gray-50 transition-all text-sm group cursor-pointer"
            >
              <Github className="w-4 h-4 group-hover:scale-110 transition-transform" />
              GitHub
            </button>
          </div>

          <div className="flex items-center gap-4 w-full text-gray-300 mb-6">
            <div className="h-px bg-gray-100 flex-1"></div>
            <span className="text-xs font-black uppercase tracking-widest text-gray-400">or use email</span>
            <div className="h-px bg-gray-100 flex-1"></div>
          </div>

          {/* Error Message Display */}
          {errorMsg && (
            <div className="mb-6 p-4 bg-red-50 text-red-600 rounded-xl text-sm font-bold text-center border border-red-100">
              {errorMsg}
            </div>
          )}

          <form onSubmit={handleAuth} className="space-y-4">
            {!isLogin && (
              <div className="relative group">
                <User className="absolute left-6 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400 group-focus-within:text-[#DB2777]" />
                <input
                  type="text"
                  placeholder="Full Name"
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                  className="w-full bg-gray-50 border-2 border-transparent focus:border-[#DB2777] focus:bg-white px-14 py-4 rounded-2xl font-bold text-[#1E293B] outline-none transition-all placeholder:text-gray-400"
                  required={!isLogin}
                />
              </div>
            )}
            <div className="relative group">
              <Mail className="absolute left-6 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400 group-focus-within:text-[#DB2777]" />
              <input
                type="email"
                placeholder="Email Address"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full bg-gray-50 border-2 border-transparent focus:border-[#DB2777] focus:bg-white px-14 py-4 rounded-2xl font-bold text-[#1E293B] outline-none transition-all placeholder:text-gray-400"
                required
              />
            </div>
            <div className="relative group">
              <Lock className="absolute left-6 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400 group-focus-within:text-[#DB2777]" />
              <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full bg-gray-50 border-2 border-transparent focus:border-[#DB2777] focus:bg-white px-14 py-4 rounded-2xl font-bold text-[#1E293B] outline-none transition-all placeholder:text-gray-400"
                required
              />
            </div>

            <button 
              disabled={loading}
              type="submit"
              className="premium-button w-full bg-gradient-to-r from-[#DB2777] to-[#8B5CF6] text-white text-lg py-5 shadow-2xl hover:shadow-pink-100 mt-2"
            >
              {loading ? "Logging in..." : (isLogin ? "Sign In" : "Create Account")}
            </button>
          </form>

          <button 
            onClick={() => {
              setIsLogin(!isLogin);
              setErrorMsg("");
            }}
            className="text-center mt-6 text-[#64748B] font-bold hover:text-[#DB2777] transition-colors py-2"
          >
            {isLogin ? "Don't have an account? Sign Up" : "Already have an account? Log In"}
          </button>
        </div>
      </div>
    </div>
  );
}
