import axios from 'axios';

// Backend .NET Web API URL
const API_BASE_URL = import.meta.env.VITE_API_URL || '/api';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface CreateProjectPayload {
  name: string;
  description: string;
}

export interface UpdateAudiencePayload {
  targetAudience: string;
}

export interface AddRequirementPayload {
  type: number; // 1: Functional, 2: NonFunctional
  title: string;
  description?: string;
  priority?: string;
}

export interface RequirementItem {
  id: number;
  type: number;
  title: string;
  description: string;
  priority: string;
}

export interface ArchitectureConfigItem {
  id: number;
  frontendStack: string;
  backendStack: string;
  databaseStack: string;
  mermaidDiagramCode: string;
}

export interface PromptArtifactItem {
  id: number;
  requirementsMarkdown: string;
  architectureMarkdown: string;
  masterPrompt: string;
  generatedAt: string;
}

export interface ProjectDetail {
  id: number;
  name: string;
  description: string;
  targetAudience: string;
  status: string;
  createdAt: string;
  updatedAt?: string;
  requirements: RequirementItem[];
  architecture?: ArchitectureConfigItem;
  prompts: PromptArtifactItem[];
}

// Wrapper Helper để lấy data từ AutoWrapper
const unwrap = <T>(res: any): T => {
  if (res.data && res.data.result !== undefined) {
    return res.data.result as T;
  }
  return res.data as T;
};

export const api = {
  // 1. Tạo dự án
  createProject: async (data: CreateProjectPayload): Promise<ProjectDetail> => {
    try {
      const res = await apiClient.post<any>('/project', data);
      return unwrap<ProjectDetail>(res);
    } catch (error) {
      console.warn('Backend API connection fallback (Local Mode):', error);
      // Fallback local mock để đảm bảo UI không crash nếu Backend chưa bật
      return {
        id: Date.now(),
        name: data.name,
        description: data.description,
        targetAudience: '',
        status: 'Draft',
        createdAt: new Date().toISOString(),
        requirements: [],
        prompts: []
      };
    }
  },

  // 2. Cập nhật đối tượng người dùng
  updateAudience: async (projectId: number, data: UpdateAudiencePayload): Promise<boolean> => {
    try {
      await apiClient.put(`/project/${projectId}/audience`, data);
      return true;
    } catch (error) {
      console.warn('Backend API connection fallback:', error);
      return true;
    }
  },

  // 3. Thêm tính năng / yêu cầu
  addRequirement: async (projectId: number, data: AddRequirementPayload): Promise<RequirementItem> => {
    try {
      const res = await apiClient.post<any>(`/project/${projectId}/requirements`, data);
      return unwrap<RequirementItem>(res);
    } catch (error) {
      console.warn('Backend API connection fallback:', error);
      return {
        id: Math.floor(Math.random() * 10000),
        type: data.type,
        title: data.title,
        description: data.description || '',
        priority: data.priority || 'Medium'
      };
    }
  },

  // 4. Lấy chi tiết dự án
  getProject: async (projectId: number): Promise<ProjectDetail | null> => {
    try {
      const res = await apiClient.get<any>(`/project/${projectId}`);
      return unwrap<ProjectDetail>(res);
    } catch (error) {
      console.warn('Backend API connection fallback:', error);
      return null;
    }
  }
};
