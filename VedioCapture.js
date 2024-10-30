// src/VideoCapture.js
import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';

const VideoCapture = () => {
  const [gesture, setGesture] = useState('');
  const [sinhala, setSinhala] = useState('');
  const [error, setError] = useState(null);
  const [videoStream, setVideoStream] = useState(null);
  const captureInterval = useRef(null);
  const videoRef = useRef(null); // Ref for the video element

  useEffect(() => {
    // Get webcam stream when component mounts
    navigator.mediaDevices
      .getUserMedia({ video: true })
      .then((stream) => {
        setVideoStream(stream);
        if (videoRef.current) {
          videoRef.current.srcObject = stream; // Set video source
        }
        // Start capturing frames every 2 seconds
        captureInterval.current = setInterval(handleCapture, 2000);
      })
      .catch((err) => setError('Failed to access camera.'));

    // Cleanup: Stop the interval and release the camera when component unmounts
    return () => {
      clearInterval(captureInterval.current);
      if (videoStream) {
        videoStream.getTracks().forEach((track) => track.stop());
      }
    };
  }, []);

  const handleCapture = async () => {
    try {
      const video = videoRef.current;
      if (!video) return;
  
      const canvas = document.createElement('canvas');
      const context = canvas.getContext('2d');
  
      // Set canvas size to match video dimensions
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
  
      // Clear the canvas and draw the current video frame
      context.clearRect(0, 0, canvas.width, canvas.height);
      context.drawImage(video, 0, 0, canvas.width, canvas.height);
  
      // Convert canvas image to Base64
      const imageData = canvas.toDataURL('image/jpeg', 0.9);
      const base64Image = imageData.split(',')[1]; // Remove data:URL prefix
  
      // Send the image to the backend
      const response = await axios.post('http://localhost:5000/api/recognize', {
        image: base64Image,
      });
  
      setGesture(response.data.gesture); // Update gesture state
      setSinhala(response.data.sinhala);
      console.log("Response: ", response.data); // Log the full responsex
    } catch (err) {
      if (err.response) {
        console.error("Backend Error: ", err.response.data); // Log backend error response
      } else {
        console.error("Request Error: ", err.message);
      }
      setError('Recognition failed. Please try again.');
    }
  };
  

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
      <video
        ref={videoRef}
        autoPlay
        onLoadedMetadata={() => {
          // Start playing the video once metadata is loaded
          videoRef.current.play();
        }}
        style={{ width: '100%', borderRadius: '10px', marginBottom: '20px' }}
      />
      <div>
        {gesture ? <h3>Recognized Gesture: {gesture}</h3> : <p>Waiting for recognition...</p>}
        {error && <p style={{ color: 'red' }}>{error}</p>}
      </div>
      <div className="display-text-container">
      
      {sinhala ? <h1>Recognized Gesture: {sinhala}</h1> : <h1>Waiting for recognition...</h1>}

      
      <button className="recognize-button">Recognize Gesture</button>
    </div>
    </div>
    
  );
};

export default VideoCapture;
