import { Link } from 'react-router-dom'
import { User, Briefcase, Zap, ArrowRight, Brain, BarChart3, Shield, Search } from 'lucide-react'

/**
 * HomePage — Landing page with role selection.
 * Users choose whether they are a Candidate or Recruiter.
 */
export default function HomePage() {
  const features = [
    {
      icon: Brain,
      title: 'AI-Powered Matching',
      desc: 'Google Gemini embeddings understand "MERN Stack" matches "Full Stack Developer" — no keyword tricks.',
    },
    {
      icon: BarChart3,
      title: 'Match Scores',
      desc: 'Get a precise percentage match for every job or candidate. See exactly where you stand.',
    },
    {
      icon: Search,
      title: 'Gap Analysis',
      desc: 'Know exactly which skills you need to close the gap and land your dream role.',
    },
    {
      icon: Shield,
      title: 'Bias-Free Screening',
      desc: 'Recruiters can anonymize candidate names for fair, skills-first evaluation.',
    },
  ]

  return (
    <div className="min-h-screen">
      {/* ─── Hero ─────────────────────────────────────────────────────────── */}
      <section className="relative py-24 px-4 overflow-hidden">
        {/* Background glow */}
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
          <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px]
                          bg-primary-600/10 rounded-full blur-3xl" />
        </div>

        <div className="container-section relative z-10 text-center">
          {/* Badge */}
          <div className="inline-flex items-center gap-2 px-4 py-1.5 bg-primary-600/10 border border-primary-500/30
                          rounded-full text-primary-400 text-sm font-medium mb-8">
            <Zap size={14} className="fill-primary-400" />
            Powered by Google Gemini AI
          </div>

          {/* Headline */}
          <h1 className="text-5xl sm:text-6xl lg:text-7xl font-extrabold leading-tight mb-6">
            <span className="text-slate-100">The Smarter Way</span>
            <br />
            <span className="gradient-text">to Match Talent</span>
          </h1>

          <p className="text-slate-400 text-xl max-w-2xl mx-auto mb-12 leading-relaxed">
            ResuM8 uses semantic AI to match resumes to jobs with precision.
            Not keyword counting — actual understanding of skills and experience.
          </p>

          {/* Role Selection CTAs */}
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link to="/candidate"
              className="group flex items-center gap-3 w-full sm:w-auto
                         bg-gradient-to-r from-primary-600 to-primary-500 hover:from-primary-500 hover:to-primary-400
                         text-white font-semibold px-8 py-4 rounded-2xl transition-all duration-200
                         shadow-xl shadow-primary-900/40 hover:shadow-primary-700/40 hover:scale-[1.02]">
              <div className="w-9 h-9 bg-white/20 rounded-xl flex items-center justify-center">
                <User size={18} />
              </div>
              <div className="text-left">
                <div className="text-xs text-primary-200 font-normal">I'm a job seeker</div>
                <div>Find Matching Jobs</div>
              </div>
              <ArrowRight size={18} className="ml-2 group-hover:translate-x-1 transition-transform" />
            </Link>

            <Link to="/recruiter"
              className="group flex items-center gap-3 w-full sm:w-auto
                         bg-slate-800 hover:bg-slate-700 text-slate-100 font-semibold px-8 py-4 rounded-2xl
                         transition-all duration-200 border border-slate-700 hover:border-slate-500
                         hover:scale-[1.02]">
              <div className="w-9 h-9 bg-slate-700 rounded-xl flex items-center justify-center">
                <Briefcase size={18} className="text-slate-300" />
              </div>
              <div className="text-left">
                <div className="text-xs text-slate-500 font-normal">I'm hiring</div>
                <div>Rank Candidates</div>
              </div>
              <ArrowRight size={18} className="ml-2 group-hover:translate-x-1 transition-transform" />
            </Link>
          </div>
        </div>
      </section>

      {/* ─── Features ─────────────────────────────────────────────────────── */}
      <section className="py-20 px-4 border-t border-slate-800">
        <div className="container-section">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-slate-100 mb-4">Why ResuM8?</h2>
            <p className="text-slate-500 max-w-xl mx-auto">
              Traditional job matching fails because it relies on keywords.
              ResuM8 understands context, synonyms, and semantics.
            </p>
          </div>

          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {features.map((f, i) => (
              <div key={i} className="glass-card p-6 hover:border-primary-500/30 transition-all duration-200
                                       hover:bg-primary-900/5">
                <div className="w-11 h-11 bg-primary-600/20 rounded-xl flex items-center justify-center mb-4">
                  <f.icon size={20} className="text-primary-400" />
                </div>
                <h3 className="text-slate-100 font-semibold mb-2">{f.title}</h3>
                <p className="text-slate-500 text-sm leading-relaxed">{f.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ─── How It Works ─────────────────────────────────────────────────── */}
      <section className="py-20 px-4 border-t border-slate-800">
        <div className="container-section">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-slate-100 mb-4">How It Works</h2>
          </div>

          <div className="grid md:grid-cols-2 gap-8">
            {/* Candidate Flow */}
            <div className="glass-card p-6">
              <div className="flex items-center gap-3 mb-6">
                <div className="w-10 h-10 bg-primary-600 rounded-xl flex items-center justify-center">
                  <User size={18} className="text-white" />
                </div>
                <h3 className="text-slate-100 font-bold text-lg">For Candidates</h3>
              </div>
              <ol className="space-y-4">
                {[
                  ['Upload', 'your resume (PDF or DOCX)'],
                  ['AI Parses', 'and understands your skills and experience'],
                  ['Gemini Matches', 'your profile to 50+ real job listings semantically'],
                  ['See Your Score', 'and get gap analysis for each matched job'],
                ].map(([step, desc], i) => (
                  <li key={i} className="flex items-start gap-3">
                    <span className="shrink-0 w-6 h-6 bg-primary-600 rounded-full flex items-center justify-center
                                     text-white text-xs font-bold mt-0.5">{i + 1}</span>
                    <p className="text-slate-400 text-sm">
                      <span className="text-slate-200 font-medium">{step}</span> {desc}
                    </p>
                  </li>
                ))}
              </ol>
              <Link to="/candidate" className="btn-primary mt-6 inline-flex items-center gap-2 w-full justify-center">
                Get Started <ArrowRight size={16} />
              </Link>
            </div>

            {/* Recruiter Flow */}
            <div className="glass-card p-6">
              <div className="flex items-center gap-3 mb-6">
                <div className="w-10 h-10 bg-slate-700 rounded-xl flex items-center justify-center">
                  <Briefcase size={18} className="text-slate-300" />
                </div>
                <h3 className="text-slate-100 font-bold text-lg">For Recruiters</h3>
              </div>
              <ol className="space-y-4">
                {[
                  ['Paste', 'your job description'],
                  ['Upload', 'up to 20 candidate resumes at once'],
                  ['AI Ranks', 'candidates from highest to lowest match'],
                  ['Get Summaries', 'AI-written executive summaries per candidate'],
                ].map(([step, desc], i) => (
                  <li key={i} className="flex items-start gap-3">
                    <span className="shrink-0 w-6 h-6 bg-slate-600 rounded-full flex items-center justify-center
                                     text-white text-xs font-bold mt-0.5">{i + 1}</span>
                    <p className="text-slate-400 text-sm">
                      <span className="text-slate-200 font-medium">{step}</span> {desc}
                    </p>
                  </li>
                ))}
              </ol>
              <Link to="/recruiter" className="btn-secondary mt-6 inline-flex items-center gap-2 w-full justify-center">
                Start Ranking <ArrowRight size={16} />
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* ─── Footer ───────────────────────────────────────────────────────── */}
      <footer className="py-8 px-4 border-t border-slate-800 text-center">
        <p className="text-slate-600 text-sm">
          Built with ❤️ using FastAPI, React, and Google Gemini AI · All free-tier tools
        </p>
      </footer>
    </div>
  )
}
