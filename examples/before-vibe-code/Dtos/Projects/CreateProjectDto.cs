using System.ComponentModel.DataAnnotations;

namespace Before_Vibe_Coding.Dtos.Projects
{
    public class CreateProjectDto
    {
        [Required(ErrorMessage = "Tên dự án không được để trống")]
        [MaxLength(150, ErrorMessage = "Tên dự án tối đa 150 ký tự")]
        public string Name { get; set; } = string.Empty;

        [Required(ErrorMessage = "Mô tả dự án không được để trống")]
        public string Description { get; set; } = string.Empty;
    }
}
