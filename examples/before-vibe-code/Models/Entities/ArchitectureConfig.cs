using System;

namespace Before_Vibe_Coding.Models.Entities
{
    public class ArchitectureConfig
    {
        public int Id { get; set; }
        public int ProjectId { get; set; }
        public string FrontendStack { get; set; } = string.Empty;
        public string BackendStack { get; set; } = string.Empty;
        public string DatabaseStack { get; set; } = string.Empty;
        public string MermaidDiagramCode { get; set; } = string.Empty;
        public DateTime CreatedAt { get; set; } = DateTime.UtcNow;

        // Navigation property
        public Project? Project { get; set; }
    }
}
