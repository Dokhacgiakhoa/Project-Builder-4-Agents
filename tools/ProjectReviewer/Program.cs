namespace ProjectReviewer;

using System;
using System.Diagnostics;
using System.Runtime.InteropServices;
using System.Windows.Forms;

static class Program
{
    [DllImport("kernel32.dll")]
    private static extern bool AttachConsole(int dwProcessId);
    private const int ATTACH_PARENT_PROCESS = -1;

    [STAThread]
    static int Main(string[] args)
    {
        // Hỗ trợ chế độ CLI trực tiếp qua 1 file EXE duy nhất (audit, serve, --help)
        if (args.Length > 0 && (args[0] == "audit" || args[0] == "--audit" || args[0] == "serve" || args[0] == "--help" || args[0] == "-h"))
        {
            AttachConsole(ATTACH_PARENT_PROCESS);
            string? enginePath = MainForm.FindBundledEngine();
            if (enginePath == null)
            {
                Console.Error.WriteLine("[ERROR] The embedded Core Engine was not found in this build.");
                return 1;
            }

            var psi = new ProcessStartInfo
            {
                FileName = enginePath,
                Arguments = string.Join(" ", args),
                UseShellExecute = false,
                CreateNoWindow = true,
                RedirectStandardOutput = true,
                RedirectStandardError = true
            };

            using var proc = Process.Start(psi);
            if (proc == null) return 1;

            proc.OutputDataReceived += (s, e) => { if (e.Data != null) Console.WriteLine(e.Data); };
            proc.ErrorDataReceived += (s, e) => { if (e.Data != null) Console.Error.WriteLine(e.Data); };
            proc.BeginOutputReadLine();
            proc.BeginErrorReadLine();
            proc.WaitForExit();
            return proc.ExitCode;
        }

        ApplicationConfiguration.Initialize();
        Application.ApplicationExit += (sender, e) => { /* graceful shutdown handlers */ };
        Application.Run(new MainForm(args));
        return 0;
    }
}
