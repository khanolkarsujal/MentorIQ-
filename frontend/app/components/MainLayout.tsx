import { ReactNode } from "react";
import Navbar from "./Navbar";
import Footer from "./Footer";
import { useLocation } from "react-router";

export default function MainLayout({ children }: { children: ReactNode }) {
  const location = useLocation();
  const isSplash = location.pathname === '/' || location.pathname === '/loading';

  return (
    <div className="min-h-screen flex flex-col bg-white overflow-x-hidden">
      {!isSplash && <Navbar />}
      
      <main className={`flex-grow flex flex-col ${!isSplash ? 'pt-24' : ''}`}>
        {children}
      </main>

      {!isSplash && <Footer />}
    </div>
  );
}
