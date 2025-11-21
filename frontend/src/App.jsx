import { useState } from 'react'
import './App.css'
import LiveKitModal from './components/LiveKitModal';

function App() {
  const [showSupport, setShowSupport] = useState(false);

  const handleSupportClick = () => {
    setShowSupport(true)
  }

  return (
    <div className="app">
      <header className="header">
        <div className="logo">LiveKit Agent</div>
        <div className="made-by">made by youssef salah</div>
      </header>

      <main className="main-section">
        

        <h1 className="welcome-title">
           AI Agent<br />
          <span>Powered by LiveKit + RAG</span>
        </h1>

        <button className="support-button" onClick={handleSupportClick}>
          Talk to The Agent
        </button>
      </main>

      {showSupport && <LiveKitModal setShowSupport={setShowSupport} />}
    </div>
  )
}

export default App
