import { useState } from 'react'
import axios from 'axios'
import { Upload, Loader2, AlertCircle, CheckCircle2, Sparkles } from 'lucide-react'
import FileUploader from '../components/FileUploader'
import JobCard from '../components/JobCard'
import GapAnalysis from '../components/GapAnalysis'

const API_BASE = import.meta.env.VITE_API_URL || ''

/**
 * CandidatePage — Resume upload, job matching, and gap analysis for job seekers.
 *
 * Flow:
 * 1. User uploads resume → parsed by backend
 * 2. Resume text sent to /api/candidate/match-jobs → returns top 5 matches
 * 3. User clicks "Gap Analysis" on a job → AI analysis displayed below
 */
export default function CandidatePage() {
  // State
  const [resumeFile, setResumeFile] = useState(null)
  const [resumeText, setResumeText] = useState('')
  const [parsedInfo, setParsedInfo] = useState(null)
  const [matchResults, setMatchResults] = useState([])
  const [selectedJob, setSelectedJob] = useState(null)
  const [gapAnalysis, setGapAnalysis] = useState(null)

  // Loading states
  const [uploadLoading, setUploadLoading] = useState(false)
  const [matchLoading, setMatchLoading] = useState(false)
  const [gapLoading, setGapLoading] = useState(false)

  // Error states
  const [uploadError, setUploadError] = useState('')
  const [matchError, setMatchError] = useState('')
  const [gapError, setGapError] = useState('')

  // ─── Step 1: Upload Resume ─────────────────────────────────────────────

  const handleFileSelect = (file) => {
    setResumeFile(file)
    setResumeText('')
    setParsedInfo(null)
    setMatchResults([])
    setSelectedJob(null)
    setGapAnalysis(null)
    setUploadError('')
    setMatchError('')
  }

  const handleUploadResume = async () => {
    if (!resumeFile) return

    setUploadLoading(true)
    setUploadError('')

    try {
      const formData = new FormData()
      formData.append('file', resumeFile)

      const response = await axios.post(`${API_BASE}/api/candidate/upload-resume`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
        timeout: 30000,
      })

      const data = response.data
      setResumeText(data.resume_text)
      setParsedInfo({
        name: data.extracted_name,
        email: data.extracted_email,
        phone: data.extracted_phone,
        wordCount: data.word_count,
      })
    } catch (err) {
      const msg = err.response?.data?.detail || err.message || 'Failed to parse resume'
      setUploadError(msg)
    } finally {
      setUploadLoading(false)
    }
  }

  // ─── Step 2: Match Jobs ────────────────────────────────────────────────

  const handleMatchJobs = async () => {
    if (!resumeText) return

    setMatchLoading(true)
    setMatchError('')
    setMatchResults([])
    setSelectedJob(null)
    setGapAnalysis(null)

    try {
      const formData = new FormData()
      formData.append('resume_text', resumeText)

      const response = await axios.post(`${API_BASE}/api/candidate/match-jobs`, formData, {
        timeout: 60000,
      })
      setMatchResults(response.data.matches || [])
    } catch (err) {
      const msg = err.response?.data?.detail || err.message || 'Failed to find job matches'
      setMatchError(msg)
    } finally {
      setMatchLoading(false)
    }
  }

  // ─── Step 3: Gap Analysis ──────────────────────────────────────────────

  const handleViewGapAnalysis = async (job) => {
    if (selectedJob?.job_id === job.job_id) {
      // Toggle off if same job
      setSelectedJob(null)
      setGapAnalysis(null)
      return
    }

    setSelectedJob(job)
    setGapLoading(true)
    setGapError('')
    setGapAnalysis(null)

    try {
      const response = await axios.post(`${API_BASE}/api/candidate/gap-analysis`, {
        resume_text: resumeText,
        job_id: job.job_id,
        match_score: job.match_score,
      }, { timeout: 60000 })
      setGapAnalysis(response.data)
    } catch (err) {
      const msg = err.response?.data?.detail || err.message || 'Failed to generate gap analysis'
      setGapError(msg)
    } finally {
      setGapLoading(false)
    }
  }

  // ─── Render ────────────────────────────────────────────────────────────

  const isStep1Done = !!resumeText
  const isStep2Done = matchResults.length > 0

  return (
    <div className="min-h-screen py-10 px-4">
      <div className="container-section space-y-8">

        {/* Page Header */}
        <div>
          <h1 className="text-3xl font-bold text-slate-100">Find Your Best Job Matches</h1>
          <p className="text-slate-500 mt-2">
            Upload your resume and let AI find the most relevant jobs for your skills.
          </p>
        </div>

        {/* ─── Step 1: Upload Resume ─────────────────────────────────────── */}
        <div className="glass-card p-6">
          <div className="flex items-center gap-3 mb-6">
            <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold
              ${isStep1Done ? 'bg-emerald-600 text-white' : 'bg-primary-600 text-white'}`}>
              {isStep1Done ? <CheckCircle2 size={16} /> : '1'}
            </div>
            <h2 className="text-slate-100 font-semibold text-lg">Upload Your Resume</h2>
          </div>

          <FileUploader
            onFileSelect={handleFileSelect}
            label="Upload Resume"
            sublabel="PDF or DOCX, max 10MB"
          />

          {uploadError && (
            <div className="mt-4 flex items-start gap-2 text-red-400 text-sm bg-red-900/20 border border-red-800/50 rounded-xl px-4 py-3">
              <AlertCircle size={16} className="shrink-0 mt-0.5" />
              <span>{uploadError}</span>
            </div>
          )}

          {parsedInfo && (
            <div className="mt-4 bg-emerald-900/20 border border-emerald-700/50 rounded-xl px-4 py-3">
              <div className="flex items-center gap-2 text-emerald-400 text-sm font-medium mb-2">
                <CheckCircle2 size={15} />
                Resume parsed successfully
              </div>
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs text-slate-400">
                {parsedInfo.name && <div><span className="text-slate-600">Name:</span> {parsedInfo.name}</div>}
                {parsedInfo.email && <div><span className="text-slate-600">Email:</span> {parsedInfo.email}</div>}
                {parsedInfo.phone && <div><span className="text-slate-600">Phone:</span> {parsedInfo.phone}</div>}
                <div><span className="text-slate-600">Words:</span> {parsedInfo.wordCount?.toLocaleString()}</div>
              </div>
            </div>
          )}

          <button
            onClick={handleUploadResume}
            disabled={!resumeFile || uploadLoading}
            className="btn-primary mt-4 flex items-center gap-2"
          >
            {uploadLoading
              ? <><Loader2 size={16} className="animate-spin" /> Parsing Resume...</>
              : <><Upload size={16} /> Parse Resume</>
            }
          </button>
        </div>

        {/* ─── Step 2: Find Matches ─────────────────────────────────────── */}
        {isStep1Done && (
          <div className="glass-card p-6">
            <div className="flex items-center gap-3 mb-6">
              <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold
                ${isStep2Done ? 'bg-emerald-600 text-white' : 'bg-primary-600 text-white'}`}>
                {isStep2Done ? <CheckCircle2 size={16} /> : '2'}
              </div>
              <h2 className="text-slate-100 font-semibold text-lg">Find Matching Jobs</h2>
            </div>

            <p className="text-slate-500 text-sm mb-4">
              ResuM8 will compare your resume against all jobs in the database using
              Google Gemini semantic embeddings. This may take 15-30 seconds.
            </p>

            {matchError && (
              <div className="mb-4 flex items-start gap-2 text-red-400 text-sm bg-red-900/20 border border-red-800/50 rounded-xl px-4 py-3">
                <AlertCircle size={16} className="shrink-0 mt-0.5" />
                <span>{matchError}</span>
              </div>
            )}

            <button
              onClick={handleMatchJobs}
              disabled={matchLoading}
              className="btn-primary flex items-center gap-2"
            >
              {matchLoading
                ? <><Loader2 size={16} className="animate-spin" /> Finding Matches...</>
                : <><Sparkles size={16} /> Match to Jobs</>
              }
            </button>
          </div>
        )}

        {/* ─── Match Results ────────────────────────────────────────────── */}
        {matchResults.length > 0 && (
          <div>
            <h2 className="text-slate-100 font-bold text-xl mb-4">
              Your Top {matchResults.length} Job Matches
            </h2>
            <div className="space-y-4">
              {matchResults.map((job) => (
                <div key={job.job_id}>
                  <JobCard
                    job={job}
                    onViewGapAnalysis={handleViewGapAnalysis}
                    isSelected={selectedJob?.job_id === job.job_id}
                    isTopMatch={job.rank === 1}
                  />

                  {/* Gap Analysis — shown inline below selected job */}
                  {selectedJob?.job_id === job.job_id && (
                    <div className="mt-3">
                      {gapError ? (
                        <div className="flex items-start gap-2 text-red-400 text-sm bg-red-900/20 border border-red-800/50 rounded-xl px-4 py-3">
                          <AlertCircle size={16} className="shrink-0 mt-0.5" />
                          <span>{gapError}</span>
                        </div>
                      ) : (
                        <GapAnalysis
                          analysis={gapAnalysis}
                          matchScore={job.match_score}
                          jobTitle={job.title}
                          loading={gapLoading}
                        />
                      )}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
