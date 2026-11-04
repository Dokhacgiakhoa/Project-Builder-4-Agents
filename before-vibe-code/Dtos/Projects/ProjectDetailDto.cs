using System;
using System.Collections.Generic;
using Before_Vibe_Coding.Models.Entities;

namespace Before_Vibe_Coding.Dtos.Projects
{
    public class RequirementDto
    {
        public int Id { get; set; }
        public RequirementType Type { get; set; }
        public string Title { get; set; } = string.Empty;
        public string Description { get; set; } = string.Empty;
        public string Priority { get; set; } = string.Empty;
    }

    public class ArchitectureConfigDto
    {
        public int Id { get; set; }
        public string FrontendStack { get; set; } = string.Empty;
        public string BackendStack { get; set; } = string.Empty;
        public string DatabaseStack { get; set; } = string.Empty;
        public string MermaidDiagramCode { get; set; } = string.Empty;
    }

    public class PromptArtifactDto
    {
        public int Id { get; set; }
        public string RequirementsMarkdown { get; set; } = string.Empty;
        public string ArchitectureMarkdown { get; set; } = string.Empty;
        public string MasterPrompt { get; set; } = string.Empty;
        public DateTime GeneratedAt { get; set; }
    }

    public class ProjectDetailDto
    {
        public int Id { get; set; }
        public string Name { get; set; } = string.Empty;
        public string Description { get; set; } = string.Empty;
        public string TargetAudience { get; set; } = string.Empty;
        public string Status { get; set; } = string.Empty;
        public DateTime CreatedAt { get; set; }
        public DateTime? UpdatedAt { get; set; }

        public List<RequirementDto> Requirements { get; set; } = new();
        public ArchitectureConfigDto? Architecture { get; set; }
        public List<PromptArtifactDto> Prompts { get; set; } = new();
    }
}
