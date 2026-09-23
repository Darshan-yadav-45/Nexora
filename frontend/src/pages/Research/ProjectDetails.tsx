import React, { useState, useEffect, useRef } from 'react';
import { useParams, Link } from 'react-router-dom';
import { 
  ArrowLeft, FileText, Upload, Trash2, 
  BookOpen, Plus, Loader2, Save, File, MessageSquare
} from 'lucide-react';
import { researchService, type ResearchProject, type ResearchPaper } from '../../services/research';

const ProjectDetails = () => {
  const { projectId } = useParams<{ projectId: string }>();
  const [project, setProject] = useState<ResearchProject | null>(null);
  const [loading, setLoading] = useState(true);
  
  // File upload state
  const [isUploading, setIsUploading] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);
  
  // Literature review state
  const [litReviewContent, setLitReviewContent] = useState('');
  const [isSavingLitReview, setIsSavingLitReview] = useState(false);
  
  // Note modal state
  const [isNoteModalOpen, setIsNoteModalOpen] = useState(false);
  const [activePaperId, setActivePaperId] = useState<string | null>(null);
  const [noteContent, setNoteContent] = useState('');
  const [notePageNumber, setNotePageNumber] = useState('');

  useEffect(() => {
    if (projectId) {
      loadProject(projectId);
    }
  }, [projectId]);

  const loadProject = async (id: string) => {
    try {
      setLoading(true);
      const data = await researchService.getProject(id);
      setProject(data);
      if (data.literature_review) {
        setLitReviewContent(data.literature_review.content || '');
      }
    } catch (error) {
      console.error('Failed to load project', error);
    } finally {
      setLoading(false);
    }
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file || !project) return;
    
    setIsUploading(true);
    const formData = new FormData();
    formData.append('file', file);
    formData.append('title', file.name.replace('.pdf', ''));
    
    try {
      await researchService.uploadPaper(project.id, formData);
      await loadProject(project.id);
    } catch (error) {
      console.error('Failed to upload paper', error);
    } finally {
      setIsUploading(false);
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    }
  };

  const handleDeletePaper = async (paperId: string) => {
    if (!confirm('Are you sure you want to delete this paper?')) return;
    try {
      await researchService.deletePaper(paperId);
      if (project) {
        await loadProject(project.id);
      }
    } catch (error) {
      console.error('Failed to delete paper', error);
    }
  };

  const handleSaveLitReview = async () => {
    if (!project) return;
    setIsSavingLitReview(true);
    try {
      await researchService.updateLiteratureReview(project.id, litReviewContent);
      // Show success indicator here if desired
    } catch (error) {
      console.error('Failed to save literature review', error);
    } finally {
      setIsSavingLitReview(false);
    }
  };

  const handleAddNote = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!activePaperId || !noteContent.trim() || !project) return;

    try {
      await researchService.addNote(activePaperId, noteContent, notePageNumber);
      setIsNoteModalOpen(false);
      setNoteContent('');
      setNotePageNumber('');
      await loadProject(project.id);
    } catch (error) {
      console.error('Failed to add note', error);
    }
  };

  if (loading) {
    return (
      <div className="flex-1 flex justify-center items-center bg-[#0a0a0a]">
        <Loader2 className="w-8 h-8 text-purple-500 animate-spin" />
      </div>
    );
  }

  if (!project) {
    return (
      <div className="flex-1 flex justify-center items-center bg-[#0a0a0a]">
        <div className="text-center">
          <h2 className="text-2xl font-bold mb-2">Project Not Found</h2>
          <Link to="/research" className="text-purple-400 hover:underline">Return to Workspace</Link>
        </div>
      </div>
    );
  }

  return (
    <div className="flex-1 overflow-y-auto bg-[#0a0a0a] min-h-screen pb-12">
      {/* Header */}
      <div className="sticky top-0 z-30 bg-[#0a0a0a]/80 backdrop-blur-md border-b border-white/10 px-4 sm:px-8 py-4">
        <div className="max-w-7xl mx-auto flex items-center gap-4">
          <Link to="/research" className="p-2 text-gray-400 hover:text-white rounded-lg hover:bg-white/5 transition-colors">
            <ArrowLeft className="w-5 h-5" />
          </Link>
          <div>
            <h1 className="text-xl font-bold line-clamp-1">{project.title}</h1>
            <p className="text-sm text-gray-500">Research Project</p>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-8 mt-8 grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* Left Column: Papers Library */}
        <div className="lg:col-span-1 space-y-6">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-semibold flex items-center gap-2">
              <BookOpen className="w-5 h-5 text-purple-400" />
              Library ({project.papers.length})
            </h2>
            <button 
              onClick={() => fileInputRef.current?.click()}
              disabled={isUploading}
              className="p-2 text-purple-400 hover:text-white bg-purple-500/10 hover:bg-purple-500/20 rounded-lg transition-colors disabled:opacity-50"
            >
              {isUploading ? <Loader2 className="w-5 h-5 animate-spin" /> : <Upload className="w-5 h-5" />}
            </button>
            <input 
              type="file" 
              ref={fileInputRef} 
              onChange={handleFileUpload} 
              className="hidden" 
              accept="application/pdf"
            />
          </div>

          <div className="space-y-4">
            {project.papers.length === 0 ? (
              <div className="text-center p-8 bg-[#111] border border-white/5 rounded-2xl border-dashed">
                <FileText className="w-12 h-12 text-gray-700 mx-auto mb-3" />
                <p className="text-gray-400 text-sm">No papers uploaded yet.</p>
              </div>
            ) : (
              project.papers.map((paper: ResearchPaper) => (
                <div key={paper.id} className="bg-[#111] border border-white/5 rounded-2xl p-4 group">
                  <div className="flex justify-between items-start">
                    <div className="flex items-start gap-3 flex-1 min-w-0">
                      <File className="w-8 h-8 text-red-400 shrink-0 mt-1" />
                      <div className="flex-1 min-w-0">
                        <h4 className="font-medium text-sm text-white truncate" title={paper.title}>
                          {paper.title}
                        </h4>
                        <p className="text-xs text-gray-500 mt-1 flex items-center gap-2">
                          <MessageSquare className="w-3 h-3" />
                          {paper.notes.length} notes
                        </p>
                      </div>
                    </div>
                    <button 
                      onClick={() => handleDeletePaper(paper.id)}
                      className="p-1.5 text-gray-500 hover:text-red-400 hover:bg-red-400/10 rounded-lg transition-colors opacity-0 group-hover:opacity-100"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                  
                  {/* Actions */}
                  <div className="mt-4 pt-4 border-t border-white/5 flex gap-2">
                    {paper.file_url && (
                      <a 
                        href={`http://localhost:8000${paper.file_url}`} 
                        target="_blank" 
                        rel="noopener noreferrer"
                        className="flex-1 text-center py-1.5 bg-white/5 hover:bg-white/10 rounded-lg text-xs font-medium transition-colors"
                      >
                        View PDF
                      </a>
                    )}
                    <button 
                      onClick={() => { setActivePaperId(paper.id); setIsNoteModalOpen(true); }}
                      className="flex-1 text-center py-1.5 bg-purple-500/10 hover:bg-purple-500/20 text-purple-400 rounded-lg text-xs font-medium transition-colors"
                    >
                      Add Note
                    </button>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Right Column: Literature Review & Notes */}
        <div className="lg:col-span-2 space-y-6">
          <div className="bg-[#111] border border-white/5 rounded-2xl flex flex-col h-[600px] shadow-xl">
            <div className="flex items-center justify-between p-4 border-b border-white/5">
              <h2 className="text-lg font-semibold flex items-center gap-2">
                <FileText className="w-5 h-5 text-purple-400" />
                Literature Review Draft
              </h2>
              <button 
                onClick={handleSaveLitReview}
                disabled={isSavingLitReview}
                className="flex items-center gap-2 px-4 py-2 bg-purple-600 hover:bg-purple-500 disabled:bg-purple-600/50 text-white text-sm font-medium rounded-lg transition-colors"
              >
                {isSavingLitReview ? <Loader2 className="w-4 h-4 animate-spin" /> : <Save className="w-4 h-4" />}
                Save Draft
              </button>
            </div>
            <textarea
              value={litReviewContent}
              onChange={(e) => setLitReviewContent(e.target.value)}
              placeholder="Synthesize your findings here. What are the main themes, gaps, and conclusions across your reading?"
              className="flex-1 w-full p-6 bg-transparent resize-none text-gray-300 placeholder-gray-600 focus:outline-none leading-relaxed"
            />
          </div>
          
          {/* Recent Notes Section could go here in a full implementation */}
        </div>
      </div>

      {/* Add Note Modal */}
      {isNoteModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
          <div className="absolute inset-0 bg-black/80 backdrop-blur-sm" onClick={() => setIsNoteModalOpen(false)} />
          <div className="relative bg-[#111] border border-white/10 rounded-2xl w-full max-w-lg p-6 shadow-2xl">
            <h2 className="text-xl font-bold mb-6">Add Note to Paper</h2>
            <form onSubmit={handleAddNote} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">Note Content</label>
                <textarea
                  required
                  value={noteContent}
                  onChange={(e) => setNoteContent(e.target.value)}
                  className="w-full px-4 py-2.5 bg-black/50 border border-white/10 rounded-xl text-white placeholder-gray-500 focus:outline-none focus:border-purple-500 focus:ring-1 focus:ring-purple-500 h-32 resize-none"
                  placeholder="Key takeaways, methodology critique, etc."
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">Page Number (Optional)</label>
                <input
                  type="text"
                  value={notePageNumber}
                  onChange={(e) => setNotePageNumber(e.target.value)}
                  className="w-full px-4 py-2.5 bg-black/50 border border-white/10 rounded-xl text-white placeholder-gray-500 focus:outline-none focus:border-purple-500 focus:ring-1 focus:ring-purple-500"
                  placeholder="e.g. 42"
                />
              </div>
              <div className="flex justify-end gap-3 mt-8">
                <button
                  type="button"
                  onClick={() => setIsNoteModalOpen(false)}
                  className="px-5 py-2.5 bg-white/5 hover:bg-white/10 text-white font-medium rounded-xl transition-all"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={!noteContent.trim()}
                  className="px-5 py-2.5 bg-purple-600 hover:bg-purple-500 disabled:opacity-50 text-white font-medium rounded-xl transition-all"
                >
                  Save Note
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default ProjectDetails;
