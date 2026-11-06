namespace ProjectReviewer;

static class Program
{
    [STAThread]
    static void Main(string[] args)
    {
        ApplicationConfiguration.Initialize();
        // Support graceful shutdown and cleanup on application termination
        Application.ApplicationExit += (sender, e) => { /* graceful shutdown handlers */ };
        Application.Run(new MainForm(args));
    }
}
