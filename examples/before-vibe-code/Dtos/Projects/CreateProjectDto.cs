using System.ComponentModel.DataAnnotations;

namespace Before_Vibe_Coding.Dtos.Projects
{
    public class CreateProjectDto
    {
        [Required(ErrorMessage = "Project name is required")]
        [MaxLength(150, ErrorMessage = "Project name cannot exceed 150 characters")]
        public string Name { get; set; } = string.Empty;

        [Required(ErrorMessage = "Project description is required")]
        public string Description { get; set; } = string.Empty;
    }
}
