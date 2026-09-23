import api from './api';

export interface ResearchProject {
  id: string;
  title: string;
  description?: string;
  research_question?: string;
  status: string;
  created_at: string;
  updated_at: string;
  papers: ResearchPaper[];
  literature_review?: LiteratureReview;
}

export interface ResearchPaper {
  id: string;
  project_id: string;
  title: string;
  authors?: string;
  publication_year?: string;
  abstract?: string;
  doi?: string;
  file_url?: string;
  created_at: string;
  notes: PaperNote[];
}

export interface PaperNote {
  id: string;
  paper_id: string;
  content: string;
  page_number?: string;
  created_at: string;
  updated_at: string;
}

export interface LiteratureReview {
  id: string;
  project_id: string;
  content: string;
  created_at: string;
  updated_at: string;
}

export const researchService = {
  // Projects
  getProjects: async () => {
    const response = await api.get('/research/projects');
    return response.data;
  },
  getProject: async (id: string) => {
    const response = await api.get(`/research/projects/${id}`);
    return response.data;
  },
  createProject: async (data: Partial<ResearchProject>) => {
    const response = await api.post('/research/projects', data);
    return response.data;
  },
  updateProject: async (id: string, data: Partial<ResearchProject>) => {
    const response = await api.put(`/research/projects/${id}`, data);
    return response.data;
  },
  deleteProject: async (id: string) => {
    await api.delete(`/research/projects/${id}`);
  },

  // Papers
  uploadPaper: async (projectId: string, formData: FormData) => {
    const response = await api.post(`/research/projects/${projectId}/papers`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },
  deletePaper: async (paperId: string) => {
    await api.delete(`/research/papers/${paperId}`);
  },

  // Notes
  addNote: async (paperId: string, content: string, pageNumber?: string) => {
    const response = await api.post(`/research/papers/${paperId}/notes`, {
      content,
      page_number: pageNumber,
    });
    return response.data;
  },
  deleteNote: async (noteId: string) => {
    await api.delete(`/research/notes/${noteId}`);
  },

  // Literature Review
  updateLiteratureReview: async (projectId: string, content: string) => {
    const response = await api.put(`/research/projects/${projectId}/literature-review`, {
      content,
    });
    return response.data;
  },
};
