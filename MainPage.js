// src/MainPage.js
import React from 'react';
import VideoCapture from './VedioCapture';
import DisplayText from './DisplayText';
import './MainPage.css'; // Import styling

const MainPage = () => {
  return (
    <div className="main-container">
      <div className="video-container">
        <VideoCapture />
      </div>
      {/* <div className="text-container">
        <DisplayText />
      </div> */}
    </div>
  );
};

export default MainPage;
