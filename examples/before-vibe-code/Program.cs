using AutoWrapper;
using Microsoft.EntityFrameworkCore;
using Before_Vibe_Coding.Data;
using Before_Vibe_Coding.Repositories;
using Before_Vibe_Coding.Services;

var builder = WebApplication.CreateBuilder(args);

// 1. Add Services to the container (Web API Controllers)
builder.Services.AddControllers();

// 2. Configure Database Context (Entity Framework Core)
var connectionString = builder.Configuration.GetConnectionString("DefaultConnection") 
    ?? "Server=.;Database=BeforeVibeCodingDb;Trusted_Connection=True;TrustServerCertificate=True;";
builder.Services.AddDbContext<ApplicationDbContext>(options =>
    options.UseSqlServer(connectionString));

// 3. Register Dependency Injection (Repository & Service Pattern)
builder.Services.AddScoped<IProjectRepository, ProjectRepository>();
builder.Services.AddScoped<IProjectService, ProjectService>();

// 4. Configure Swagger / OpenAPI
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

// 5. Configure CORS for Frontend (Local Dev & Production)
builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowAll", policy =>
    {
        policy.AllowAnyOrigin()
              .AllowAnyMethod()
              .AllowAnyHeader();
    });
});

var app = builder.Build();

// 6. Configure HTTP Request Pipeline
if (app.Environment.IsDevelopment())
{
    app.UseDeveloperExceptionPage();
}

// 7. Swagger Documentation tại /swagger
app.UseSwagger();
app.UseSwaggerUI(c =>
{
    c.SwaggerEndpoint("/swagger/v1/swagger.json", "Before Vibe Coding API v1");
    c.RoutePrefix = "swagger"; // Swagger UI tại http://localhost:port/swagger
});

// 8. AutoWrapper - Chuẩn hóa Response và Exception cho các API (/api/...)
app.UseApiResponseAndExceptionWrapper(new AutoWrapperOptions
{
    ShowStatusCode = true,
    IsApiOnly = false,
    WrapWhenApiPathStartsWith = "/api"
});

app.UseHttpsRedirection();

app.UseCors("AllowAll");

// 9. Host Giao Diện Web Frontend (React UI)
app.UseDefaultFiles();
app.UseStaticFiles();

app.UseRouting();

app.UseAuthorization();

app.MapControllers();

// 10. SPA Fallback (Điều hướng mọi route không phải API về trang web React)
app.MapFallbackToFile("index.html");

app.Run();
