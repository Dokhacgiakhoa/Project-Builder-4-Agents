using System;

namespace Before_Vibe_Coding.Models.Entities
{
    public enum RequirementType
    {
        Functional = 1,
        NonFunctional = 2
    }

    public class Requirement
    {
        public int Id { get; set; }
        public int ProjectId { get; set; }
        public RequirementType Type { get; set; } = RequirementType.Functional;
        public string Title { get; set; } = string.Empty;
        public string Description { get; set; } = string.Empty;
        public string Priority { get; set; } = "Medium"; // High, Medium, Low
        public DateTime CreatedAt { get; set; } = DateTime.UtcNow;

        // Navigation property
        public Project? Project { get; set; }
    }
}
