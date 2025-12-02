import React from 'react';
import { motion } from 'framer-motion';
import { ArrowRight, Leaf, Sprout, ShieldCheck } from 'lucide-react';
import './LandingPage.css';
import heroImage from '../assets/hero_crops.png';
import techImage from '../assets/tech_farming.png';

const LandingPage = ({ onGetStarted }) => {
  return (
    <div className="landing-page">
      {/* Hero Section */}
      <section className="hero-section">
        <div className="hero-content">
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <span className="badge">AI-Powered Agriculture</span>
            <h1>Smart Farming for a <span className="highlight">Sustainable Future</span></h1>
            <p className="hero-text">
              Optimize your crop yields with our advanced recommendation system. 
              Analyze soil health, weather patterns, and get real-time insights.
            </p>
            <button className="cta-button" onClick={onGetStarted}>
              Get Started <ArrowRight size={20} />
            </button>
          </motion.div>
        </div>
        <motion.div 
          className="hero-image-container"
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
        >
          <img src={heroImage} alt="Vibrant crop field" className="hero-image" />
          <div className="floating-card card-1">
            <Sprout size={24} color="#10b981" />
            <div>
              <h4>98% Accuracy</h4>
              <p>Crop Prediction</p>
            </div>
          </div>
        </motion.div>
      </section>

      {/* Features Preview */}
      <section className="features-section">
        <div className="section-header">
          <h2>Why Choose CropSense?</h2>
          <p>Advanced technology meets traditional farming expertise</p>
        </div>
        
        <div className="feature-grid">
          <motion.div 
            className="feature-card"
            whileHover={{ y: -10 }}
          >
            <div className="card-bg-shape"></div>
            <div className="icon-box">
              <Leaf size={32} />
            </div>
            <h3>Smart Analysis</h3>
            <p>Get personalized crop recommendations based on your specific soil data using advanced ML algorithms.</p>
            <div className="card-footer">
              <span>Learn more</span> <ArrowRight size={16} />
            </div>
          </motion.div>

          <motion.div 
            className="feature-card"
            whileHover={{ y: -10 }}
          >
            <div className="card-bg-shape"></div>
            <div className="icon-box">
              <ShieldCheck size={32} />
            </div>
            <h3>Disease Prevention</h3>
            <p>Early warning systems to protect your crops from potential threats and maximize plant health.</p>
            <div className="card-footer">
              <span>Learn more</span> <ArrowRight size={16} />
            </div>
          </motion.div>

          <motion.div 
            className="feature-card"
            whileHover={{ y: -10 }}
          >
            <div className="card-bg-shape"></div>
            <div className="icon-box">
              <Sprout size={32} />
            </div>
            <h3>Yield Optimization</h3>
            <p>Maximize your harvest with data-driven farming insights and real-time environmental monitoring.</p>
            <div className="card-footer">
              <span>Learn more</span> <ArrowRight size={16} />
            </div>
          </motion.div>
        </div>
      </section>

      {/* Tech Section */}
      <section className="tech-section">
        <div className="tech-content">
          <img src={techImage} alt="Smart farming technology" className="tech-image" />
          <div className="tech-info">
            <h2>Precision Agriculture at Your Fingertips</h2>
            <p>
              Our platform leverages cutting-edge machine learning algorithms to process 
              complex environmental data, providing you with actionable insights that 
              take the guesswork out of farming.
            </p>
            <ul className="tech-list">
              <li>Real-time environmental monitoring</li>
              <li>Historical data analysis</li>
              <li>Predictive modeling for crop success</li>
            </ul>
          </div>
        </div>
      </section>
    </div>
  );
};

export default LandingPage;
