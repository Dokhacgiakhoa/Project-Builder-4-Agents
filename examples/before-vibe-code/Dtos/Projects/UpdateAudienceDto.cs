using System.ComponentModel.DataAnnotations;

namespace Before_Vibe_Coding.Dtos.Projects
{
    public class UpdateAudienceDto
    {
        [Required(ErrorMessage = "Target audience is required")]
        public string TargetAudience { get; set; } = string.Empty;
    }
}
