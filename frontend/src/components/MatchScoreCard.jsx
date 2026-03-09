/**
 * MatchScoreCard component.
 * Displays a circular progress indicator showing the match percentage.
 *
 * Props:
 * - score: number (0-100)
 * - size: 'sm' | 'md' | 'lg' (default: 'md')
 * - showLabel: boolean (default: true)
 * - rank: number (optional, shows rank badge)
 */
export default function MatchScoreCard({ score = 0, size = 'md', showLabel = true, rank }) {
  // Determine color based on score
  const getColor = (s) => {
    if (s >= 80) return { stroke: '#10b981', text: 'text-emerald-400', bg: 'bg-emerald-400/10', label: 'Excellent Match' }
    if (s >= 65) return { stroke: '#6366f1', text: 'text-primary-400', bg: 'bg-primary-400/10', label: 'Good Match' }
    if (s >= 50) return { stroke: '#f59e0b', text: 'text-amber-400', bg: 'bg-amber-400/10', label: 'Fair Match' }
    return { stroke: '#ef4444', text: 'text-red-400', bg: 'bg-red-400/10', label: 'Low Match' }
  }

  const { stroke, text, bg, label } = getColor(score)

  const sizes = {
    sm: { width: 64, height: 64, r: 24, strokeWidth: 4, fontSize: 'text-xs', fontWeight: 'font-bold' },
    md: { width: 96, height: 96, r: 38, strokeWidth: 6, fontSize: 'text-sm', fontWeight: 'font-bold' },
    lg: { width: 140, height: 140, r: 56, strokeWidth: 8, fontSize: 'text-xl', fontWeight: 'font-extrabold' },
  }

  const { width, height, r, strokeWidth, fontSize, fontWeight } = sizes[size]
  const circumference = 2 * Math.PI * r
  const progress = ((100 - score) / 100) * circumference

  return (
    <div className="flex flex-col items-center gap-2">
      {/* Rank badge */}
      {rank && (
        <div className="flex items-center justify-center w-6 h-6 bg-slate-700 rounded-full text-xs font-bold text-slate-300">
          #{rank}
        </div>
      )}

      {/* Circular SVG */}
      <div className={`relative ${bg} rounded-full p-1`}>
        <svg width={width} height={height} viewBox={`0 0 ${width} ${height}`}>
          {/* Background circle */}
          <circle
            cx={width / 2}
            cy={height / 2}
            r={r}
            fill="none"
            stroke="#1e293b"
            strokeWidth={strokeWidth}
          />
          {/* Progress circle */}
          <circle
            cx={width / 2}
            cy={height / 2}
            r={r}
            fill="none"
            stroke={stroke}
            strokeWidth={strokeWidth}
            strokeLinecap="round"
            strokeDasharray={circumference}
            strokeDashoffset={progress}
            className="circular-progress transition-all duration-1000 ease-out"
          />
          {/* Score text */}
          <text
            x="50%"
            y="50%"
            textAnchor="middle"
            dominantBaseline="central"
            fill={stroke}
            className={`${fontSize} ${fontWeight} font-mono`}
          >
            {Math.round(score)}%
          </text>
        </svg>
      </div>

      {/* Label */}
      {showLabel && (
        <span className={`text-xs font-medium ${text}`}>{label}</span>
      )}
    </div>
  )
}
