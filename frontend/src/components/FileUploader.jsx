import { useCallback, useState } from 'react'
import { Upload, FileText, X, CheckCircle2, AlertCircle } from 'lucide-react'

/**
 * FileUploader component — Drag & drop file upload with validation.
 *
 * Props:
 * - onFileSelect(file): called when a valid file is selected
 * - accept: file accept string (default: ".pdf,.docx")
 * - multiple: allow multiple file selection (default: false)
 * - maxFiles: max files when multiple=true (default: 20)
 * - label: label text
 */

const ALLOWED_TYPES = [
  'application/pdf',
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
]
const MAX_SIZE_MB = 10

function validateFile(file) {
  if (!ALLOWED_TYPES.includes(file.type) && !file.name.match(/\.(pdf|docx)$/i)) {
    return 'Only PDF and DOCX files are supported'
  }
  if (file.size > MAX_SIZE_MB * 1024 * 1024) {
    return `File size must be under ${MAX_SIZE_MB}MB`
  }
  return null
}

export default function FileUploader({
  onFileSelect,
  onMultipleSelect,
  accept = '.pdf,.docx',
  multiple = false,
  maxFiles = 20,
  label = 'Upload Resume',
  sublabel = 'PDF or DOCX, max 10MB',
}) {
  const [isDragging, setIsDragging] = useState(false)
  const [selectedFiles, setSelectedFiles] = useState([])
  const [error, setError] = useState('')

  const handleFiles = useCallback((files) => {
    setError('')
    const fileArray = Array.from(files)

    if (multiple) {
      if (fileArray.length > maxFiles) {
        setError(`Maximum ${maxFiles} files allowed`)
        return
      }
      const errors = fileArray.map(validateFile).filter(Boolean)
      if (errors.length > 0) {
        setError(errors[0])
        return
      }
      setSelectedFiles(fileArray)
      onMultipleSelect && onMultipleSelect(fileArray)
    } else {
      const file = fileArray[0]
      const err = validateFile(file)
      if (err) {
        setError(err)
        return
      }
      setSelectedFiles([file])
      onFileSelect && onFileSelect(file)
    }
  }, [multiple, maxFiles, onFileSelect, onMultipleSelect])

  const handleDragEnter = (e) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragging(true)
  }

  const handleDragLeave = (e) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragging(false)
  }

  const handleDragOver = (e) => {
    e.preventDefault()
    e.stopPropagation()
  }

  const handleDrop = (e) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragging(false)
    const { files } = e.dataTransfer
    if (files && files.length > 0) {
      handleFiles(files)
    }
  }

  const handleInputChange = (e) => {
    if (e.target.files && e.target.files.length > 0) {
      handleFiles(e.target.files)
    }
  }

  const removeFile = (index) => {
    const updated = selectedFiles.filter((_, i) => i !== index)
    setSelectedFiles(updated)
    if (multiple) {
      onMultipleSelect && onMultipleSelect(updated)
    } else {
      onFileSelect && onFileSelect(null)
    }
  }

  const formatFileSize = (bytes) => {
    if (bytes < 1024) return `${bytes} B`
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
  }

  return (
    <div className="w-full">
      {/* Drop Zone */}
      <div
        onDragEnter={handleDragEnter}
        onDragLeave={handleDragLeave}
        onDragOver={handleDragOver}
        onDrop={handleDrop}
        className={`relative border-2 border-dashed rounded-2xl p-8 text-center cursor-pointer transition-all duration-200
          ${isDragging
            ? 'border-primary-400 bg-primary-900/20 scale-[1.01]'
            : 'border-slate-700 hover:border-slate-500 hover:bg-slate-800/50'
          }`}
        onClick={() => document.getElementById('file-input-hidden').click()}
      >
        <input
          id="file-input-hidden"
          type="file"
          accept={accept}
          multiple={multiple}
          onChange={handleInputChange}
          className="hidden"
        />

        <div className="flex flex-col items-center gap-3">
          <div className={`w-14 h-14 rounded-2xl flex items-center justify-center
            ${isDragging ? 'bg-primary-600' : 'bg-slate-800'}`}>
            <Upload size={24} className={isDragging ? 'text-white' : 'text-slate-400'} />
          </div>
          <div>
            <p className="text-slate-200 font-semibold text-lg">{label}</p>
            <p className="text-slate-500 text-sm mt-1">{sublabel}</p>
            {multiple && (
              <p className="text-slate-600 text-xs mt-1">Up to {maxFiles} files</p>
            )}
          </div>
          <p className="text-slate-600 text-xs">
            Drag & drop here, or <span className="text-primary-400 underline">browse</span>
          </p>
        </div>
      </div>

      {/* Error Message */}
      {error && (
        <div className="mt-3 flex items-center gap-2 text-red-400 text-sm bg-red-900/20 border border-red-800/50 rounded-lg px-4 py-2">
          <AlertCircle size={16} className="shrink-0" />
          {error}
        </div>
      )}

      {/* Selected Files List */}
      {selectedFiles.length > 0 && (
        <div className="mt-4 space-y-2">
          {selectedFiles.map((file, index) => (
            <div key={index}
              className="flex items-center gap-3 bg-slate-800/60 border border-slate-700 rounded-xl px-4 py-3">
              <div className="w-9 h-9 bg-primary-600/20 rounded-lg flex items-center justify-center shrink-0">
                <FileText size={16} className="text-primary-400" />
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-slate-200 text-sm font-medium truncate">{file.name}</p>
                <p className="text-slate-500 text-xs">{formatFileSize(file.size)}</p>
              </div>
              <div className="flex items-center gap-2 shrink-0">
                <CheckCircle2 size={16} className="text-accent-400" />
                <button
                  onClick={(e) => { e.stopPropagation(); removeFile(index) }}
                  className="text-slate-500 hover:text-red-400 transition-colors"
                  aria-label="Remove file"
                >
                  <X size={16} />
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
