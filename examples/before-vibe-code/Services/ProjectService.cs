using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Before_Vibe_Coding.Dtos.Projects;
using Before_Vibe_Coding.Dtos.Requirements;
using Before_Vibe_Coding.Models.Entities;
using Before_Vibe_Coding.Repositories;

namespace Before_Vibe_Coding.Services
{
    public class ProjectService : IProjectService
    {
        private readonly IProjectRepository _projectRepository;

        public ProjectService(IProjectRepository projectRepository)
        {
            _projectRepository = projectRepository;
        }

        public async Task<List<ProjectDetailDto>> GetAllProjectsAsync()
        {
            var projects = await _projectRepository.GetAllProjectsAsync();
            return projects.Select(MapToDetailDto).ToList();
        }

        public async Task<ProjectDetailDto?> GetProjectByIdAsync(int id)
        {
            var project = await _projectRepository.GetProjectByIdAsync(id);
            return project == null ? null : MapToDetailDto(project);
        }

        public async Task<ProjectDetailDto> CreateProjectAsync(CreateProjectDto dto)
        {
            try
            {
                var project = new Project
                {
                    Name = dto.Name,
                    Description = dto.Description,
                    Status = "Draft",
                    CreatedAt = DateTime.UtcNow
                };

                var createdProject = await _projectRepository.AddProjectAsync(project);
                return MapToDetailDto(createdProject);
            }
            catch (Exception)
            {
                throw;
            }
        }

        public async Task<bool> UpdateAudienceAsync(int id, UpdateAudienceDto dto)
        {
            var project = await _projectRepository.GetProjectByIdAsync(id);
            if (project == null) return false;

            project.TargetAudience = dto.TargetAudience;
            return await _projectRepository.UpdateProjectAsync(project);
        }

        public async Task<RequirementDto> AddRequirementAsync(int projectId, AddRequirementDto dto)
        {
            var project = await _projectRepository.GetProjectByIdAsync(projectId);
            if (project == null)
            {
                throw new KeyNotFoundException($"Dự án với ID {projectId} không tồn tại.");
            }

            var requirement = new Requirement
            {
                ProjectId = projectId,
                Type = dto.Type,
                Title = dto.Title,
                Description = dto.Description,
                Priority = dto.Priority,
                CreatedAt = DateTime.UtcNow
            };

            var createdReq = await _projectRepository.AddRequirementAsync(requirement);

            return new RequirementDto
            {
                Id = createdReq.Id,
                Type = createdReq.Type,
                Title = createdReq.Title,
                Description = createdReq.Description,
                Priority = createdReq.Priority
            };
        }

        public async Task<bool> DeleteProjectAsync(int id)
        {
            return await _projectRepository.DeleteProjectAsync(id);
        }

        private static ProjectDetailDto MapToDetailDto(Project project)
        {
            return new ProjectDetailDto
            {
                Id = project.Id,
                Name = project.Name,
                Description = project.Description,
                TargetAudience = project.TargetAudience,
                Status = project.Status,
                CreatedAt = project.CreatedAt,
                UpdatedAt = project.UpdatedAt,
                Requirements = project.Requirements?.Select(r => new RequirementDto
                {
                    Id = r.Id,
                    Type = r.Type,
                    Title = r.Title,
                    Description = r.Description,
                    Priority = r.Priority
                }).ToList() ?? new List<RequirementDto>(),
                Architecture = project.Architecture == null ? null : new ArchitectureConfigDto
                {
                    Id = project.Architecture.Id,
                    FrontendStack = project.Architecture.FrontendStack,
                    BackendStack = project.Architecture.BackendStack,
                    DatabaseStack = project.Architecture.DatabaseStack,
                    MermaidDiagramCode = project.Architecture.MermaidDiagramCode
                },
                Prompts = project.Prompts?.Select(pr => new PromptArtifactDto
                {
                    Id = pr.Id,
                    RequirementsMarkdown = pr.RequirementsMarkdown,
                    ArchitectureMarkdown = pr.ArchitectureMarkdown,
                    MasterPrompt = pr.MasterPrompt,
                    GeneratedAt = pr.GeneratedAt
                }).ToList() ?? new List<PromptArtifactDto>()
            };
        }
    }
}
