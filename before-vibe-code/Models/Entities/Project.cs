using System;
using System.Collections.Generic;

namespace Before_Vibe_Coding.Models.Entities
{
    public class Project
    {
        public int Id { get; set; }
        public string Name { get; set; } = string.Empty;
        public string Description { get; set; } = string.Empty;
        public string TargetAudience { get; set; } = string.Empty;
        public string Status { get; set; } = "Draft"; // Draft, InProgress, Completed
        public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
        public DateTime? UpdatedAt { get; set; }

        // Navigation properties
        public ICollection<Requirement> Requirements { get; set; } = new List<Requirement>();
        public ArchitectureConfig? Architecture { get; set; }
        public ICollection<PromptArtifact> Prompts { get; set; } = new List<PromptArtifact>();
    }
}
