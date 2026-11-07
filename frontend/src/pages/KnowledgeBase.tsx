import { useState, useEffect } from 'react';
import { BookMarked, Search, Plus, X } from 'lucide-react';
import api from '../services/api';

export default function KnowledgeBase() {
  const [items, setItems] = useState<any[]>([]);
  const [search, setSearch] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [selectedItem, setSelectedItem] = useState<any>(null);
  const [showAddModal, setShowAddModal] = useState(false);

  const [newTitle, setNewTitle] = useState('');
  const [newCategory, setNewCategory] = useState('Research Papers');
  const [newContent, setNewContent] = useState('');

  useEffect(() => {
    loadItems();
  }, []);

  const loadItems = async () => {
    try {
      const res = await api.get('/integration/knowledge-base/items');
      setItems(res.data);
      if (res.data.length > 0) {
        setSelectedItem(res.data[0]);
      }
    } catch (err) {
      console.error('Error loading knowledge base:', err);
    }
  };

  const handleCreateItem = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTitle.trim()) return;

    try {
      const res = await api.post('/integration/knowledge-base/items', {
        title: newTitle,
        category: newCategory,
        content: newContent,
        tags: [newCategory.toLowerCase()]
      });
      setItems([res.data, ...items]);
      setSelectedItem(res.data);
      setShowAddModal(false);
      setNewTitle('');
      setNewContent('');
    } catch (err) {
      console.error('Error creating knowledge item:', err);
    }
  };

  const categories = ['All', 'Research Papers', 'Career Notes', 'Methodologies', 'General'];

  const filteredItems = items.filter(item => {
    if (selectedCategory !== 'All' && item.category !== selectedCategory) return false;
    if (search && !item.title.toLowerCase().includes(search.toLowerCase()) && !item.content.toLowerCase().includes(search.toLowerCase())) return false;
    return true;
  });

  return (
    <div className="w-full max-w-7xl mx-auto space-y-6 pb-20">
      
      {/* Header */}
      <div className="p-6 rounded-2xl bg-dark-card border border-white/10 glass-panel flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-400 text-xs font-semibold mb-2">
            <BookMarked className="w-3.5 h-3.5" />
            Personal Knowledge Base
          </div>
          <h1 className="text-2xl md:text-3xl font-extrabold text-white">Academic & Engineering Repository</h1>
          <p className="text-xs text-gray-400 mt-1">
            Persistently stores verified findings, architecture summaries, research papers, and technical cheat sheets.
          </p>
        </div>

        <button
          onClick={() => setShowAddModal(true)}
          className="px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold flex items-center gap-2 shadow-md shadow-emerald-600/30 transition self-start sm:self-auto"
        >
          <Plus className="w-4 h-4" />
          Add Knowledge Item
        </button>
      </div>

      {/* Search & Category Pills */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 text-xs">
        <div className="relative flex-1 max-w-md">
          <Search className="absolute left-3.5 top-3 w-4 h-4 text-gray-400" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search knowledge repository..."
            className="w-full bg-dark-card border border-white/10 rounded-xl pl-10 pr-4 py-2 text-xs text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-emerald-500"
          />
        </div>

        <div className="flex items-center gap-1.5 overflow-x-auto pb-1">
          {categories.map((cat) => (
            <button
              key={cat}
              onClick={() => setSelectedCategory(cat)}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold whitespace-nowrap transition ${
                selectedCategory === cat ? 'bg-emerald-600 text-white' : 'bg-dark-card text-gray-400 hover:text-white border border-white/5'
              }`}
            >
              {cat}
            </button>
          ))}
        </div>
      </div>

      {/* Main Split: Items List (4 Cols) + Detail Markdown View (8 Cols) */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        
        {/* Left Column: Items List */}
        <div className="lg:col-span-4 space-y-2.5 max-h-[75vh] overflow-y-auto pr-1">
          {filteredItems.map((item) => {
            const isSelected = selectedItem?.id === item.id;
            return (
              <div
                key={item.id}
                onClick={() => setSelectedItem(item)}
                className={`p-4 rounded-xl border transition cursor-pointer glass-panel ${
                  isSelected ? 'bg-emerald-600/20 border-emerald-500/50 text-white' : 'bg-dark-card border-white/10 hover:border-white/20'
                }`}
              >
                <div className="flex items-center justify-between gap-2 mb-1">
                  <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-white/5 text-emerald-300">
                    {item.category}
                  </span>
                  <span className="text-[10px] text-gray-500">
                    {new Date(item.created_at).toLocaleDateString()}
                  </span>
                </div>
                <h4 className="text-xs font-bold text-white truncate">{item.title}</h4>
                <p className="text-[11px] text-gray-400 line-clamp-2 mt-1">{item.content}</p>
              </div>
            );
          })}

          {filteredItems.length === 0 && (
            <div className="text-center py-12 rounded-xl bg-dark-card/40 border border-dashed border-white/10 text-gray-400 text-xs">
              No knowledge items match your search.
            </div>
          )}
        </div>

        {/* Right Column: Markdown Reader View */}
        <div className="lg:col-span-8 p-6 rounded-2xl bg-dark-card border border-white/10 glass-panel min-h-[500px] space-y-4">
          {selectedItem ? (
            <>
              <div className="pb-4 border-b border-white/10 space-y-2">
                <div className="flex items-center gap-2">
                  <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-emerald-500/20 text-emerald-300">
                    {selectedItem.category}
                  </span>
                  <span className="text-xs text-gray-400 uppercase font-semibold">
                    Source: {selectedItem.source_type}
                  </span>
                </div>
                <h2 className="text-xl font-bold text-white">{selectedItem.title}</h2>
              </div>

              <div className="prose prose-invert max-w-none text-xs sm:text-sm text-gray-300 whitespace-pre-wrap leading-relaxed font-sans">
                {selectedItem.content}
              </div>
            </>
          ) : (
            <div className="text-center py-24 text-gray-500 text-xs">
              Select an item from the repository or sync papers directly from your Research Lab.
            </div>
          )}
        </div>

      </div>

      {/* Add Item Modal */}
      {showAddModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm">
          <div className="relative w-full max-w-lg bg-dark-card border border-white/10 rounded-2xl p-6 shadow-2xl glass-panel space-y-4">
            <div className="flex items-center justify-between pb-3 border-b border-white/10">
              <h3 className="text-base font-bold text-white">Add Knowledge Base Item</h3>
              <button onClick={() => setShowAddModal(false)} className="text-gray-400 hover:text-white">
                <X className="w-5 h-5" />
              </button>
            </div>

            <form onSubmit={handleCreateItem} className="space-y-3 text-xs">
              <div>
                <label className="block font-semibold text-gray-300 mb-1">Title</label>
                <input
                  type="text"
                  required
                  value={newTitle}
                  onChange={(e) => setNewTitle(e.target.value)}
                  placeholder="e.g. Scalable Microservice Rate-Limiting Algorithms"
                  className="w-full bg-dark-bg border border-white/10 rounded-xl px-3 py-2 text-white"
                />
              </div>

              <div>
                <label className="block font-semibold text-gray-300 mb-1">Category</label>
                <select
                  value={newCategory}
                  onChange={(e) => setNewCategory(e.target.value)}
                  className="w-full bg-dark-bg border border-white/10 rounded-xl px-3 py-2 text-white"
                >
                  <option value="Research Papers">Research Papers</option>
                  <option value="Career Notes">Career Notes</option>
                  <option value="Methodologies">Methodologies</option>
                  <option value="General">General</option>
                </select>
              </div>

              <div>
                <label className="block font-semibold text-gray-300 mb-1">Content (Markdown supported)</label>
                <textarea
                  required
                  rows={6}
                  value={newContent}
                  onChange={(e) => setNewContent(e.target.value)}
                  placeholder="Write or paste your technical notes, algorithms, or paper synthesis..."
                  className="w-full bg-dark-bg border border-white/10 rounded-xl px-3 py-2 text-white font-mono"
                />
              </div>

              <button
                type="submit"
                className="w-full py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold transition shadow-lg shadow-emerald-600/30"
              >
                Save Knowledge Item in PostgreSQL
              </button>
            </form>
          </div>
        </div>
      )}

    </div>
  );
}
