import React, { useState, useEffect } from 'react';
import {
  Sparkles, Plus, Search, BookOpen, FileText, Upload, Trash2,
  ChevronLeft, ChevronRight, Download, Send, Pin, Bookmark
} from 'lucide-react';
import api from '../services/api';

export default function Research() {
  // Navigation / Selected View: null (Notebooks List) or notebook object
  const [selectedNotebook, setSelectedNotebook] = useState<any | null>(null);
  const [notebooks, setNotebooks] = useState<any[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // --- Create Notebook Modal State (Title ONLY required!) ---
  const [createModalOpen, setCreateModalOpen] = useState(false);
  const [newTitle, setNewTitle] = useState('');
  const [newDomain, setNewDomain] = useState('Computer Science & AI');
  const [newDescription, setNewDescription] = useState('');

  // --- 3-Panel Workspace States ---
  const [addSourceModalOpen, setAddSourceModalOpen] = useState(false);
  const [addSourceType, setAddSourceType] = useState<'file' | 'paste' | 'url'>('file');
  const [pastedTitle, setPastedTitle] = useState('');
  const [pastedContent, setPastedContent] = useState('');
  const [urlInput, setUrlInput] = useState('');

  // Center Panel: Chat
  const [chatMessages, setChatMessages] = useState<any[]>([
    {
      role: 'assistant',
      content: 'Welcome to your AI Research Notebook. Upload papers or paste text in the Sources panel on the left to ask questions grounded strictly in your references with exact page citations.',
      is_source_grounded: true,
      citations: []
    }
  ]);
  const [chatInput, setChatInput] = useState('');
  const [generalAiMode, setGeneralAiMode] = useState(false);
  const [chatLoading, setChatLoading] = useState(false);

  // Right Panel: Studio & Humanize Tools
  const [rightPanelTab, setRightPanelTab] = useState<'studio' | 'humanize' | 'notes'>('studio');
  const [activeStudioTool, setActiveStudioTool] = useState<string>('summary');
  const [studioOutput, setStudioOutput] = useState<any | null>(null);
  const [studioLoading, setStudioLoading] = useState(false);

  // Humanize Tool State
  const [humanizeInput, setHumanizeInput] = useState('');
  const [humanizeMode, setHumanizeMode] = useState('natural_human');
  const [humanizeOutput, setHumanizeOutput] = useState<any | null>(null);
  const [humanizeLoading, setHumanizeLoading] = useState(false);

  // Collapse/Expand side panels
  const [leftPanelOpen, setLeftPanelOpen] = useState(true);
  const [rightPanelOpen, setRightPanelOpen] = useState(true);

  // Fetch Notebooks on Mount
  useEffect(() => {
    fetchNotebooks();
  }, []);

  const fetchNotebooks = async () => {
    setLoading(true);
    try {
      const res = await api.get('/notebooks');
      setNotebooks(res.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to fetch research notebooks');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateNotebook = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTitle.trim()) return;

    setLoading(true);
    setError(null);
    try {
      const res = await api.post('/notebooks', {
        title: newTitle.trim(),
        description: newDescription.trim() || undefined,
        domain_area: newDomain.trim() || undefined
      });
      setNotebooks([res.data, ...notebooks]);
      setCreateModalOpen(false);
      setNewTitle('');
      setNewDescription('');
      // Open immediately in 3-panel workspace
      handleOpenNotebook(res.data.id);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to create notebook');
    } finally {
      setLoading(false);
    }
  };

  const handleOpenNotebook = async (notebookId: string) => {
    setLoading(true);
    setError(null);
    try {
      const res = await api.get(`/notebooks/${notebookId}`);
      setSelectedNotebook(res.data);
      // Reset chat stream
      setChatMessages([
        {
          role: 'assistant',
          content: `Opened notebook: **${res.data.title}**. You have ${res.data.sources?.length || 0} source documents active. Ask any question to explore your sources with verified inline citations.`,
          is_source_grounded: true,
          citations: []
        }
      ]);
      setStudioOutput(null);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load notebook');
    } finally {
      setLoading(false);
    }
  };

  // --- Source Operations ---
  const handleUploadSourceFile = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files || !e.target.files[0] || !selectedNotebook) return;
    const file = e.target.files[0];
    const formData = new FormData();
    formData.append('file', file);

    setLoading(true);
    try {
      await api.post(`/notebooks/${selectedNotebook.id}/sources/upload`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      // Refresh notebook details
      handleOpenNotebook(selectedNotebook.id);
      setAddSourceModalOpen(false);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Source upload failed');
    } finally {
      setLoading(false);
    }
  };

  const handlePasteSource = async () => {
    if (!pastedContent.trim() || !selectedNotebook) return;
    setLoading(true);
    try {
      await api.post(`/notebooks/${selectedNotebook.id}/sources/paste-text`, {
        title: pastedTitle.trim() || 'Pasted Research Excerpt',
        content_text: pastedContent
      });
      handleOpenNotebook(selectedNotebook.id);
      setAddSourceModalOpen(false);
      setPastedTitle('');
      setPastedContent('');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to save pasted source');
    } finally {
      setLoading(false);
    }
  };

  const handleRemoveSource = async (sourceId: string) => {
    if (!selectedNotebook) return;
    try {
      await api.delete(`/notebooks/${selectedNotebook.id}/sources/${sourceId}`);
      setSelectedNotebook({
        ...selectedNotebook,
        sources: selectedNotebook.sources.filter((s: any) => s.id !== sourceId)
      });
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to remove source');
    }
  };

  // --- Chat Submission ---
  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!chatInput.trim() || !selectedNotebook) return;

    const query = chatInput.trim();
    setChatInput('');

    // Append user message
    const updated = [...chatMessages, { role: 'user', content: query }];
    setChatMessages(updated);
    setChatLoading(true);

    try {
      const res = await api.post(`/notebooks/${selectedNotebook.id}/chat`, {
        query,
        general_ai_mode: generalAiMode
      });

      setChatMessages([
        ...updated,
        {
          role: 'assistant',
          content: res.data.answer,
          is_source_grounded: res.data.is_source_grounded,
          citations: res.data.citations || []
        }
      ]);
    } catch (err: any) {
      setChatMessages([
        ...updated,
        {
          role: 'assistant',
          content: 'An error occurred while synthesizing your query. Please try again.',
          is_source_grounded: false,
          citations: []
        }
      ]);
    } finally {
      setChatLoading(false);
    }
  };

  // --- Run Studio Tool (20 Generators) ---
  const handleRunStudioTool = async (toolName: string) => {
    if (!selectedNotebook) return;
    setActiveStudioTool(toolName);
    setStudioLoading(true);
    setError(null);

    try {
      const res = await api.post(`/notebooks/${selectedNotebook.id}/studio/${toolName}`);
      setStudioOutput(res.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || `Failed to run studio tool: ${toolName}`);
    } finally {
      setStudioLoading(false);
    }
  };

  // --- Run Humanize Tool ---
  const handleRunHumanize = async () => {
    if (!humanizeInput.trim() || !selectedNotebook) return;
    setHumanizeLoading(true);
    try {
      const res = await api.post(`/notebooks/${selectedNotebook.id}/humanize`, {
        text: humanizeInput,
        mode: humanizeMode
      });
      setHumanizeOutput(res.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Humanize transformation failed');
    } finally {
      setHumanizeLoading(false);
    }
  };

  // --- Save Output to Persistent Notes ---
  const handleSaveToNotes = async (title: string, content: string) => {
    if (!selectedNotebook) return;
    try {
      await api.post(`/notebooks/${selectedNotebook.id}/notes`, {
        title,
        content,
        category: 'Studio Insight'
      });
      alert('Saved directly to your persistent research notes in PostgreSQL!');
      // Refresh notebook
      handleOpenNotebook(selectedNotebook.id);
    } catch (err: any) {
      alert('Failed to save note: ' + err.message);
    }
  };

  // --- Export Notebook ---
  const handleExportNotebook = async (format: 'markdown' | 'csv' | 'text') => {
    if (!selectedNotebook) return;
    window.open(`${api.defaults.baseURL}/notebooks/${selectedNotebook.id}/export?export_format=${format}`, '_blank');
  };

  // =========================================================================
  // VIEW 1: NOTEBOOKS DIRECTORY (Grid / Search / + Create New Notebook)
  // =========================================================================
  if (!selectedNotebook) {
    const filteredNotebooks = notebooks.filter(nb =>
      nb.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      (nb.domain_area && nb.domain_area.toLowerCase().includes(searchQuery.toLowerCase()))
    );

    return (
      <div className="max-w-7xl mx-auto space-y-8 animate-in fade-in duration-300">
        
        {/* Banner Header */}
        <div className="flex flex-col sm:flex-row justify-between sm:items-center gap-4 border-b border-white/10 pb-6">
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary-500/10 border border-primary-500/20 text-primary-400 text-xs font-semibold uppercase tracking-wider mb-2">
              <Sparkles className="w-3.5 h-3.5" /> Google NotebookLM-Inspired Architecture
            </div>
            <h1 className="text-3xl font-extrabold text-white">AI Research Notebooks</h1>
            <p className="text-gray-400 text-sm mt-1">
              Create an AI research notebook using only a title, ingest multi-format source papers, and explore with source-grounded citations.
            </p>
          </div>

          <button
            onClick={() => setCreateModalOpen(true)}
            className="px-6 py-3 rounded-2xl bg-gradient-to-r from-primary-600 to-indigo-600 hover:from-primary-500 hover:to-indigo-500 text-white font-bold text-sm shadow-xl shadow-primary-500/25 flex items-center gap-2 transition"
          >
            <Plus className="w-5 h-5" /> + Create New Research Notebook
          </button>
        </div>

        {/* Search & Stats Bar */}
        {error && (
          <div className="p-3.5 rounded-2xl bg-red-500/10 border border-red-500/20 text-red-300 text-xs">
            {error}
          </div>
        )}
        <div className="flex flex-col sm:flex-row justify-between items-center gap-4">
          <div className="relative w-full sm:w-96">
            <Search className="absolute left-3.5 top-3 w-4 h-4 text-gray-400" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search research notebooks by title or domain..."
              className="w-full bg-dark-card/60 border border-white/10 rounded-xl pl-10 pr-4 py-2.5 text-sm text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-primary-500"
            />
          </div>

          <div className="text-xs text-gray-400 flex items-center gap-4">
            <span>Total Notebooks: <strong className="text-white">{notebooks.length}</strong></span>
            <span>All Data Persisted in: <strong className="text-emerald-400">PostgreSQL</strong></span>
          </div>
        </div>

        {/* Notebooks Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          
          {/* Quick Create Card */}
          <div
            onClick={() => setCreateModalOpen(true)}
            className="border-2 border-dashed border-white/15 hover:border-primary-500/60 rounded-3xl p-8 flex flex-col items-center justify-center text-center cursor-pointer bg-dark-card/30 hover:bg-primary-500/5 transition duration-300 group min-h-[220px]"
          >
            <div className="p-4 rounded-2xl bg-primary-500/10 text-primary-400 group-hover:scale-110 transition duration-300 mb-3">
              <Plus className="w-8 h-8" />
            </div>
            <h3 className="text-base font-bold text-white group-hover:text-primary-300 transition">
              Create New Notebook
            </h3>
            <p className="text-xs text-gray-500 mt-1 max-w-[200px]">
              Just enter your paper title — sources and AI questions can be added anytime.
            </p>
          </div>

          {/* Existing Notebook Cards */}
          {filteredNotebooks.map((nb) => (
            <div
              key={nb.id}
              onClick={() => handleOpenNotebook(nb.id)}
              className="glass-panel p-6 rounded-3xl border border-white/10 hover:border-primary-500/40 cursor-pointer transition duration-300 flex flex-col justify-between hover:shadow-2xl hover:shadow-primary-500/10 group"
            >
              <div>
                <div className="flex justify-between items-start mb-3">
                  <span className="text-[11px] font-semibold px-2.5 py-0.5 rounded-full bg-primary-500/10 text-primary-400 border border-primary-500/20">
                    {nb.domain_area || 'General Research'}
                  </span>
                  {nb.is_pinned && <Pin className="w-4 h-4 text-amber-400 fill-amber-400" />}
                </div>

                <h3 className="text-lg font-bold text-white group-hover:text-primary-300 transition line-clamp-2 mb-2">
                  {nb.title}
                </h3>

                <p className="text-xs text-gray-400 line-clamp-2 leading-relaxed">
                  {nb.description || 'Dedicated AI research workspace with grounded sources and citations.'}
                </p>
              </div>

              <div className="pt-6 border-t border-white/10 flex justify-between items-center text-xs text-gray-400">
                <span className="flex items-center gap-1.5 font-medium text-gray-300">
                  <FileText className="w-3.5 h-3.5 text-primary-400" />
                  {nb.source_count || 0} sources
                </span>
                <span className="text-gray-500">
                  {new Date(nb.updated_at).toLocaleDateString()}
                </span>
              </div>
            </div>
          ))}

        </div>

        {/* Modal: Create Notebook (Title ONLY required!) */}
        {createModalOpen && (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md animate-in fade-in">
            <div className="w-full max-w-md bg-dark-card border border-white/10 rounded-3xl p-6 glass-panel shadow-2xl space-y-4">
              <div className="flex justify-between items-center pb-2 border-b border-white/10">
                <h3 className="text-lg font-bold text-white flex items-center gap-2">
                  <BookOpen className="w-5 h-5 text-primary-400" /> New Research Notebook
                </h3>
                <button onClick={() => setCreateModalOpen(false)} className="text-gray-400 hover:text-white">✕</button>
              </div>

              <form onSubmit={handleCreateNotebook} className="space-y-4">
                <div>
                  <label className="block text-xs font-semibold text-gray-300 uppercase tracking-wider mb-1.5">
                    Research Paper / Project Title *
                  </label>
                  <input
                    type="text"
                    required
                    value={newTitle}
                    onChange={(e) => setNewTitle(e.target.value)}
                    placeholder="e.g. Artificial Intelligence in Healthcare"
                    autoFocus
                    className="w-full bg-dark-bg/60 border border-white/10 rounded-xl px-4 py-2.5 text-sm text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-primary-500"
                  />
                  <p className="text-[11px] text-gray-400 mt-1">
                    Entering a title is sufficient to create your notebook. AI will assist with sources and methodology inside.
                  </p>
                </div>

                <div>
                  <label className="block text-xs font-semibold text-gray-300 uppercase tracking-wider mb-1.5">
                    Domain / Field (Optional)
                  </label>
                  <input
                    type="text"
                    value={newDomain}
                    onChange={(e) => setNewDomain(e.target.value)}
                    placeholder="e.g. Biomedical AI, Distributed Systems"
                    className="w-full bg-dark-bg/60 border border-white/10 rounded-xl px-4 py-2 text-sm text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
                  />
                </div>

                <div>
                  <label className="block text-xs font-semibold text-gray-300 uppercase tracking-wider mb-1.5">
                    Description (Optional)
                  </label>
                  <textarea
                    rows={2}
                    value={newDescription}
                    onChange={(e) => setNewDescription(e.target.value)}
                    placeholder="Brief description of research scope or hypotheses..."
                    className="w-full bg-dark-bg/60 border border-white/10 rounded-xl p-3 text-sm text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
                  />
                </div>

                <div className="flex justify-end gap-2 pt-2">
                  <button
                    type="button"
                    onClick={() => setCreateModalOpen(false)}
                    className="px-4 py-2 rounded-xl text-xs text-gray-400 hover:bg-white/5"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    disabled={loading || !newTitle.trim()}
                    className="px-6 py-2.5 rounded-xl bg-primary-600 hover:bg-primary-500 text-white font-bold text-xs shadow-lg shadow-primary-500/25 flex items-center gap-1.5 transition disabled:opacity-50"
                  >
                    Create Notebook &rarr;
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}

      </div>
    );
  }

  // =========================================================================
  // VIEW 2: 3-PANEL NOTEBOOKLM WORKSPACE (Left: Sources, Center: Chat, Right: Studio)
  // =========================================================================
  return (
    <div className="h-[calc(100vh-6.5rem)] flex flex-col space-y-3 animate-in fade-in duration-300">
      
      {/* Notebook Top Navigation Bar */}
      <div className="glass-panel px-4 py-2.5 rounded-2xl border border-white/10 flex justify-between items-center shrink-0">
        <div className="flex items-center gap-3">
          <button
            onClick={() => setSelectedNotebook(null)}
            className="p-1.5 rounded-lg border border-white/10 text-gray-400 hover:text-white hover:bg-white/5 transition"
            title="Back to all notebooks"
          >
            <ChevronLeft className="w-5 h-5" />
          </button>
          <div>
            <h2 className="text-base font-bold text-white flex items-center gap-2">
              <BookOpen className="w-4 h-4 text-primary-400" />
              {selectedNotebook.title}
            </h2>
            <div className="text-[11px] text-gray-400 flex items-center gap-2">
              <span>{selectedNotebook.domain_area || 'General Research'}</span>
              <span>&bull;</span>
              <span className="text-primary-300 font-medium">{selectedNotebook.sources?.length || 0} reference sources</span>
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="flex items-center gap-2">
          {/* General AI Mode Toggle */}
          <div className="flex items-center gap-2 px-3 py-1 rounded-xl bg-dark-bg/60 border border-white/10 text-xs">
            <span className={generalAiMode ? 'text-amber-400 font-semibold' : 'text-primary-400 font-semibold'}>
              {generalAiMode ? 'General AI Mode' : 'Source-Grounded Mode'}
            </span>
            <button
              onClick={() => setGeneralAiMode(!generalAiMode)}
              className={`w-9 h-5 rounded-full p-0.5 transition ${generalAiMode ? 'bg-amber-500' : 'bg-primary-600'}`}
              title="Toggle between strictly source-grounded answers and broader AI knowledge"
            >
              <div className={`w-4 h-4 rounded-full bg-white transition-transform ${generalAiMode ? 'translate-x-4' : 'translate-x-0'}`} />
            </button>
          </div>

          {/* Export Dropdown */}
          <div className="relative group">
            <button className="px-3 py-1.5 rounded-xl border border-white/10 bg-dark-bg/60 text-gray-300 hover:text-white text-xs font-semibold flex items-center gap-1.5 transition">
              <Download className="w-3.5 h-3.5" /> Export
            </button>
            <div className="absolute right-0 mt-1 w-36 rounded-xl bg-dark-card border border-white/10 shadow-xl hidden group-hover:block z-50 p-1">
              <button
                onClick={() => handleExportNotebook('markdown')}
                className="w-full text-left px-3 py-1.5 rounded-lg text-xs text-gray-300 hover:bg-white/10 hover:text-white"
              >
                Markdown (.md)
              </button>
              <button
                onClick={() => handleExportNotebook('csv')}
                className="w-full text-left px-3 py-1.5 rounded-lg text-xs text-gray-300 hover:bg-white/10 hover:text-white"
              >
                CSV Table (.csv)
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* 3-Panel Main Area */}
      <div className="flex-1 flex gap-3 overflow-hidden">
        
        {/* ================================================================ */}
        {/* LEFT PANEL: SOURCES (Uploaded References & Upload Trigger) */}
        {/* ================================================================ */}
        <div className={`${leftPanelOpen ? 'w-80 shrink-0' : 'w-10 shrink-0'} transition-all duration-300 glass-panel rounded-2xl border border-white/10 flex flex-col overflow-hidden`}>
          <div className="p-3 border-b border-white/10 flex justify-between items-center">
            {leftPanelOpen && (
              <h3 className="text-xs font-bold text-white uppercase tracking-wider flex items-center gap-1.5">
                <FileText className="w-3.5 h-3.5 text-primary-400" /> Sources ({selectedNotebook.sources?.length || 0})
              </h3>
            )}
            <button
              onClick={() => setLeftPanelOpen(!leftPanelOpen)}
              className="p-1 rounded text-gray-400 hover:text-white hover:bg-white/5"
            >
              {leftPanelOpen ? <ChevronLeft className="w-4 h-4" /> : <ChevronRight className="w-4 h-4" />}
            </button>
          </div>

          {leftPanelOpen && (
            <div className="flex-1 flex flex-col p-3 overflow-hidden space-y-3">
              {/* Add Source Button */}
              <button
                onClick={() => setAddSourceModalOpen(true)}
                className="w-full py-2.5 px-3 rounded-xl bg-primary-500/15 border border-primary-500/30 hover:bg-primary-500/25 text-primary-300 text-xs font-bold flex items-center justify-center gap-2 transition"
              >
                <Plus className="w-4 h-4" /> Add Source Documents
              </button>

              {/* Source List */}
              <div className="flex-1 overflow-y-auto space-y-2 pr-1">
                {(!selectedNotebook.sources || selectedNotebook.sources.length === 0) ? (
                  <div className="p-6 text-center text-xs text-gray-500 border border-dashed border-white/10 rounded-2xl space-y-2 mt-4">
                    <Upload className="w-6 h-6 mx-auto text-gray-600" />
                    <p>No reference sources added yet.</p>
                    <p className="text-[11px] text-gray-600">Upload a PDF or paste notes to anchor the AI assistant.</p>
                  </div>
                ) : (
                  selectedNotebook.sources.map((src: any) => (
                    <div
                      key={src.id}
                      className="p-3 rounded-xl bg-dark-bg/60 border border-white/10 hover:border-primary-500/30 transition text-xs space-y-1.5 group"
                    >
                      <div className="flex justify-between items-start gap-1">
                        <span className="font-semibold text-white line-clamp-1">{src.title}</span>
                        <button
                          onClick={() => handleRemoveSource(src.id)}
                          className="text-gray-500 hover:text-red-400 opacity-0 group-hover:opacity-100 transition"
                          title="Remove source"
                        >
                          <Trash2 className="w-3.5 h-3.5" />
                        </button>
                      </div>

                      <div className="flex justify-between items-center text-[11px] text-gray-400">
                        <span className="uppercase text-primary-400 font-medium">{src.source_type}</span>
                        <span>{src.page_count || 1} pages</span>
                      </div>

                      {src.overview && (
                        <p className="text-[11px] text-gray-400 line-clamp-2 leading-relaxed">
                          {src.overview}
                        </p>
                      )}
                    </div>
                  ))
                )}
              </div>
            </div>
          )}
        </div>

        {/* ================================================================ */}
        {/* CENTER PANEL: AI RESEARCH ASSISTANT (CHAT + CITATIONS) */}
        {/* ================================================================ */}
        <div className="flex-1 glass-panel rounded-2xl border border-white/10 flex flex-col overflow-hidden">
          
          {/* Messages Stream */}
          <div className="flex-1 overflow-y-auto p-4 space-y-4">
            {chatMessages.map((msg, idx) => (
              <div
                key={idx}
                className={`flex gap-3 text-sm ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                {msg.role === 'assistant' && (
                  <div className="w-8 h-8 rounded-xl bg-primary-500/15 border border-primary-500/30 text-primary-400 flex items-center justify-center shrink-0">
                    <Sparkles className="w-4 h-4" />
                  </div>
                )}

                <div className={`max-w-[85%] rounded-2xl p-4 leading-relaxed ${
                  msg.role === 'user'
                    ? 'bg-primary-600 text-white shadow-lg shadow-primary-500/20'
                    : 'bg-dark-bg/70 border border-white/10 text-gray-200'
                }`}>
                  <div className="prose prose-invert prose-xs max-w-none whitespace-pre-line">
                    {msg.content}
                  </div>

                  {/* Inline Grounded Citations Cards */}
                  {msg.citations && msg.citations.length > 0 && (
                    <div className="mt-3 pt-3 border-t border-white/10 space-y-2">
                      <div className="text-[11px] font-bold text-primary-400 uppercase tracking-wider flex items-center gap-1.5">
                        <Bookmark className="w-3 h-3" /> Grounded Source Citations:
                      </div>
                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                        {msg.citations.map((c: any, cIdx: number) => (
                          <div key={cIdx} className="p-2.5 rounded-xl bg-black/40 border border-primary-500/20 text-xs">
                            <div className="flex items-center justify-between text-primary-300 font-semibold mb-1">
                              <span>{c.citation_key} {c.source_title}</span>
                              <span className="text-[10px] px-1.5 py-0.5 rounded bg-primary-500/20">p. {c.page_number}</span>
                            </div>
                            <p className="text-[11px] text-gray-400 italic line-clamp-2">
                              "{c.passage}"
                            </p>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            ))}

            {chatLoading && (
              <div className="flex gap-3 text-sm">
                <div className="w-8 h-8 rounded-xl bg-primary-500/15 border border-primary-500/30 text-primary-400 flex items-center justify-center shrink-0 animate-pulse">
                  <Sparkles className="w-4 h-4" />
                </div>
                <div className="p-4 rounded-2xl bg-dark-bg/70 border border-white/10 text-xs text-gray-400 flex items-center gap-2">
                  <div className="w-3 h-3 border-2 border-primary-400 border-t-transparent rounded-full animate-spin" />
                  Synthesizing answer grounded in uploaded reference materials...
                </div>
              </div>
            )}
          </div>

          {/* Chat Input Bar */}
          <form onSubmit={handleSendMessage} className="p-3 border-t border-white/10 bg-dark-bg/40 flex items-center gap-2">
            <input
              type="text"
              value={chatInput}
              onChange={(e) => setChatInput(e.target.value)}
              placeholder={generalAiMode ? "Ask anything using general AI knowledge..." : "Ask questions grounded strictly in your reference sources..."}
              className="flex-1 bg-dark-bg/80 border border-white/10 rounded-xl px-4 py-2.5 text-sm text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-primary-500"
            />
            <button
              type="submit"
              disabled={chatLoading || !chatInput.trim()}
              className="p-2.5 rounded-xl bg-primary-600 hover:bg-primary-500 text-white font-semibold shadow-lg shadow-primary-500/20 transition disabled:opacity-50"
            >
              <Send className="w-4 h-4" />
            </button>
          </form>

        </div>

        {/* ================================================================ */}
        {/* RIGHT PANEL: STUDIO & HUMANIZED WRITING WORKSPACE */}
        {/* ================================================================ */}
        <div className={`${rightPanelOpen ? 'w-96 shrink-0' : 'w-10 shrink-0'} transition-all duration-300 glass-panel rounded-2xl border border-white/10 flex flex-col overflow-hidden`}>
          <div className="p-3 border-b border-white/10 flex justify-between items-center">
            {rightPanelOpen && (
              <div className="flex gap-1 text-xs">
                <button
                  onClick={() => setRightPanelTab('studio')}
                  className={`px-3 py-1 rounded-lg font-semibold transition ${
                    rightPanelTab === 'studio' ? 'bg-primary-500/20 text-primary-300' : 'text-gray-400 hover:text-white'
                  }`}
                >
                  Studio (20 Tools)
                </button>
                <button
                  onClick={() => setRightPanelTab('humanize')}
                  className={`px-3 py-1 rounded-lg font-semibold transition ${
                    rightPanelTab === 'humanize' ? 'bg-primary-500/20 text-primary-300' : 'text-gray-400 hover:text-white'
                  }`}
                >
                  Humanize Writing
                </button>
              </div>
            )}
            <button
              onClick={() => setRightPanelOpen(!rightPanelOpen)}
              className="p-1 rounded text-gray-400 hover:text-white hover:bg-white/5"
            >
              {rightPanelOpen ? <ChevronRight className="w-4 h-4" /> : <ChevronLeft className="w-4 h-4" />}
            </button>
          </div>

          {rightPanelOpen && (
            <div className="flex-1 flex flex-col p-3 overflow-y-auto space-y-4">
              
              {/* TAB 1: STUDIO (20 Generators) */}
              {rightPanelTab === 'studio' && (
                <div className="space-y-4">
                  <div>
                    <h4 className="text-xs font-semibold text-gray-300 uppercase tracking-wider mb-2">Select Generator:</h4>
                    <div className="grid grid-cols-2 gap-1.5">
                      {[
                        { id: 'summary', label: 'Complete Summary' },
                        { id: 'short_summary', label: 'Short TL;DR' },
                        { id: 'detailed_notes', label: 'Study Notes' },
                        { id: 'important_definitions', label: 'Definitions' },
                        { id: 'key_concepts', label: 'Key Concepts' },
                        { id: 'literature_comparison', label: 'Comparison' },
                        { id: 'gap_analysis', label: 'Gap Analysis' },
                        { id: 'research_questions', label: 'Questions' },
                        { id: 'research_objectives', label: 'Objectives' },
                        { id: 'methodology', label: 'Methodology' },
                        { id: 'abstract_draft', label: 'Abstract Draft' },
                        { id: 'intro_draft', label: 'Introduction' },
                        { id: 'study_guide', label: 'Study Guide' },
                        { id: 'viva_questions', label: 'Viva Q&A' },
                        { id: 'mcqs', label: 'Assessment MCQs' },
                        { id: 'flashcards', label: 'Flashcards' },
                        { id: 'mind_map', label: 'Mind Map' },
                        { id: 'report_outline', label: 'Report Outline' },
                        { id: 'presentation_outline', label: 'Slide Deck' },
                        { id: 'audio_overview', label: 'Audio Podcast Script' }
                      ].map((t) => (
                        <button
                          key={t.id}
                          onClick={() => handleRunStudioTool(t.id)}
                          className={`p-2 rounded-xl text-xs text-left border transition ${
                            activeStudioTool === t.id
                              ? 'bg-primary-500/20 border-primary-500 text-primary-300 font-semibold'
                              : 'bg-dark-bg/50 border-white/10 text-gray-400 hover:border-white/20'
                          }`}
                        >
                          {t.label}
                        </button>
                      ))}
                    </div>
                  </div>

                  {/* Studio Tool Output Display */}
                  {studioLoading ? (
                    <div className="p-6 rounded-2xl bg-dark-bg/60 border border-white/10 text-center text-xs text-gray-400 space-y-2">
                      <div className="w-5 h-5 border-2 border-primary-400 border-t-transparent rounded-full animate-spin mx-auto" />
                      <p>Generating insights across reference sources...</p>
                    </div>
                  ) : studioOutput && (
                    <div className="p-4 rounded-2xl bg-dark-bg/60 border border-white/10 space-y-3">
                      <div className="flex justify-between items-center border-b border-white/10 pb-2">
                        <h5 className="font-bold text-white text-xs">{studioOutput.title}</h5>
                        <button
                          onClick={() => handleSaveToNotes(studioOutput.title, JSON.stringify(studioOutput.data, null, 2))}
                          className="px-2.5 py-1 rounded-lg bg-emerald-500/20 border border-emerald-500/40 text-emerald-300 hover:bg-emerald-500/30 text-[11px] font-semibold flex items-center gap-1 transition"
                        >
                          <Bookmark className="w-3 h-3" /> Save to Notes
                        </button>
                      </div>

                      <pre className="text-[11px] text-gray-300 font-mono whitespace-pre-wrap max-h-60 overflow-y-auto leading-relaxed bg-black/40 p-2.5 rounded-xl">
                        {typeof studioOutput.data === 'string'
                          ? studioOutput.data
                          : JSON.stringify(studioOutput.data, null, 2)}
                      </pre>
                    </div>
                  )}
                </div>
              )}

              {/* TAB 2: HUMANIZE & IMPROVE WRITING */}
              {rightPanelTab === 'humanize' && (
                <div className="space-y-4">
                  <div>
                    <label className="block text-xs font-semibold text-gray-300 uppercase tracking-wider mb-1.5">
                      Writing Transformation Mode:
                    </label>
                    <select
                      value={humanizeMode}
                      onChange={(e) => setHumanizeMode(e.target.value)}
                      className="w-full bg-dark-bg/60 border border-white/10 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
                    >
                      <option value="natural_human">Natural Human (Flow & conversational clarity)</option>
                      <option value="academic_formal">Academic Formal (Scholarly publication register)</option>
                      <option value="simple_english">Simple English (Demystify complex jargon)</option>
                      <option value="concise">Concise (Cut redundancy, keep all data)</option>
                      <option value="expand">Expand (Deepen analytical rationale)</option>
                      <option value="bullet_to_para">Convert Bullets to Paragraphs</option>
                      <option value="para_to_notes">Convert Paragraphs to Structured Notes</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-xs font-semibold text-gray-300 uppercase tracking-wider mb-1.5">
                      Original Text:
                    </label>
                    <textarea
                      rows={4}
                      value={humanizeInput}
                      onChange={(e) => setHumanizeInput(e.target.value)}
                      placeholder="Paste your draft or notes to polish..."
                      className="w-full bg-dark-bg/60 border border-white/10 rounded-xl p-3 text-xs text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-primary-500"
                    />
                  </div>

                  <button
                    onClick={handleRunHumanize}
                    disabled={humanizeLoading || !humanizeInput.trim()}
                    className="w-full py-2.5 rounded-xl bg-gradient-to-r from-primary-600 to-indigo-600 hover:from-primary-500 hover:to-indigo-500 text-white font-bold text-xs shadow-lg shadow-primary-500/25 flex items-center justify-center gap-1.5 transition disabled:opacity-50"
                  >
                    <Sparkles className="w-4 h-4" /> Transform & Polish Writing
                  </button>

                  {/* Side-by-Side Revised Output */}
                  {humanizeOutput && (
                    <div className="p-3.5 rounded-2xl bg-dark-bg/60 border border-white/10 space-y-3">
                      <div className="flex justify-between items-center border-b border-white/10 pb-2">
                        <span className="text-xs font-bold text-emerald-400">Revised Output:</span>
                        <button
                          onClick={() => handleSaveToNotes(`Polished Text (${humanizeMode})`, humanizeOutput.revised_text)}
                          className="px-2.5 py-1 rounded-lg bg-emerald-500/20 text-emerald-300 text-[11px] font-semibold"
                        >
                          Save as Note
                        </button>
                      </div>

                      <p className="text-xs text-gray-200 leading-relaxed bg-black/40 p-3 rounded-xl">
                        {humanizeOutput.revised_text}
                      </p>

                      {humanizeOutput.changes_summary?.length > 0 && (
                        <div className="text-[11px] text-gray-400 space-y-1">
                          <strong className="text-gray-300">Changes Applied:</strong>
                          {humanizeOutput.changes_summary.map((c: string, idx: number) => (
                            <div key={idx}>&bull; {c}</div>
                          ))}
                        </div>
                      )}
                    </div>
                  )}
                </div>
              )}

            </div>
          )}
        </div>

      </div>

      {/* Modal: Add Source (File upload, Paste text, URL) */}
      {addSourceModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md animate-in fade-in">
          <div className="w-full max-w-lg bg-dark-card border border-white/10 rounded-3xl p-6 glass-panel shadow-2xl space-y-4">
            <div className="flex justify-between items-center pb-2 border-b border-white/10">
              <h3 className="text-base font-bold text-white flex items-center gap-2">
                <Upload className="w-5 h-5 text-primary-400" /> Add Research Source
              </h3>
              <button onClick={() => setAddSourceModalOpen(false)} className="text-gray-400 hover:text-white">✕</button>
            </div>

            {/* Source Type Selector */}
            <div className="flex gap-2">
              {[
                { id: 'file', label: 'Upload File (PDF/DOCX/TXT)' },
                { id: 'paste', label: 'Paste Text' },
                { id: 'url', label: 'Website / YouTube URL' }
              ].map((st) => (
                <button
                  key={st.id}
                  onClick={() => setAddSourceType(st.id as any)}
                  className={`flex-1 py-2 rounded-xl text-xs font-semibold border transition ${
                    addSourceType === st.id
                      ? 'bg-primary-500/20 border-primary-500 text-primary-300'
                      : 'bg-dark-bg/60 border-white/10 text-gray-400 hover:border-white/20'
                  }`}
                >
                  {st.label}
                </button>
              ))}
            </div>

            {addSourceType === 'file' && (
              <div className="border-2 border-dashed border-white/15 rounded-2xl p-6 text-center space-y-3">
                <FileText className="w-8 h-8 mx-auto text-primary-400" />
                <p className="text-xs text-gray-400">Select PDF, DOCX, DOC or TXT</p>
                <input
                  type="file"
                  accept=".pdf,.docx,.doc,.txt"
                  onChange={handleUploadSourceFile}
                  className="w-full text-xs text-gray-400 file:mr-3 file:py-2 file:px-4 file:rounded-xl file:border-0 file:text-xs file:font-semibold file:bg-primary-500/20 file:text-primary-300 hover:file:bg-primary-500/30 cursor-pointer"
                />
              </div>
            )}

            {addSourceType === 'paste' && (
              <div className="space-y-3">
                <div>
                  <label className="block text-xs font-medium text-gray-300 mb-1">Source Title</label>
                  <input
                    type="text"
                    value={pastedTitle}
                    onChange={(e) => setPastedTitle(e.target.value)}
                    placeholder="e.g. Clinical Imaging Trial Notes"
                    className="w-full bg-dark-bg/60 border border-white/10 rounded-xl px-4 py-2 text-sm text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
                  />
                </div>
                <div>
                  <label className="block text-xs font-medium text-gray-300 mb-1">Text Content</label>
                  <textarea
                    rows={5}
                    value={pastedContent}
                    onChange={(e) => setPastedContent(e.target.value)}
                    placeholder="Paste article, abstract, findings, or notes here..."
                    className="w-full bg-dark-bg/60 border border-white/10 rounded-xl p-3 text-xs text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-primary-500"
                  />
                </div>
                <div className="flex justify-end">
                  <button
                    onClick={handlePasteSource}
                    disabled={!pastedContent.trim()}
                    className="px-5 py-2 rounded-xl bg-primary-600 hover:bg-primary-500 text-white font-bold text-xs"
                  >
                    Add Pasted Source
                  </button>
                </div>
              </div>
            )}

            {addSourceType === 'url' && (
              <div className="space-y-3">
                <div>
                  <label className="block text-xs font-medium text-gray-300 mb-1">Source Title</label>
                  <input
                    type="text"
                    value={pastedTitle}
                    onChange={(e) => setPastedTitle(e.target.value)}
                    placeholder="e.g. arXiv Publication"
                    className="w-full bg-dark-bg/60 border border-white/10 rounded-xl px-4 py-2 text-sm text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
                  />
                </div>
                <div>
                  <label className="block text-xs font-medium text-gray-300 mb-1">Resource URL</label>
                  <input
                    type="url"
                    value={urlInput}
                    onChange={(e) => setUrlInput(e.target.value)}
                    placeholder="https://arxiv.org/abs/2301.12345"
                    className="w-full bg-dark-bg/60 border border-white/10 rounded-xl px-4 py-2 text-sm text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
                  />
                </div>
                <div className="flex justify-end">
                  <button
                    onClick={async () => {
                      if (!urlInput.trim()) return;
                      await api.post(`/notebooks/${selectedNotebook.id}/sources/url`, {
                        title: pastedTitle || 'External Resource',
                        url: urlInput
                      });
                      handleOpenNotebook(selectedNotebook.id);
                      setAddSourceModalOpen(false);
                    }}
                    className="px-5 py-2 rounded-xl bg-primary-600 hover:bg-primary-500 text-white font-bold text-xs"
                  >
                    Link URL Source
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      )}

    </div>
  );
}
