import { useState } from 'react'
import axios from 'axios'
import { Loader2, AlertCircle, Sparkles, EyeOff, Eye, Bot, X } from 'lucide-react'
import FileUploader from '../components/FileUploader'
import CandidateRankTable from '../components/CandidateRankTable'

const API_BASE = import.meta.env.VITE_API_URL || ''

/**
 * RecruiterDashboard — Bulk resume upload, candidate ranking, and AI summaries.
 *
 * Flow:
 * 1. Recruiter pastes job description
 * 2. Recruiter uploads up to 20 resumes
 * 3. Backend ranks candidates by semantic similarity
 * 4. Recruiter can click "AI Summary" for any candidate
 */
export default function RecruiterDashboard() {
  // Form state
  const [jobDescription, setJobDescription] = useState('')
  const [resumeFiles, setResumeFiles] = useState([])
  const [maskNames, setMaskNames] = useState(false)

  // Results state
  const [rankedCandidates, setRankedCandidates] = useState([])

  // Summary modal state
  const [summaryCandidate, setSummaryCandidate] = useState(null)
  const [summaryText, setSummaryText] = useState('')
  const [summaryLoading, setSummaryLoading] = useState(false)
  const [summaryError, setSummaryError] = useState('')

  // Loading / error state
  const [rankLoading, setRankLoading] = useState(false)
  const [rankError, setRankError] = useState('')

  // ─── Handle file selection ─────────────────────────────────────────────

  const handleMultipleSelect = (files) => {
    setResumeFiles(files)
  }

  // ─── Rank Candidates ───────────────────────────────────────────────────

  const handleRankCandidates = async () => {
    if (!jobDescription.trim() || resumeFiles.length === 0) return

    setRankLoading(true)
    setRankError('')
    setRankedCandidates([])

    try {
      const formData = new FormData()
      formData.append('job_description', jobDescription)
      formData.append('mask_names', maskNames ? 'true' : 'false')
      resumeFiles.forEach((file) => formData.append('files', file))

      const response = await axios.post(`${API_BASE}/api/recruiter/upload-resumes`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
        timeout: 120000, // 2 min for bulk processing
      })

      setRankedCandidates(response.data.candidates || [])
    } catch (err) {
      const msg = err.response?.data?.detail || err.message || 'Failed to rank candidates'
      setRankError(msg)
    } finally {
      setRankLoading(false)
    }
  }

  // ─── Get AI Summary ────────────────────────────────────────────────────

  const handleViewSummary = async (candidate) => {
    setSummaryCandidate(candidate)
    setSummaryText('')
    setSummaryLoading(true)
    setSummaryError('')

    try {
      const formData = new FormData()
      formData.append('resume_text', candidate.resume_text)
      formData.append('candidate_name', candidate.name)
      formData.append('job_title', '') // Could pass JD title if extracted

      const response = await axios.post(
        `${API_BASE}/api/recruiter/summary/${candidate.candidate_id}`,
        formData,
        { timeout: 30000 }
      )
      setSummaryText(response.data.summary)
    } catch (err) {
      const msg = err.response?.data?.detail || err.message || 'Failed to generate summary'
      setSummaryError(msg)
    } finally {
      setSummaryLoading(false)
    }
  }

  const closeSummary = () => {
    setSummaryCandidate(null)
    setSummaryText('')
    setSummaryError('')
  }

  const isReadyToRank = jobDescription.trim().length >= 50 && resumeFiles.length > 0

  // ─── Render ────────────────────────────────────────────────────────────

  return (
    <div className="min-h-screen py-10 px-4">
      <div className="container-section space-y-8">

        {/* Page Header */}
        <div>
          <h1 className="text-3xl font-bold text-slate-100">Recruiter Dashboard</h1>
          <p className="text-slate-500 mt-2">
            Upload resumes and rank candidates against your job description using AI.
          </p>
        </div>

        {/* ─── Job Description Input ────────────────────────────────────── */}
        <div className="glass-card p-6">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-8 h-8 rounded-full bg-primary-600 text-white flex items-center justify-center text-sm font-bold">
              1
            </div>
            <h2 className="text-slate-100 font-semibold text-lg">Paste Job Description</h2>
          </div>

          <textarea
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
            placeholder="Paste your job description here... (minimum 50 characters)

Example:
We are looking for a Senior Full Stack Developer with 5+ years of experience.
Required skills: React, Node.js, TypeScript, PostgreSQL, REST APIs.
Experience with microservices architecture and cloud deployment (AWS/GCP) is a plus..."
            rows={8}
            className="w-full bg-slate-800/60 border border-slate-700 rounded-xl px-4 py-3
                       text-slate-300 placeholder-slate-600 text-sm resize-none
                       focus:outline-none focus:border-primary-500/50 focus:ring-1 focus:ring-primary-500/20
                       transition-colors"
          />
          <div className="flex items-center justify-between mt-2">
            <span className={`text-xs ${jobDescription.length < 50 ? 'text-slate-600' : 'text-emerald-500'}`}>
              {jobDescription.length} / 50+ characters required
            </span>
          </div>
        </div>

        {/* ─── Upload Resumes ───────────────────────────────────────────── */}
        <div className="glass-card p-6">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-8 h-8 rounded-full bg-primary-600 text-white flex items-center justify-center text-sm font-bold">
              2
            </div>
            <h2 className="text-slate-100 font-semibold text-lg">Upload Candidate Resumes</h2>
          </div>

          <FileUploader
            onMultipleSelect={handleMultipleSelect}
            multiple={true}
            maxFiles={20}
            label="Upload Resumes"
            sublabel="Up to 20 PDF or DOCX files, 10MB each"
          />

          {/* Privacy Toggle */}
          <div className="mt-4 flex items-center gap-3">
            <button
              onClick={() => setMaskNames(!maskNames)}
              className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors
                ${maskNames ? 'bg-primary-600' : 'bg-slate-700'}`}
              role="switch"
              aria-checked={maskNames}
            >
              <span className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform
                ${maskNames ? 'translate-x-6' : 'translate-x-1'}`} />
            </button>
            <div className="flex items-center gap-2">
              {maskNames ? <EyeOff size={15} className="text-primary-400" /> : <Eye size={15} className="text-slate-500" />}
              <span className="text-sm text-slate-400">
                {maskNames ? 'Names masked (bias-free mode)' : 'Show candidate names'}
              </span>
            </div>
          </div>
        </div>

        {/* ─── Rank Button ──────────────────────────────────────────────── */}
        {rankError && (
          <div className="flex items-start gap-2 text-red-400 text-sm bg-red-900/20 border border-red-800/50 rounded-xl px-4 py-3">
            <AlertCircle size={16} className="shrink-0 mt-0.5" />
            <span>{rankError}</span>
          </div>
        )}

        <button
          onClick={handleRankCandidates}
          disabled={!isReadyToRank || rankLoading}
          className="btn-primary flex items-center gap-2 text-base px-8 py-4"
        >
          {rankLoading
            ? <><Loader2 size={18} className="animate-spin" /> Ranking {resumeFiles.length} candidate{resumeFiles.length !== 1 ? 's' : ''}...</>
            : <><Sparkles size={18} /> Rank Candidates</>
          }
        </button>

        {rankLoading && (
          <div className="glass-card p-6 text-center space-y-3">
            <Loader2 size={32} className="animate-spin text-primary-400 mx-auto" />
            <p className="text-slate-300 font-medium">Processing {resumeFiles.length} resumes...</p>
            <p className="text-slate-500 text-sm">
              Generating AI embeddings and computing semantic similarity.
              This may take 30-60 seconds for multiple files.
            </p>
          </div>
        )}

        {/* ─── Ranked Results ───────────────────────────────────────────── */}
        {rankedCandidates.length > 0 && (
          <CandidateRankTable
            candidates={rankedCandidates}
            onViewSummary={handleViewSummary}
          />
        )}
      </div>

      {/* ─── AI Summary Modal ─────────────────────────────────────────────── */}
      {summaryCandidate && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm">
          <div className="glass-card w-full max-w-lg p-6 relative">
            {/* Close button */}
            <button
              onClick={closeSummary}
              className="absolute top-4 right-4 text-slate-500 hover:text-slate-200 transition-colors"
            >
              <X size={20} />
            </button>

            {/* Header */}
            <div className="flex items-center gap-3 mb-4">
              <div className="w-10 h-10 bg-primary-600/20 rounded-xl flex items-center justify-center">
                <Bot size={18} className="text-primary-400" />
              </div>
              <div>
                <h3 className="text-slate-100 font-semibold">AI Executive Summary</h3>
                <p className="text-slate-500 text-sm">{summaryCandidate.name}</p>
              </div>
            </div>

            {/* Content */}
            {summaryLoading ? (
              <div className="space-y-3 py-4">
                <div className="h-4 shimmer rounded" />
                <div className="h-4 shimmer rounded w-5/6" />
                <div className="h-4 shimmer rounded w-4/5" />
              </div>
            ) : summaryError ? (
              <div className="flex items-start gap-2 text-red-400 text-sm bg-red-900/20 border border-red-800/50 rounded-xl px-4 py-3">
                <AlertCircle size={16} className="shrink-0 mt-0.5" />
                <span>{summaryError}</span>
              </div>
            ) : (
              <div className="bg-slate-800/50 rounded-xl p-4 border border-slate-700/50">
                <p className="text-slate-300 text-sm leading-relaxed">{summaryText}</p>
              </div>
            )}

            {/* Match score */}
            <div className="mt-4 flex items-center justify-between text-sm">
              <span className="text-slate-600">Match Score</span>
              <span className={`font-bold ${summaryCandidate.match_score >= 70 ? 'text-emerald-400' : 'text-primary-400'}`}>
                {Math.round(summaryCandidate.match_score)}%
              </span>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
