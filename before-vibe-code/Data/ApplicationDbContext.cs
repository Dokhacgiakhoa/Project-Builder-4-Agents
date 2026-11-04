using Microsoft.EntityFrameworkCore;
using Before_Vibe_Coding.Models.Entities;

namespace Before_Vibe_Coding.Data
{
    public class ApplicationDbContext : DbContext
    {
        public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options) : base(options)
        {
        }

        public DbSet<Project> Projects => Set<Project>();
        public DbSet<Requirement> Requirements => Set<Requirement>();
        public DbSet<ArchitectureConfig> ArchitectureConfigs => Set<ArchitectureConfig>();
        public DbSet<PromptArtifact> PromptArtifacts => Set<PromptArtifact>();

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);

            // Project - Requirements (1-N)
            modelBuilder.Entity<Project>()
                .HasMany(p => p.Requirements)
                .WithOne(r => r.Project)
                .HasForeignKey(r => r.ProjectId)
                .OnDelete(DeleteBehavior.Cascade);

            // Project - Architecture (1-1)
            modelBuilder.Entity<Project>()
                .HasOne(p => p.Architecture)
                .WithOne(a => a.Project)
                .HasForeignKey<ArchitectureConfig>(a => a.ProjectId)
                .OnDelete(DeleteBehavior.Cascade);

            // Project - PromptArtifacts (1-N)
            modelBuilder.Entity<Project>()
                .HasMany(p => p.Prompts)
                .WithOne(pr => pr.Project)
                .HasForeignKey(pr => pr.ProjectId)
                .OnDelete(DeleteBehavior.Cascade);
        }
    }
}
