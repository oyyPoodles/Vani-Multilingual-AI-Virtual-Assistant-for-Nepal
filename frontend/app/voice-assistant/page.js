"use client";
import { useState } from "react";
import Sidebar from "../components/Sidebar";

export default function VoiceAssistantPage() {
  const [language, setLanguage] = useState("auto");
  const [isRecording, setIsRecording] = useState(false);
  const [transcript, setTranscript] = useState("");
  const [response, setResponse] = useState("");
  const [chatHistory, setChatHistory] = useState([
    { role: "assistant", text: "नमस्ते! म VANI हुँ — तपाईंको AI सहायक। I can help with sales, inventory, invoices, and more. कसरी सहयोग गर्न सकछु?" },
  ]);
  const [textInput, setTextInput] = useState("");

  const handleMicClick = () => {
    setIsRecording(!isRecording);
    if (!isRecording) {
      setTranscript("Listening...");
      setResponse("");
      // In production: connect to WebSocket/API for real-time ASR
      setTimeout(() => {
        const mockTranscript = "आजको बिक्री कति भयो?";
        setTranscript(mockTranscript);
        setIsRecording(false);
        const mockResponse = "आजको कुल बिक्री NPR 1,25,400 छ। कुल ४५ वटा transaction भएको छ।";
        setResponse(mockResponse);
        setChatHistory(prev => [
          ...prev,
          { role: "user", text: mockTranscript },
          { role: "assistant", text: mockResponse }
        ]);
      }, 2000);
    } else {
      setTranscript("");
    }
  };

  const handleTextSubmit = (e) => {
    e.preventDefault();
    if (!textInput.trim()) return;
    const userText = textInput;
    setTextInput("");
    setChatHistory(prev => [...prev, { role: "user", text: userText }]);

    // Mock response - in production, call /api/chat
    setTimeout(() => {
      const mockReply = `Processing: "${userText}" — This would connect to the VANI backend API for real responses.`;
      setResponse(mockReply);
      setChatHistory(prev => [...prev, { role: "assistant", text: mockReply }]);
    }, 500);
  };

  return (
    <div className="app-layout">
      <Sidebar />
      <main className="main-content">
        <header className="page-header">
          <h1 className="page-title">🎙️ Voice Assistant</h1>
          <p className="page-subtitle">Speak in Nepali, English, or both — VANI understands</p>
        </header>
        <div className="page-body">
          <div className="voice-container">
            {/* Language Toggle */}
            <div className="lang-toggle">
              {["auto", "ne", "en"].map((lang) => (
                <button
                  key={lang}
                  className={`lang-btn ${language === lang ? "active" : ""}`}
                  onClick={() => setLanguage(lang)}
                >
                  {lang === "auto" ? "🌐 Auto" : lang === "ne" ? "🇳🇵 नेपाली" : "🇬🇧 English"}
                </button>
              ))}
            </div>

            {/* Microphone Button */}
            <button
              className={`mic-button ${isRecording ? "recording" : ""}`}
              onClick={handleMicClick}
              id="mic-button"
              aria-label={isRecording ? "Stop recording" : "Start recording"}
            >
              🎤
            </button>
            <div className="mic-label">
              {isRecording ? "🔴 Recording... Tap to stop" : "Press and Speak"}
            </div>

            {/* Transcript */}
            {transcript && (
              <div className="transcript-box">
                <div style={{ fontSize: 12, color: "var(--text-muted)", marginBottom: 8, textTransform: "uppercase", letterSpacing: "0.5px" }}>Transcription</div>
                {transcript}
              </div>
            )}

            {/* VANI Response */}
            {response && (
              <div className="response-box">
                <div style={{ fontSize: 12, color: "var(--accent-indigo)", marginBottom: 8, fontWeight: 600, textTransform: "uppercase", letterSpacing: "0.5px" }}>VANI Response</div>
                {response}
              </div>
            )}

            {/* Text Input */}
            <form onSubmit={handleTextSubmit} style={{ width: "100%", maxWidth: 700, display: "flex", gap: 10 }}>
              <div className="search-box" style={{ flex: 1, marginBottom: 0 }}>
                <span>💬</span>
                <input
                  type="text"
                  placeholder="Type your question here... (Nepali or English)"
                  value={textInput}
                  onChange={(e) => setTextInput(e.target.value)}
                  id="text-input"
                  style={{ fontFamily: "'Noto Sans Devanagari', 'Inter', sans-serif" }}
                />
              </div>
              <button type="submit" className="btn btn-primary">Send</button>
            </form>

            {/* Chat History */}
            <div style={{ width: "100%", maxWidth: 700 }}>
              <h3 style={{ fontSize: 14, fontWeight: 600, color: "var(--text-muted)", marginBottom: 12, textTransform: "uppercase", letterSpacing: "0.5px" }}>Conversation History</h3>
              <div className="chat-history">
                {chatHistory.map((msg, i) => (
                  <div key={i} className={`chat-msg ${msg.role}`}>
                    {msg.text}
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
