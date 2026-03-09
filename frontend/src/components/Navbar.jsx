import { Link, useLocation } from 'react-router-dom'
import { Briefcase, User, Zap } from 'lucide-react'

/**
 * Navbar component.
 * Displays the ResuM8 brand and navigation links.
 * Highlights the active route.
 */
export default function Navbar() {
  const location = useLocation()

  const navLinks = [
    { to: '/candidate', label: 'For Candidates', icon: User },
    { to: '/recruiter', label: 'For Recruiters', icon: Briefcase },
  ]

  return (
    <nav className="sticky top-0 z-50 bg-slate-950/80 backdrop-blur-md border-b border-slate-800">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">

          {/* Brand */}
          <Link to="/" className="flex items-center gap-2 group">
            <div className="w-8 h-8 bg-primary-600 rounded-lg flex items-center justify-center
                            group-hover:bg-primary-500 transition-colors">
              <Zap size={16} className="text-white" />
            </div>
            <span className="text-xl font-bold gradient-text">ResuM8</span>
          </Link>

          {/* Navigation Links */}
          <div className="flex items-center gap-2">
            {navLinks.map(({ to, label, icon: Icon }) => (
              <Link
                key={to}
                to={to}
                className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200
                  ${location.pathname === to
                    ? 'bg-primary-600/20 text-primary-300 border border-primary-500/30'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800'
                  }`}
              >
                <Icon size={15} />
                <span className="hidden sm:inline">{label}</span>
              </Link>
            ))}
          </div>
        </div>
      </div>
    </nav>
  )
}
