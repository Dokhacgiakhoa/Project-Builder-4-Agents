using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;
using Before_Vibe_Coding.Data;
using Before_Vibe_Coding.Models.Entities;

namespace Before_Vibe_Coding.Repositories
{
    public class ProjectRepository : IProjectRepository
    {
        private readonly ApplicationDbContext _context;

        public ProjectRepository(ApplicationDbContext context)
        {
            _context = context;
        }

        public async Task<List<Project>> GetAllProjectsAsync()
        {
            try
            {
                return await _context.Projects
                    .Include(p => p.Requirements)
                    .Include(p => p.Architecture)
                    .AsNoTracking()
                    .ToListAsync();
            }
            catch (Exception)
            {
                throw;
            }
        }

        public async Task<Project?> GetProjectByIdAsync(int id)
        {
            try
            {
                return await _context.Projects
                    .Include(p => p.Requirements)
                    .Include(p => p.Architecture)
                    .Include(p => p.Prompts)
                    .FirstOrDefaultAsync(p => p.Id == id);
            }
            catch (Exception)
            {
                throw;
            }
        }

        public async Task<Project> AddProjectAsync(Project project)
        {
            try
            {
                await _context.Projects.AddAsync(project);
                await _context.SaveChangesAsync();
                return project;
            }
            catch (Exception)
            {
                throw;
            }
        }

        public async Task<bool> UpdateProjectAsync(Project project)
        {
            try
            {
                project.UpdatedAt = DateTime.UtcNow;
                _context.Projects.Update(project);
                return await _context.SaveChangesAsync() > 0;
            }
            catch (Exception)
            {
                throw;
            }
        }

        public async Task<bool> DeleteProjectAsync(int id)
        {
            try
            {
                var project = await _context.Projects.FindAsync(id);
                if (project == null) return false;

                _context.Projects.Remove(project);
                return await _context.SaveChangesAsync() > 0;
            }
            catch (Exception)
            {
                throw;
            }
        }

        public async Task<Requirement> AddRequirementAsync(Requirement requirement)
        {
            try
            {
                await _context.Requirements.AddAsync(requirement);
                await _context.SaveChangesAsync();
                return requirement;
            }
            catch (Exception)
            {
                throw;
            }
        }
    }
}
