using System.ComponentModel.DataAnnotations;
using Before_Vibe_Coding.Models.Entities;

namespace Before_Vibe_Coding.Dtos.Requirements
{
    public class AddRequirementDto
    {
        public RequirementType Type { get; set; } = RequirementType.Functional;

        [Required(ErrorMessage = "Requirement title is required")]
        public string Title { get; set; } = string.Empty;

        public string Description { get; set; } = string.Empty;
        public string Priority { get; set; } = "Medium";
    }
}
