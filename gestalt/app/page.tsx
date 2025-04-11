import React from "react";
import Link from "next/link";
import ModGeneratorsCard from "@/components/ModGeneratorsCard";
import KeyFeatureCard, { FeatureProp } from "@/components/KeyFeatureCard";
export const QuickQueryGeneratorInfo = {
  name: "Text Generator",
  description:
    "Instantly transform individual text-based questions into comprehensive modules.",
  bestFor: "Fast, single-question processing.",
  inputType: "Text-based questions.",
  outputType: "Complete modules with all necessary content.",
  path: "/generators/text_generator",
};

export const VisualExtractGeneratorInfo = {
  name: "Image Extraction Generator",
  description: "Extract and process multiple questions from images or PDFs.",
  bestFor: "Handwritten notes, scanned documents, textbook solutions.",
  inputType: "Images and PDFs.",
  outputType: "Individual modules for each extracted question.",
  path: "/generators/image_generator",
};

export const KeyFeatures: FeatureProp[] = [
  {
    title: "Adaptive Content Generation",
    description:
      "Quickly generate tailored modules from text, images, or PDFs.",
  },
  {
    title: "Multi-Question Extraction",
    description:
      "Extract multiple questions from a single input and generate individual modules for each.",
  },
  {
    title: "Code-Enhanced AI Generation",
    description:
      "Leverage Retrieval-Augmented Generation (RAG) to search relevant code documentation, enhancing module quality and overcoming traditional training data limitations.",
  },
  {
    title: "Comprehensive Output",
    description:
      "Generate JavaScript, Python, and HTML files for computational questions and step-by-step solution guides.",
  },
  {
    title: "Customization & Review",
    description:
      "Manually test, tweak, and adjust outputs for precision and personalization.",
  },
];

const HeroSection: React.FC = () => {
  return (
    <>
      <section id="hero-section" className="p-5">
        <div className="container text-center mt-3">
          <h1 className="main-heading">Gestalt Generator</h1>
          <p className="subheading">
            Empowering Educators with AI-Powered STEM Content Creation
          </p>
          <Link href="/#generators-section" className="cta-button">
            Get Started
          </Link>
        </div>
      </section>
    </>
  );
};

const KeyFeatureSection: React.FC = () => {
  return (
    <>
      <section id="key-features" className="p-5">
        <div className="container text-center mb-5">
          <h2 className="section-heading">Key Features</h2>
          <hr className="divider div-dark" />
          <div className="container key-feature-container my-2">
            {KeyFeatures.map((feature, index) => (
              <KeyFeatureCard key={index} {...feature} />
            ))}
          </div>
        </div>
      </section>
    </>
  );
};

const GeneratorSection: React.FC = () => {
  return (
    <>
      <section id="generators-section" className="generators-section">
        <div className="container text-container">
          <h2>Our Generators</h2>
          <hr className="divider div-dark d-flex" />
        </div>
        <div className="generators-container">
          <ModGeneratorsCard {...QuickQueryGeneratorInfo} />
          <ModGeneratorsCard {...VisualExtractGeneratorInfo} />
        </div>
      </section>
    </>
  );
};

export default function Home() {
  return (
    <>
      <HeroSection />
      <GeneratorSection />
      <KeyFeatureSection />
    </>
  );
}
