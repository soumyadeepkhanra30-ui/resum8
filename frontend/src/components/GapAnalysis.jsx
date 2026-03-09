import { CheckCircle2, XCircle, Lightbulb, ChevronDown, ChevronUp } from 'lucide-react'
import { useState } from 'react'

/**
 * GapAnalysis component.
 * Displays the AI-powered gap analysis for a candidate-job match.
 *
 * Props:
 * - analysis: { matching_skills, missing_skills, improvement_tips, summary }
 * - matchScore: number (0-100)
 * - jobTitle: string
 * - loading: boolean
 */
export default function GapAnalysis({ analysis, matchScore, jobTitle, loading }) {
  const [expanded, setExpanded] = useState(true)

  if (loading) {
    return (
      <div className="glass-card p-6 space-y-4">
        <div className="h-5 w-48 shimmer rounded-lg" />
        <div className="h-4 w-full shimmer rounded" />
        <div className="h-4 w-3/4 shimmer rounded" />
        <div className="grid grid-cols-2 gap-4 mt-4">
          <div className="h-24 shimmer rounded-xl" />
          <div className="h-24 shimmer rounded-xl" />
        </div>
      </div>
    )
  }

  if (!analysis) return null

  const { matching_skills = [], missing_skills = [], improvement_tips = [], summary = '' } = analysis

  return (
    <div className="glass-card overflow-hidden">
      {/* Header */}
      <button
        onClick={() => setExpanded(!expanded)}
        className="w-full flex items-center justify-between p-6 hover:bg-slate-800/30 transition-colors"
      >
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-primary-600/20 rounded-xl flex items-center justify-center">
            <Lightbulb size={18} className="text-primary-400" />
          </div>
          <div className="text-left">
            <h3 className="text-slate-100 font-semibold">Gap Analysis</h3>
            <p className="text-slate-500 text-sm">
              {jobTitle} — {Math.round(matchScore)}% match
            </p>
          </div>
        </div>
        {expanded ? (
          <ChevronUp size={18} className="text-slate-500" />
        ) : (
          <ChevronDown size={18} className="text-slate-500" />
        )}
      </button>

      {expanded && (
        <div className="px-6 pb-6 space-y-5 border-t border-slate-700/50 pt-5">

          {/* AI Summary */}
          {summary && (
            <div className="bg-slate-800/50 rounded-xl p-4 border border-slate-700/50">
              <p className="text-slate-300 text-sm leading-relaxed">{summary}</p>
            </div>
          )}

          {/* Skills Grid */}
          <div className="grid sm:grid-cols-2 gap-4">
            {/* Matching Skills */}
            <div className="space-y-3">
              <div className="flex items-center gap-2">
                <CheckCircle2 size={16} className="text-emerald-400" />
                <h4 className="text-emerald-400 font-semibold text-sm">
                  You Have ({matching_skills.length})
                </h4>
              </div>
              {matching_skills.length === 0 ? (
                <p className="text-slate-600 text-sm italic">No matching skills detected</p>
              ) : (
                <div className="flex flex-wrap gap-2">
                  {matching_skills.map((skill, i) => (
                    <span key={i}
                      className="px-3 py-1 bg-emerald-900/30 text-emerald-300 border border-emerald-700/50 rounded-full text-xs font-medium">
                      {skill}
                    </span>
                  ))}
                </div>
              )}
            </div>

            {/* Missing Skills */}
            <div className="space-y-3">
              <div className="flex items-center gap-2">
                <XCircle size={16} className="text-red-400" />
                <h4 className="text-red-400 font-semibold text-sm">
                  You Need ({missing_skills.length})
                </h4>
              </div>
              {missing_skills.length === 0 ? (
                <p className="text-slate-500 text-sm italic">No significant gaps detected!</p>
              ) : (
                <div className="flex flex-wrap gap-2">
                  {missing_skills.map((skill, i) => (
                    <span key={i}
                      className="px-3 py-1 bg-red-900/30 text-red-300 border border-red-700/50 rounded-full text-xs font-medium">
                      {skill}
                    </span>
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* Improvement Tips */}
          {improvement_tips.length > 0 && (
            <div className="space-y-3">
              <h4 className="text-primary-400 font-semibold text-sm flex items-center gap-2">
                <Lightbulb size={14} />
                Improvement Tips
              </h4>
              <ul className="space-y-2">
                {improvement_tips.map((tip, i) => (
                  <li key={i} className="flex items-start gap-3 text-sm text-slate-300">
                    <span className="shrink-0 w-5 h-5 bg-primary-600/20 rounded-full flex items-center justify-center text-primary-400 text-xs font-bold mt-0.5">
                      {i + 1}
                    </span>
                    {tip}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
