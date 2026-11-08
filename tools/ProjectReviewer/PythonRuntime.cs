using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Threading.Tasks;

namespace ProjectReviewer;

/// <summary>
/// Dò tìm Python (>= 3.12) cho Core Engine và tự cài đặt qua winget khi thiếu (có hỏi người dùng trước).
/// </summary>
internal static class PythonRuntime
{
    public const int MinVersion = 312; // 3.12
    public const string WingetPythonId = "Python.Python.3.12";
    public const string WingetWebView2Id = "Microsoft.EdgeWebView2Runtime";
    public const string PythonDownloadUrl = "https://www.python.org/downloads/";

    /// <summary>Trả về đường dẫn python.exe phù hợp (>= 3.12), hoặc null nếu không có.</summary>
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

        // Python Launcher (py.exe) giúp tìm bản mới nhất, kể cả khi PATH chưa được làm mới.
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

    /// <summary>Chạy thử interpreter, trả về (phiên bản dạng 312, đường dẫn thật) hoặc null nếu không chạy được.</summary>
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
                try { proc.Kill(true); } catch { /* bỏ qua */ }
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
            // Không có interpreter này (hoặc là stub của Microsoft Store): thử ứng viên kế tiếp.
            return null;
        }
    }

    /// <summary>Cài một gói bằng winget ở chế độ im lặng. Trả về true nếu winget kết thúc thành công.</summary>
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
                // winget không có trên máy này.
                return false;
            }
        });
    }
}
