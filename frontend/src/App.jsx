import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Sprout, Leaf, Menu, X } from 'lucide-react';
import LiveMode from './components/LiveMode';
import ManualMode from './components/ManualMode';
import './App.css';

function App() {
  const [mode, setMode] = useState(null);
  const [menuOpen, setMenuOpen] = useState(false);

  const resetMode = () => setMode(null);
  const toggleMenu = () => setMenuOpen(!menuOpen);

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
              <h3 className="logo-subtitle">Smart Shield For Smart Farming</h3>
              <p> Innovate,Protect,Grow</p>
            </div>
          </div>

          {/* Desktop Navigation */}
          <nav className="nav-features desktop-nav">
            <div className="nav-item">
              <Sprout size={18} />
              <span>Smart Analysis</span>
            </div>
            <div className="nav-item">
              <Leaf size={18} />
              <span>Real-time Weather</span>
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
              <div className="mobile-menu-item">
                <Sprout size={20} />
                <span>Smart Analysis</span>
              </div>
              <div className="mobile-menu-item">
                <Leaf size={20} />
                <span>Real-time Weather</span>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </motion.header>

      {/* Main Content */}
      <main className="main-content">
        {!mode ? (
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
                onClick={() => setMode('live')}
              >
                <div className="mode-icon live-icon">
                  <Sprout size={48} />
                </div>
                <h3>Live Mode</h3>
                <p>Auto-detect location and fetch real-time weather data</p>
                <ul className="features">
                  <li>📍 Auto location detection</li>
                  <li>🌤️ Real-time weather</li>
                  <li>✍️ Manual soil data</li>
                </ul>
                <button className="select-btn">Get Started →</button>
              </motion.div>

              {/* Manual Mode Card */}
              <motion.div 
                className="mode-card"
                whileHover={{ scale: 1.05, y: -5 }}
                whileTap={{ scale: 0.98 }}
                onClick={() => setMode('manual')}
              >
                <div className="mode-icon manual-icon">
                  <Leaf size={48} />
                </div>
                <h3>Manual Mode</h3>
                <p>Enter all data manually for custom analysis</p>
                <ul className="features">
                  <li>✍️ Manual soil data</li>
                  <li>🌡️ Manual weather</li>
                  <li>🔄 Offline capable</li>
                </ul>
                <button className="select-btn">Get Started →</button>
              </motion.div>
            </div>
          </motion.div>
        ) : (
          <div className="mode-container">
            {mode === 'live' ? (
              <LiveMode onBack={resetMode} />
            ) : (
              <ManualMode onBack={resetMode} />
            )}
          </div>
        )}
      </main>

      {/* Footer */}
      {/* <motion.footer 
        className="footer"
        initial={{ y: 100, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.6, delay: 0.2 }}
      >
        <p>Powered by NASA Weather API & OpenWeatherMap</p>
      </motion.footer> */}
    </div>
  );
}

export default App;
