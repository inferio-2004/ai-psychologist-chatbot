import React, { useState, useEffect } from "react";
import SpeechRecognition, { useSpeechRecognition } from "react-speech-recognition";
import { FaMicrophone } from "react-icons/fa";
import Orb from "./Orb";
import "./ChatBot.css";

const ChatBot = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const { transcript, listening, resetTranscript } = useSpeechRecognition();

  // Retrieve the username from sessionStorage; default to "Anonymous" if not found
  const username = sessionStorage.getItem("username") || "Anonymous";

  useEffect(() => {
    if (transcript) setInput(transcript);
  }, [transcript]);

  const speak = (text) => {
    const utterance = new SpeechSynthesisUtterance(text);
    window.speechSynthesis.speak(utterance);
  };

  const sendMessage = async (text) => {
    if (!text.trim()) return;
    
    const userMessage = { text, sender: "user" };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    resetTranscript();
    if (listening) SpeechRecognition.stopListening();
    
    // Make a POST request to the Rasa backend with the username and message
    try {
      const response = await fetch("http://localhost:5005/webhooks/rest/webhook", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ sender: username, message: text }),
      });
      const data = await response.json();
      if (data && data.length > 0) {
        data.forEach((reply) => {
          setMessages((prev) => [...prev, { text: reply.text, sender: "bot" }]);
          speak(reply.text);
        });
      } else {
        setMessages((prev) => [...prev, { text: "No response from bot.", sender: "bot" }]);
        speak("No response from bot.");
      }
    } catch (error) {
      console.error("Error sending message:", error);
      setMessages((prev) => [...prev, { text: "Error contacting server.", sender: "bot" }]);
      speak("Error contacting server.");
    }
  };

  return (
    <div className="chat-container">
      <div className="orb-wrapper">
        <Orb hoverIntensity={0.5} rotateOnHover={true} hue={200} forceHoverState={listening} />
      </div>
      <div className="chat-box">
        {messages.map((msg, index) => (
          <div key={index} className={msg.sender === "user" ? "user-message" : "bot-message"}>
            <span>{msg.text}</span>
          </div>
        ))}
      </div>
      <div className="input-area">
        <input 
          type="text" 
          value={input} 
          onChange={(e) => setInput(e.target.value)} 
          placeholder="Type a message..."
        />
        <button 
          onClick={() => {
            sendMessage(input);
            if (listening) {
              SpeechRecognition.stopListening();
            }
            document.querySelector('.orb-wrapper').classList.remove('globe-active');
            document.querySelector('.orb-wrapper').setAttribute('forceHoverState', 'false');
            SpeechRecognition.abortListening();
          }} 
          className="send-button"
        >
          Send
        </button>
        <button 
          onClick={() => listening ? SpeechRecognition.stopListening() : SpeechRecognition.startListening({ continuous: true })} 
          className="mic-button"
        >
          <FaMicrophone className={`mic-icon ${listening ? "mic-active-glow" : ""}`} />
        </button>
      </div>
    </div>
  );
};

export default ChatBot;
