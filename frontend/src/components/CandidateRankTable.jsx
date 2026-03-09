import { useState } from 'react'
import { ChevronUp, ChevronDown, Eye, EyeOff, FileText, ChevronRight } from 'lucide-react'
import MatchScoreCard from './MatchScoreCard'

/**
 * CandidateRankTable component.
 * Sortable table of ranked candidates for the recruiter dashboard.
 *
 * Props:
 * - candidates: array of CandidateRankResult
 * - onViewSummary: function(candidate) — called when "View Summary" is clicked
 * - loading: boolean
 */
export default function CandidateRankTable({ candidates = [], onViewSummary, loading }) {
  const [sortField, setSortField] = useState('rank')
  const [sortDir, setSortDir] = useState('asc')
  const [showResumes, setShowResumes] = useState({})

  if (loading) {
    return (
      <div className="glass-card p-6 space-y-4">
        <div className="h-6 w-48 shimmer rounded-lg" />
        {[1, 2, 3].map(i => (
          <div key={i} className="flex items-center gap-4 p-4 bg-slate-800/40 rounded-xl">
            <div className="w-16 h-16 shimmer rounded-full" />
            <div className="flex-1 space-y-2">
              <div className="h-4 w-32 shimmer rounded" />
              <div className="h-3 w-24 shimmer rounded" />
            </div>
            <div className="h-8 w-28 shimmer rounded-lg" />
          </div>
        ))}
      </div>
    )
  }

  if (!candidates || candidates.length === 0) return null

  // Sort
  const sorted = [...candidates].sort((a, b) => {
    let aVal = a[sortField]
    let bVal = b[sortField]
    if (typeof aVal === 'string') aVal = aVal.toLowerCase()
    if (typeof bVal === 'string') bVal = bVal.toLowerCase()
    if (aVal < bVal) return sortDir === 'asc' ? -1 : 1
    if (aVal > bVal) return sortDir === 'asc' ? 1 : -1
    return 0
  })

  const handleSort = (field) => {
    if (sortField === field) {
      setSortDir(d => d === 'asc' ? 'desc' : 'asc')
    } else {
      setSortField(field)
      setSortDir(field === 'match_score' ? 'desc' : 'asc')
    }
  }

  const SortIcon = ({ field }) => {
    if (sortField !== field) return <ChevronUp size={12} className="text-slate-700" />
    return sortDir === 'asc'
      ? <ChevronUp size={12} className="text-primary-400" />
      : <ChevronDown size={12} className="text-primary-400" />
  }

  const toggleResume = (id) => {
    setShowResumes(prev => ({ ...prev, [id]: !prev[id] }))
  }

  return (
    <div className="glass-card overflow-hidden">
      {/* Header */}
      <div className="px-6 py-4 border-b border-slate-700/50">
        <h3 className="text-slate-100 font-semibold text-lg">Ranked Candidates</h3>
        <p className="text-slate-500 text-sm">{candidates.length} candidates • sorted by match score</p>
      </div>

      {/* Table */}
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="border-b border-slate-800">
              <th className="text-left px-6 py-3">
                <button onClick={() => handleSort('rank')}
                  className="flex items-center gap-1 text-slate-500 text-xs font-semibold uppercase tracking-wider hover:text-slate-300">
                  Rank <SortIcon field="rank" />
                </button>
              </th>
              <th className="text-left px-6 py-3">
                <button onClick={() => handleSort('name')}
                  className="flex items-center gap-1 text-slate-500 text-xs font-semibold uppercase tracking-wider hover:text-slate-300">
                  Candidate <SortIcon field="name" />
                </button>
              </th>
              <th className="text-left px-6 py-3">
                <button onClick={() => handleSort('match_score')}
                  className="flex items-center gap-1 text-slate-500 text-xs font-semibold uppercase tracking-wider hover:text-slate-300">
                  Match Score <SortIcon field="match_score" />
                </button>
              </th>
              <th className="text-left px-6 py-3 hidden md:table-cell">
                <span className="text-slate-500 text-xs font-semibold uppercase tracking-wider">Resume</span>
              </th>
              <th className="text-left px-6 py-3">
                <span className="text-slate-500 text-xs font-semibold uppercase tracking-wider">Actions</span>
              </th>
            </tr>
          </thead>
          <tbody>
            {sorted.map((candidate, index) => (
              <>
                <tr key={candidate.candidate_id}
                  className="border-b border-slate-800/50 hover:bg-slate-800/30 transition-colors">
                  {/* Rank */}
                  <td className="px-6 py-4">
                    <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold
                      ${index === 0 ? 'bg-amber-500/20 text-amber-400 border border-amber-500/30' :
                        index === 1 ? 'bg-slate-600/20 text-slate-300 border border-slate-600/30' :
                        index === 2 ? 'bg-orange-700/20 text-orange-400 border border-orange-700/30' :
                        'bg-slate-800 text-slate-500'}`}>
                      {candidate.rank}
                    </div>
                  </td>

                  {/* Name */}
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-3">
                      <div className="w-9 h-9 bg-primary-600/20 rounded-xl flex items-center justify-center">
                        <span className="text-primary-400 text-sm font-semibold">
                          {candidate.name ? candidate.name[0].toUpperCase() : '?'}
                        </span>
                      </div>
                      <div>
                        <p className="text-slate-200 font-medium text-sm">{candidate.name}</p>
                        {candidate.email && (
                          <p className="text-slate-500 text-xs">{candidate.email}</p>
                        )}
                        {candidate.is_masked && (
                          <span className="text-xs text-amber-500/70 flex items-center gap-1 mt-0.5">
                            <EyeOff size={10} /> Masked
                          </span>
                        )}
                      </div>
                    </div>
                  </td>

                  {/* Match Score */}
                  <td className="px-6 py-4">
                    <MatchScoreCard score={candidate.match_score} size="sm" showLabel={false} />
                  </td>

                  {/* Resume preview toggle */}
                  <td className="px-6 py-4 hidden md:table-cell">
                    <button
                      onClick={() => toggleResume(candidate.candidate_id)}
                      className="flex items-center gap-1.5 text-slate-500 hover:text-primary-400 text-xs transition-colors"
                    >
                      <FileText size={13} />
                      {showResumes[candidate.candidate_id] ? 'Hide' : 'Preview'}
                      {showResumes[candidate.candidate_id]
                        ? <ChevronUp size={12} /> : <ChevronDown size={12} />}
                    </button>
                  </td>

                  {/* Actions */}
                  <td className="px-6 py-4">
                    <button
                      onClick={() => onViewSummary && onViewSummary(candidate)}
                      className="flex items-center gap-1.5 px-3 py-1.5 bg-slate-800 hover:bg-primary-600/20
                                 text-slate-300 hover:text-primary-300 text-xs font-medium rounded-lg
                                 border border-slate-700 hover:border-primary-500/40 transition-all"
                    >
                      AI Summary <ChevronRight size={12} />
                    </button>
                  </td>
                </tr>

                {/* Resume Preview Row */}
                {showResumes[candidate.candidate_id] && (
                  <tr key={`${candidate.candidate_id}-resume`} className="bg-slate-900/30">
                    <td colSpan={5} className="px-6 py-4">
                      <div className="bg-slate-800/50 rounded-xl p-4 border border-slate-700/50 max-h-48 overflow-y-auto">
                        <pre className="text-slate-400 text-xs whitespace-pre-wrap font-sans leading-relaxed">
                          {candidate.resume_text
                            ? candidate.resume_text.substring(0, 1000) + (candidate.resume_text.length > 1000 ? '...' : '')
                            : 'No resume text available'
                          }
                        </pre>
                      </div>
                    </td>
                  </tr>
                )}
              </>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
