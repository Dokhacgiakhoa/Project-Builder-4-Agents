using System.ComponentModel.DataAnnotations;

namespace Before_Vibe_Coding.Dtos.Projects
{
    public class UpdateAudienceDto
    {
        [Required(ErrorMessage = "Đối tượng người dùng không được để trống")]
        public string TargetAudience { get; set; } = string.Empty;
    }
}
