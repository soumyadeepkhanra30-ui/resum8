import { MapPin, Briefcase, DollarSign, Tag, ChevronRight, Star } from 'lucide-react'
import MatchScoreCard from './MatchScoreCard'

/**
 * JobCard component.
 * Displays a matched job with score, details, and a CTA to view gap analysis.
 *
 * Props:
 * - job: JobMatchResult object
 * - onViewGapAnalysis: function(job) — called when "Gap Analysis" is clicked
 * - isSelected: boolean — whether this job is currently selected
 * - isTopMatch: boolean — whether this is the #1 match
 */
export default function JobCard({ job, onViewGapAnalysis, isSelected, isTopMatch }) {
  if (!job) return null

  const {
    title, company, location, job_type, experience_level,
    salary_range, required_skills, match_score, rank
  } = job

  return (
    <div className={`glass-card p-6 transition-all duration-200 hover:border-primary-500/40
      ${isSelected ? 'border-primary-500/60 bg-primary-900/10 ring-1 ring-primary-500/30' : ''}
      ${isTopMatch ? 'border-amber-500/40' : ''}`}
    >
      <div className="flex gap-4">
        {/* Match Score */}
        <div className="shrink-0">
          <MatchScoreCard score={match_score} size="md" rank={rank} />
        </div>

        {/* Job Details */}
        <div className="flex-1 min-w-0">
          <div className="flex items-start justify-between gap-2 flex-wrap">
            <div>
              {isTopMatch && (
                <div className="flex items-center gap-1 mb-1">
                  <Star size={12} className="text-amber-400 fill-amber-400" />
                  <span className="text-amber-400 text-xs font-semibold">Top Match</span>
                </div>
              )}
              <h3 className="text-slate-100 font-semibold text-lg leading-tight">{title}</h3>
              <p className="text-slate-400 text-sm font-medium mt-0.5">{company}</p>
            </div>
          </div>

          {/* Meta Info */}
          <div className="flex flex-wrap gap-3 mt-3">
            <span className="flex items-center gap-1 text-slate-500 text-xs">
              <MapPin size={12} className="text-slate-600" />
              {location}
            </span>
            <span className="flex items-center gap-1 text-slate-500 text-xs">
              <Briefcase size={12} className="text-slate-600" />
              {job_type} · {experience_level}
            </span>
            {salary_range && (
              <span className="flex items-center gap-1 text-slate-500 text-xs">
                <DollarSign size={12} className="text-slate-600" />
                {salary_range}
              </span>
            )}
          </div>

          {/* Required Skills */}
          {required_skills && required_skills.length > 0 && (
            <div className="flex flex-wrap gap-1.5 mt-3">
              {required_skills.slice(0, 5).map((skill, i) => (
                <span key={i}
                  className="px-2.5 py-0.5 bg-slate-800 text-slate-400 border border-slate-700 rounded-full text-xs">
                  {skill}
                </span>
              ))}
              {required_skills.length > 5 && (
                <span className="px-2.5 py-0.5 text-slate-600 text-xs">
                  +{required_skills.length - 5} more
                </span>
              )}
            </div>
          )}

          {/* Actions */}
          <div className="mt-4">
            <button
              onClick={() => onViewGapAnalysis && onViewGapAnalysis(job)}
              className={`flex items-center gap-2 text-sm font-medium px-4 py-2 rounded-lg transition-all duration-200
                ${isSelected
                  ? 'bg-primary-600 text-white shadow-lg shadow-primary-900/30'
                  : 'bg-slate-800 text-primary-400 hover:bg-primary-600/20 border border-slate-700 hover:border-primary-500/50'
                }`}
            >
              <Tag size={14} />
              {isSelected ? 'Viewing Gap Analysis' : 'See Gap Analysis'}
              {!isSelected && <ChevronRight size={14} />}
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
