using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Threading.Tasks;

namespace ProjectReviewer;

/// <summary>
/// Detects Python (>= 3.12) for the Core Engine and installs it through winget when missing (asking the user first).
/// </summary>
internal static class PythonRuntime
{
    public const int MinVersion = 312; // 3.12
    public const string WingetPythonId = "Python.Python.3.12";
    public const string WingetWebView2Id = "Microsoft.EdgeWebView2Runtime";
    public const string PythonDownloadUrl = "https://www.python.org/downloads/";

    /// <summary>Returns the path of a suitable python.exe (>= 3.12), or null if none.</summary>
    public static string? Find()
    {
        string? best = null;
        int bestVersion = 0;

        foreach (var (exe, args) in Candidates())
        {
            var probed = Probe(exe, args);
            if (probed is { } p && p.Version >= MinVersion && p.Version > bestVersion)
            {
                best = p.Executable;
                bestVersion = p.Version;
            }
        }
        return best;
    }

    private static IEnumerable<(string Exe, string Args)> Candidates()
    {
        string local = Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData);
        string programFiles = Environment.GetFolderPath(Environment.SpecialFolder.ProgramFiles);

        // The Python Launcher (py.exe) finds the newest version, even when PATH has not been refreshed.
        yield return ("py", "-3");

        foreach (string v in new[] { "314", "313", "312" })
        {
            string perUser = Path.Combine(local, "Programs", "Python", "Python" + v, "python.exe");
            if (File.Exists(perUser)) yield return (perUser, "");

            string perMachine = Path.Combine(programFiles, "Python" + v, "python.exe");
            if (File.Exists(perMachine)) yield return (perMachine, "");
        }

        yield return ("python", "");
    }

    /// <summary>Runs the interpreter as a trial; returns (version as 312, real path) or null if it cannot run.</summary>
    private static (int Version, string Executable)? Probe(string exe, string args)
    {
        try
        {
            var psi = new ProcessStartInfo
            {
                FileName = exe,
                Arguments = (args.Length > 0 ? args + " " : "")
                    + "-c \"import sys;print(sys.version_info[0]*100+sys.version_info[1],sys.executable,sep='|')\"",
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                UseShellExecute = false,
                CreateNoWindow = true
            };
            using var proc = Process.Start(psi);
            if (proc == null) return null;

            if (!proc.WaitForExit(5000))
            {
                try { proc.Kill(true); } catch { /* ignore */ }
                return null;
            }
            if (proc.ExitCode != 0) return null;

            string output = proc.StandardOutput.ReadToEnd().Trim();
            int sep = output.IndexOf('|');
            if (sep <= 0) return null;
            if (!int.TryParse(output[..sep], out int version)) return null;

            string path = output[(sep + 1)..].Trim();
            return File.Exists(path) ? (version, path) : null;
        }
        catch (Exception)
        {
            // This interpreter is not available (or is a Microsoft Store stub): try the next candidate.
            return null;
        }
    }

    /// <summary>Installs a package with winget in silent mode. Returns true if winget finished successfully.</summary>
    public static Task<bool> InstallWithWingetAsync(string packageId)
    {
        return Task.Run(() =>
        {
            try
            {
                var psi = new ProcessStartInfo
                {
                    FileName = "winget",
                    Arguments = $"install --id {packageId} -e --silent --accept-package-agreements --accept-source-agreements",
                    UseShellExecute = false,
                    CreateNoWindow = true
                };
                using var proc = Process.Start(psi);
                if (proc == null) return false;
                if (!proc.WaitForExit(15 * 60 * 1000)) return false;
                return proc.ExitCode == 0;
            }
            catch (Exception)
            {
                // winget is not available on this machine.
                return false;
            }
        });
    }
}
