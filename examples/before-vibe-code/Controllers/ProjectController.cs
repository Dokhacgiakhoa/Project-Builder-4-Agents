using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Before_Vibe_Coding.Dtos.Projects;
using Before_Vibe_Coding.Dtos.Requirements;
using Before_Vibe_Coding.Services;

namespace Before_Vibe_Coding.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class ProjectController : ControllerBase
    {
        private readonly IProjectService _projectService;

        public ProjectController(IProjectService projectService)
        {
            _projectService = projectService;
        }

        // GET: api/project
        [HttpGet]
        public async Task<ActionResult<List<ProjectDetailDto>>> GetAll()
        {
            var projects = await _projectService.GetAllProjectsAsync();
            return Ok(projects);
        }

        // GET: api/project/{id}
        [HttpGet("{id}")]
        public async Task<ActionResult<ProjectDetailDto>> GetById(int id)
        {
            var project = await _projectService.GetProjectByIdAsync(id);
            if (project == null)
            {
                return NotFound(new { message = $"Không tìm thấy dự án với ID {id}" });
            }
            return Ok(project);
        }

        // POST: api/project (Bước 1: Khởi tạo ý tưởng)
        [HttpPost]
        public async Task<ActionResult<ProjectDetailDto>> Create([FromBody] CreateProjectDto dto)
        {
            if (!ModelState.IsValid)
            {
                return BadRequest(ModelState);
            }

            var createdProject = await _projectService.CreateProjectAsync(dto);
            return CreatedAtAction(nameof(GetById), new { id = createdProject.Id }, createdProject);
        }

        // PUT: api/project/{id}/audience (Bước 2: Chân dung đối tượng)
        [HttpPut("{id}/audience")]
        public async Task<IActionResult> UpdateAudience(int id, [FromBody] UpdateAudienceDto dto)
        {
            if (!ModelState.IsValid)
            {
                return BadRequest(ModelState);
            }

            var result = await _projectService.UpdateAudienceAsync(id, dto);
            if (!result)
            {
                return NotFound(new { message = $"Không tìm thấy dự án với ID {id}" });
            }

            return Ok(new { message = "Cập nhật đối tượng người dùng thành công." });
        }

        // POST: api/project/{id}/requirements (Bước 3 & 4: Thêm tính năng / yêu cầu)
        [HttpPost("{id}/requirements")]
        public async Task<ActionResult<RequirementDto>> AddRequirement(int id, [FromBody] AddRequirementDto dto)
        {
            if (!ModelState.IsValid)
            {
                return BadRequest(ModelState);
            }

            try
            {
                var createdReq = await _projectService.AddRequirementAsync(id, dto);
                return Ok(createdReq);
            }
            catch (KeyNotFoundException ex)
            {
                return NotFound(new { message = ex.Message });
            }
        }

        // DELETE: api/project/{id}
        [HttpDelete("{id}")]
        public async Task<IActionResult> Delete(int id)
        {
            var result = await _projectService.DeleteProjectAsync(id);
            if (!result)
            {
                return NotFound(new { message = $"Không tìm thấy dự án với ID {id}" });
            }

            return Ok(new { message = "Xóa dự án thành công." });
        }
    }
}
