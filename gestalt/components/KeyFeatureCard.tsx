import React from "react";
import "../styles/KeyFeatureCard.css";

export interface FeatureProp {
  title: string;
  description: string;
}

const KeyFeatureCard: React.FC<FeatureProp> = ({ title, description }) => {
  return (
    <div className="card m-2 key-feature-item">
      <div className="card-body key-feature-body">
        <h5 className="card-title feature-title">
          {title}
          <hr className="divider" />
        </h5>
      </div>
      <p className="card-text feature-text">{description}</p>
    </div>
  );
};

export default KeyFeatureCard;
