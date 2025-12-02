import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Sprout, Leaf, Menu, X, MapPin, CloudSun, ClipboardList, Thermometer, WifiOff, Home } from 'lucide-react';
import LiveMode from './components/LiveMode';
import ManualMode from './components/ManualMode';
import LandingPage from './components/LandingPage';
import ChatBot from './components/ChatBot';
import './App.css';

function App() {
  const [page, setPage] = useState('home');
  const [menuOpen, setMenuOpen] = useState(false);

  const toggleMenu = () => setMenuOpen(!menuOpen);

  const navigateToSelector = () => setPage('selector');
  const navigateToLive = () => setPage('live');
  const navigateToManual = () => setPage('manual');
  const navigateToHome = () => setPage('home');

  return (
    <div className="app">
      {/* Header - Navbar Style */}
      <motion.header 
        className="header"
        initial={{ y: -100, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.4 }}
      >
        <div className="header-content">
          <div className="logo-section">
            <Sprout className="logo-icon" size={32} />
            <div>
              <h1>CropSense</h1>
              {/* <h3 className="logo-subtitle">Smart Shield For Smart Farming</h3> */}
              
            </div>
          </div>

          {/* Desktop Navigation */}
          <nav className="nav-features desktop-nav">
            <div className="nav-item">
              <Home size={18} />
              <span onClick={navigateToHome} style={{ cursor: 'pointer' }}>Home</span>
            </div>
            <div className="nav-item">
              <Sprout size={18} />
              <span onClick={navigateToSelector} style={{ cursor: 'pointer' }}>Smart Analysis</span>
            </div>
            <div className="nav-item">
              <Leaf size={18} />
              <span onClick={navigateToLive} style={{ cursor: 'pointer' }}>Live Analysis</span>
            </div>
          </nav>

          {/* Mobile Hamburger Menu */}
          <button className="hamburger-menu" onClick={toggleMenu}>
            {menuOpen ? <X size={28} /> : <Menu size={28} />}
          </button>
        </div>

        {/* Mobile Menu Dropdown */}
        <AnimatePresence>
          {menuOpen && (
            <motion.div
              className="mobile-menu"
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: 'auto', opacity: 1 }}
              exit={{ height: 0, opacity: 0 }}
              transition={{ duration: 0.3 }}
            >
              <div className="mobile-menu-item" onClick={() => { navigateToHome(); toggleMenu(); }}>
                <Home size={20} />
                <span>Home</span>
              </div>
              <div className="mobile-menu-item" onClick={() => { navigateToSelector(); toggleMenu(); }}>
                <Sprout size={20} />
                <span>Smart Analysis</span>
              </div>
              <div className="mobile-menu-item" onClick={() => { navigateToLive(); toggleMenu(); }}>
                <Leaf size={20} />
                <span>Live Analysis</span>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </motion.header>

      {/* Main Content */}
      <main className="main-content">
        {page === 'home' && (
          <LandingPage onGetStarted={navigateToSelector} />
        )}

        {page === 'selector' && (
          <motion.div 
            className="mode-selection"
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ duration: 0.5 }}
          >
            <h2>Choose Your Mode</h2>
            <p className="subtitle">Select how you'd like to get your crop recommendation</p>
            
            <div className="mode-cards">
              {/* Live Mode Card */}
              <motion.div 
                className="mode-card"
                whileHover={{ scale: 1.05, y: -5 }}
                whileTap={{ scale: 0.98 }}
                onClick={navigateToLive}
              >
                <div className="mode-icon live-icon">
                  <Sprout size={48} />
                </div>
                <h3>Live Mode</h3>
                <p>Auto-detect location and fetch real-time weather data</p>
                <ul className="features">
                  <li><MapPin size={20} /> GPS-Based Location Tracking</li>
                  <li><CloudSun size={20} /> Live Meteorological Data Integration</li>
                  <li><ClipboardList size={20} /> Customizable Soil Parameters</li>
                </ul>
                <button className="select-btn">Get Started →</button>
              </motion.div>

              {/* Manual Mode Card */}
              <motion.div 
                className="mode-card"
                whileHover={{ scale: 1.05, y: -5 }}
                whileTap={{ scale: 0.98 }}
                onClick={navigateToManual}
              >
                <div className="mode-icon manual-icon">
                  <Leaf size={48} />
                </div>
                <h3>Manual Mode</h3>
                <p>Enter all data manually for custom analysis</p>
                <ul className="features">
                  <li><ClipboardList size={20} /> Comprehensive Soil Data Input</li>
                  <li><Thermometer size={20} /> User-Defined Weather Conditions</li>
                  <li><WifiOff size={20} /> Offline Analysis Support</li>
                </ul>
                <button className="select-btn">Get Started →</button>
              </motion.div>
            </div>
          </motion.div>
        )}

        {page === 'live' && (
          <div className="mode-container">
            <LiveMode onBack={navigateToSelector} />
          </div>
        )}

        {page === 'manual' && (
          <div className="mode-container">
            <ManualMode onBack={navigateToSelector} />
          </div>
        )}
      </main>

      {/* Footer */}
      {/* Footer */}
      <motion.footer 
        className="footer"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.6, delay: 0.2 }}
      >
        <div className="footer-content">
          <div className="footer-section">
            <h4>CropSense</h4>
            <p>Empowering farmers with AI-driven insights for a sustainable future.</p>
          </div>
          <div className="footer-section">
            <h4>Quick Links</h4>
            <span onClick={navigateToHome}>Home</span>
            <span onClick={navigateToSelector}>Smart Analysis</span>
            <span onClick={navigateToLive}>Live Analysis</span>
          </div>
          <div className="footer-section">
            <h4>Contact</h4>
            <p>support@cropsense.com</p>
            <p>+91 7707891701</p>
          </div>
        </div>
        <div className="footer-bottom">
          <p>© 2024 CropSense. Powered by Genconians and OpenWeatherMap</p>
        </div>
      </motion.footer>

      {/* Global ChatBot */}
      <ChatBot />
    </div>
  );
}

export default App;
