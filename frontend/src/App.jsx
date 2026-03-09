import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import HomePage from './pages/HomePage'
import CandidatePage from './pages/CandidatePage'
import RecruiterDashboard from './pages/RecruiterDashboard'

/**
 * Main App component.
 * Sets up React Router with three routes:
 * - /            → Landing page (role selection)
 * - /candidate   → Candidate resume upload & job matching
 * - /recruiter   → Recruiter bulk upload & candidate ranking
 */
function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-slate-950">
        <Navbar />
        <main>
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/candidate" element={<CandidatePage />} />
            <Route path="/recruiter" element={<RecruiterDashboard />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  )
}

export default App
