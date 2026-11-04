using System;

namespace Before_Vibe_Coding.Models.Entities
{
    public class PromptArtifact
    {
        public int Id { get; set; }
        public int ProjectId { get; set; }
        public string RequirementsMarkdown { get; set; } = string.Empty;
        public string ArchitectureMarkdown { get; set; } = string.Empty;
        public string MasterPrompt { get; set; } = string.Empty;
        public DateTime GeneratedAt { get; set; } = DateTime.UtcNow;

        // Navigation property
        public Project? Project { get; set; }
    }
}
