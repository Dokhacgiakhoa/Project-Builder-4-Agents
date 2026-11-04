using System.Collections.Generic;
using System.Threading.Tasks;
using Before_Vibe_Coding.Dtos.Projects;
using Before_Vibe_Coding.Dtos.Requirements;

namespace Before_Vibe_Coding.Services
{
    public interface IProjectService
    {
        Task<List<ProjectDetailDto>> GetAllProjectsAsync();
        Task<ProjectDetailDto?> GetProjectByIdAsync(int id);
        Task<ProjectDetailDto> CreateProjectAsync(CreateProjectDto dto);
        Task<bool> UpdateAudienceAsync(int id, UpdateAudienceDto dto);
        Task<RequirementDto> AddRequirementAsync(int projectId, AddRequirementDto dto);
        Task<bool> DeleteProjectAsync(int id);
    }
}
