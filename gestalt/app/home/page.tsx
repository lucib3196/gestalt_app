import React from "react";

const HeroSection: React.FC = () => {
  return (
    <>
      <section id="hero-section" className="p-5">
        <div className="container text-center mt-3">
          <h1 className="main-heading">Gestalt Generator</h1>
          <p className="subheading">
            Empowering Educators with AI-Powered STEM Content Creation
          </p>
        </div>
      </section>
    </>
  );
};

export default function Home() {
  return (
    <>
      <HeroSection />
    </>
  );
}
