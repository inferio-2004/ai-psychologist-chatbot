import React, { useState, useEffect } from "react";
import { Spinner } from "@chakra-ui/react";
import "./PsychotherapistDashboard.css";

const PsychotherapistDashboard = () => {
  const [selectedSession, setSelectedSession] = useState(null);
  const [report, setReport] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [hoveredPatient, setHoveredPatient] = useState(null);
  const [patients, setPatients] = useState([]);

  useEffect(() => {
    const fetchPatients = async () => {
      try {
        const response = await fetch("http://127.0.0.1:5000/get-patients-sessions");
        if (!response.ok) throw new Error("Failed to fetch patients");
        const data = await response.json();
        setPatients(data);
      } catch (error) {
        console.error("Error fetching patients:", error);
      }
    };
    fetchPatients();
  }, []);

  const fetchReport = async (patientName, sessionId) => {
    setLoading(true);
    try {
      const response = await fetch("http://127.0.0.1:5000/get-report", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ patient: patientName, session: sessionId })
      });
      if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
      const data = await response.json();
      setReport(data);
      setError(null);
    } catch (err) {
      console.error("Error fetching report:", err);
      setError("Failed to fetch the report. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  // Helper to render Top 3 Emotions per Message as enhanced cards
  const renderTop3Emotions = () => {
    if (!report || !report.emotion_analysis || !report.emotion_analysis.top_3_emotions_per_message)
      return null;
    return (
      <div className="enhanced-emotions">
        <h4>Top 3 Emotions per Message</h4>
        {Object.entries(report.emotion_analysis.top_3_emotions_per_message).map(
          ([msg, emotions], index) => (
            <div key={index} className="emotion-message-card">
              <div className="emotion-message">
                <strong>Message:</strong> {msg}
              </div>
              <div className="emotion-list">
                {emotions.map(([emotion, score], idx) => (
                  <div key={idx} className="emotion-item">
                    <span className="emotion-name">{emotion}</span>:{" "}
                    <span className="emotion-score">{score.toFixed(4)}</span>
                  </div>
                ))}
              </div>
            </div>
          )
        )}
      </div>
    );
  };

  // Helper to render Emotion Distribution in a grid
  const renderEmotionGrid = () => {
    if (!report || !report.emotion_analysis || !report.emotion_analysis.distribution)
      return null;
    const entries = Object.entries(report.emotion_analysis.distribution);
    const colCount = 3;
    const rowCount = Math.ceil(entries.length / colCount);
    const columns = [];
    for (let i = 0; i < colCount; i++) {
      columns.push(entries.slice(i * rowCount, (i + 1) * rowCount));
    }
    return (
      <div className="emotion-grid">
        {columns.map((col, colIndex) => (
          <div key={colIndex} className="emotion-column">
            {col.map(([emotion, percentage], idx) => (
              <div key={idx} className="emotion-item">
                <strong>{emotion}:</strong> {percentage}%
              </div>
            ))}
          </div>
        ))}
      </div>
    );
  };

  return (
    <div className="dashboard-container">
      {/* Sidebar */}
      <div className="sidebar">
        <h2>Patients</h2>
        <ul>
          {patients.map((patient) => (
            <li
              key={patient.id}
              className="patient-item"
              onMouseEnter={() => setHoveredPatient(patient)}
              onMouseLeave={() => setHoveredPatient(null)}
            >
              {patient.name}
              {hoveredPatient?.id === patient.id && (
                <div className="sessions-box">
                  {patient.sessions.map((session, index) => (
                    <button
                      key={index}
                      onClick={() => {
                        setSelectedSession(session);
                        fetchReport(patient.name, session);
                      }}
                    >
                      {session}
                    </button>
                  ))}
                </div>
              )}
            </li>
          ))}
        </ul>
      </div>

      {/* Report Section */}
      <div className="report-container">
        {error && <p className="error">{error}</p>}
        {loading ? (
          <div style={{ textAlign: "center", marginTop: "50px" }}>
            <Spinner size="xl" color="teal.500" />
            <p>Loading report...</p>
          </div>
        ) : report ? (
          <div className="report-section">
            <h2>📄 Session {selectedSession} Report</h2>

            {/* Concerning Topics */}
            <div className="report-block">
              <h3>🛑 Concerning Topics</h3>
              {Object.entries(report.concern_detection).map(([message, concerns], index) => (
                <div key={index} className="report-sub-block">
                  <p><strong>Message:</strong> {message}</p>
                  <ul>
                    {Object.entries(concerns).map(([concern, score], idx) => (
                      <li key={idx}>
                        {concern}: {score.toFixed(4)}
                      </li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>

            {/* Emotion Analysis */}
            <div className="report-block">
              <h3>😊 Emotion Analysis</h3>
              <p><strong>Emotion Distribution:</strong></p>
              {renderEmotionGrid()}
              <img
                src={`http://127.0.0.1:5000/static/${report.emotion_analysis.image}`}
                alt="Emotion Distribution"
              />
              {renderTop3Emotions()}
            </div>

            {/* Sentiment Analysis */}
            <div className="report-block">
              <h3>📉 Sentiment Analysis</h3>
              <p><strong>Overall Sentiment Trend:</strong> {report.sentiment_analysis.trend}</p>
              <p><strong>Sentiment Score:</strong> {report.sentiment_analysis.score}</p>
              <img
                src={`http://127.0.0.1:5000/static/${report.sentiment_analysis.image}`}
                alt="Sentiment Trend"
              />
            </div>

            {/* Interactive Sentiment Analysis */}
            <div className="report-block">
              <h3>📊 Interactive Sentiment Analysis</h3>
              <iframe
                src={`http://127.0.0.1:5000/static/${report.interactive_sentiment_analysis}`}
                title="Interactive Sentiment Analysis"
                className="interactive-plot"
              ></iframe>
            </div>

            {/* Conversation Logs */}
            <div className="report-block">
              <h3>💬 Conversation Logs</h3>
              {report.entire_convo && report.entire_convo.length > 0 ? (
                <div className="chat-window">
                  {report.entire_convo.map((msg, index) => (
                    <div
                      key={index}
                      className={`message-bubble ${index % 2 === 0 ? "bot-message" : "user-message"}`}
                    >
                      {msg}
                    </div>
                  ))}
                </div>
              ) : (
                <p>No conversation data available.</p>
              )}
            </div>

            {/* NLP Summarization */}
            <div className="report-block">
              <h3>📜 NLP Conversation Summary</h3>
              <p>{report.nlp_summarization}</p>
            </div>

            {/* Word Cloud */}
            <div className="report-block">
              <h3>🔠 Word Cloud</h3>
              <img
                src={`http://127.0.0.1:5000/static/${report.wordcloud}`}
                alt="Word Cloud"
              />
            </div>

          </div>
        ) : (
          <p className="placeholder">Select a session to view the report.</p>
        )}
      </div>
    </div>
  );
};

export default PsychotherapistDashboard;
