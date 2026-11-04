using System.Collections.Generic;
using System.Threading.Tasks;
using Before_Vibe_Coding.Models.Entities;

namespace Before_Vibe_Coding.Repositories
{
    public interface IProjectRepository
    {
        Task<List<Project>> GetAllProjectsAsync();
        Task<Project?> GetProjectByIdAsync(int id);
        Task<Project> AddProjectAsync(Project project);
        Task<bool> UpdateProjectAsync(Project project);
        Task<bool> DeleteProjectAsync(int id);
        Task<Requirement> AddRequirementAsync(Requirement requirement);
    }
}
