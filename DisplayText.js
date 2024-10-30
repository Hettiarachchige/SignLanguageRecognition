// src/components/DisplayText.js
import React from 'react';
import './DisplayText.css'; // Import CSS

const DisplayText = () => {
  return (
    <div className="display-text-container">
      <h1>Recognized Text</h1>
      <textarea readOnly
        className="recognized-textarea"
        rows="10"
        cols="30"
        placeholder="The recognized text will appear here..."
      ></textarea>
      <button className="recognize-button">Recognize Gesture</button>
    </div>
  );
};

export default DisplayText;
