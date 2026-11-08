using System;
using System.IO;
using System.Net;
using System.Net.Sockets;
using System.Drawing;
using System.Diagnostics;
using System.Windows.Forms;
using System.Threading.Tasks;
using System.Runtime.InteropServices;
using Microsoft.Web.WebView2.WinForms;
using Microsoft.Web.WebView2.Core;

namespace ProjectReviewer;

public class MainForm : Form
{
    [DllImport("dwmapi.dll")]
    private static extern int DwmSetWindowAttribute(IntPtr hwnd, int attr, ref int attrValue, int attrSize);

    private const int DWMWA_USE_IMMERSIVE_DARK_MODE = 20;
    private const int DWMWA_BORDER_COLOR = 34;
    private const int DWMWA_CAPTION_COLOR = 35;

    private readonly WebView2 _webView;
    private Process? _pythonProcess;
    private int _serverPort = 8998;

    public MainForm(string[] args)
    {
        // 1. Standard native Windows Form configuration
        Text = "Project Builder Analytics";
        Width = 1260;
        Height = 840;
        StartPosition = FormStartPosition.CenterScreen;
        BackColor = Color.FromArgb(14, 13, 19); // #0e0d13 (Dark Slate)

        // 2. Load the icon from app-icon.ico
        LoadCustomIcon();

        // 3. Lock the title bar to native Dark Mode through the Windows DWM API
        ApplyDwmDarkTitleBar();

        // 4. Initialize the WebView2 control
        _webView = new WebView2
        {
            Dock = DockStyle.Fill,
            BackColor = Color.FromArgb(5, 5, 7) // #050507
        };
        Controls.Add(_webView);

        // 5. Event lifecycle
        Load += OnFormLoadAsync;
        FormClosing += OnFormClosing;
    }

    private void LoadCustomIcon()
    {
        try
        {
            string appDir = AppContext.BaseDirectory;
            string[] iconCandidates = new[]
            {
                Path.Combine(appDir, "app-icon.ico"),
                Path.Combine(appDir, "assets", "app-icon.ico"),
                Path.Combine(Directory.GetCurrentDirectory(), "assets", "app-icon.ico"),
                Path.Combine(Directory.GetCurrentDirectory(), "app-icon.ico")
            };

            foreach (var p in iconCandidates)
            {
                if (File.Exists(p))
                {
                    Icon = new Icon(p);
                    break;
                }
            }
        }
        catch { }
    }

    private void ApplyDwmDarkTitleBar()
    {
        try
        {
            // Enable Immersive Dark Mode
            int darkMode = 1;
            DwmSetWindowAttribute(Handle, DWMWA_USE_IMMERSIVE_DARK_MODE, ref darkMode, sizeof(int));

            // Lock the caption bar color to Dark Slate (#0e0d13 -> BGR: 0x130D0E)
            int captionColor = 0x130D0E;
            DwmSetWindowAttribute(Handle, DWMWA_CAPTION_COLOR, ref captionColor, sizeof(int));

            // Lock the border color to Slate Subtle (#1e1d27 -> BGR: 0x271D1E)
            int borderColor = 0x271D1E;
            DwmSetWindowAttribute(Handle, DWMWA_BORDER_COLOR, ref borderColor, sizeof(int));
        }
        catch { }
    }

    private static int GetFreePort()
    {
        try
        {
            var l = new TcpListener(IPAddress.Loopback, 0);
            l.Start();
            int port = ((IPEndPoint)l.LocalEndpoint).Port;
            l.Stop();
            return port;
        }
        catch
        {
            return 8998;
        }
    }

    private async void OnFormLoadAsync(object? sender, EventArgs e)
    {
        try
        {
            _serverPort = GetFreePort();

            // Prefer the packaged Engine (no Python needed). Only when it is missing use Python >= 3.12
            // (installed through winget if missing, with a prompt to the user). The WebView2 Runtime is checked the same way.
            string? enginePath = FindBundledEngine();
            string? pythonExe = null;
            if (enginePath == null)
            {
                pythonExe = await EnsurePythonAsync();
                if (pythonExe == null) { Close(); return; }
            }
            if (!await EnsureWebView2Async()) { Close(); return; }

            // Start the Backend Server in headless mode
            if (!StartBackend(_serverPort, enginePath, pythonExe)) { Close(); return; }

            // Wait for the server to be ready (up to 3 seconds)
            await WaitForServerReadyAsync(_serverPort);

            // Initialize the WebView2 Environment
            string profileDir = Path.Combine(
                Environment.GetFolderPath(Environment.SpecialFolder.UserProfile),
                ".starter-kit",
                "webview2_profile"
            );
            Directory.CreateDirectory(profileDir);

            var env = await CoreWebView2Environment.CreateAsync(null, profileDir);
            await _webView.EnsureCoreWebView2Async(env);

            // Tune WebView2 to remove the browser chrome entirely
            _webView.CoreWebView2.Settings.IsStatusBarEnabled = false;
            _webView.CoreWebView2.Settings.IsBuiltInErrorPageEnabled = false;
            _webView.CoreWebView2.Settings.AreDevToolsEnabled = false;
            _webView.CoreWebView2.Settings.AreDefaultContextMenusEnabled = true;

            // Handle native communication events (Windows 11 modern folder picker)
            _webView.CoreWebView2.WebMessageReceived += (s, args) =>
            {
                try
                {
                    string msg = args.TryGetWebMessageAsString();
                    if (msg == "select-folder")
                    {
                        Invoke(() =>
                        {
                            using var dlg = new FolderBrowserDialog
                            {
                                Description = "Select the project folder to review",
                                UseDescriptionForTitle = true,
                                AutoUpgradeEnabled = true
                            };
                            if (dlg.ShowDialog(this) == DialogResult.OK)
                            {
                                string json = System.Text.Json.JsonSerializer.Serialize(dlg.SelectedPath);
                                _webView.CoreWebView2.ExecuteScriptAsync($"onFolderSelected({json})");
                            }
                        });
                    }
                }
                catch { }
            };

            // Navigate to the Antigravity 2.0 Web Canvas UI
            _webView.Source = new Uri($"http://127.0.0.1:{_serverPort}");
        }
        catch (Exception ex)
        {
            MessageBox.Show(
                $"Failed to start the interface: {ex.Message}\nPlease check the Python and WebView2 environment.",
                "Startup Error",
                MessageBoxButtons.OK,
                MessageBoxIcon.Error
            );
        }
    }

    private async Task<string?> EnsurePythonAsync()
    {
        string? pythonExe = PythonRuntime.Find();
        if (pythonExe != null) return pythonExe;

        var answer = MessageBox.Show(
            "The audit engine needs Python 3.12 or newer, which was not found on this computer.\n\n" +
            "Install Python 3.12 automatically with winget now?",
            "Python Missing",
            MessageBoxButtons.YesNo,
            MessageBoxIcon.Question);
        if (answer != DialogResult.Yes) return null;

        Text = "Installing Python 3.12...";
        bool installed = await PythonRuntime.InstallWithWingetAsync(PythonRuntime.WingetPythonId);
        pythonExe = installed ? PythonRuntime.Find() : null;
        if (pythonExe == null)
        {
            MessageBox.Show(
                "Automatic installation failed. Please install Python 3.12+ manually from:\n" + PythonRuntime.PythonDownloadUrl,
                "Python Installation Failed",
                MessageBoxButtons.OK,
                MessageBoxIcon.Warning);
        }
        Text = "Project Builder Analytics";
        return pythonExe;
    }

    private async Task<bool> EnsureWebView2Async()
    {
        try
        {
            if (!string.IsNullOrEmpty(CoreWebView2Environment.GetAvailableBrowserVersionString())) return true;
        }
        catch (Exception)
        {
            // No WebView2 Runtime: try to install it below.
        }

        var answer = MessageBox.Show(
            "The app needs the Microsoft Edge WebView2 Runtime to show its interface, but it was not found.\n\n" +
            "Install it automatically with winget now?",
            "WebView2 Runtime Missing",
            MessageBoxButtons.YesNo,
            MessageBoxIcon.Question);
        if (answer != DialogResult.Yes) return false;

        Text = "Installing WebView2 Runtime...";
        bool installed = await PythonRuntime.InstallWithWingetAsync(PythonRuntime.WingetWebView2Id);
        Text = "Project Builder Analytics";
        if (!installed)
        {
            MessageBox.Show(
                "Automatic installation failed. Please download the WebView2 Runtime from Microsoft and run the app again.",
                "WebView2 Installation Failed",
                MessageBoxButtons.OK,
                MessageBoxIcon.Warning);
        }
        return installed;
    }

    /// <summary>Finds the packaged engine: prefers engine\reviewer-engine.exe next to the exe, otherwise extracts it from the EmbeddedResource into a temp folder.</summary>
    public static string? FindBundledEngine()
    {
        // 1. Check for an engine right next to the exe (for dev / unbundled environments)
        string candidate = Path.Combine(AppContext.BaseDirectory, "engine", "reviewer-engine.exe");
        if (File.Exists(candidate))
        {
            return candidate;
        }

        // 2. Extract with SHA-256 verification from the Embedded Resource into a hash-named folder (ADR-0025)
        return EngineExtractor.Extract(typeof(MainForm).Assembly);
    }

    private bool StartBackend(int port, string? enginePath, string? pythonExe)
    {
        if (enginePath != null)
        {
            var enginePsi = new ProcessStartInfo
            {
                FileName = enginePath,
                Arguments = $"serve --server-only --port={port}",
                WorkingDirectory = Path.GetDirectoryName(enginePath) ?? AppContext.BaseDirectory,
                CreateNoWindow = true,
                UseShellExecute = false,
                WindowStyle = ProcessWindowStyle.Hidden
            };
            _pythonProcess = Process.Start(enginePsi);
            return _pythonProcess != null;
        }

        if (pythonExe == null) return false;

        string baseDir = AppContext.BaseDirectory;
        string projectRoot = baseDir;

        // Find the root folder containing scripts/reviewer_app.py
        for (int i = 0; i < 4; i++)
        {
            if (File.Exists(Path.Combine(projectRoot, "scripts", "reviewer_app.py")))
            {
                break;
            }
            string parent = Path.GetDirectoryName(projectRoot) ?? projectRoot;
            if (parent == projectRoot) break;
            projectRoot = parent;
        }

        string scriptPath = Path.Combine(projectRoot, "scripts", "reviewer_app.py");

        if (!File.Exists(scriptPath))
        {
            MessageBox.Show(
                "The embedded Core Engine was not found in this build, and scripts\\reviewer_app.py is not next to Project-Builder-Analytics.exe.\nRebuild with: python scripts/build_exe.py",
                "Core Engine Missing",
                MessageBoxButtons.OK,
                MessageBoxIcon.Error);
            return false;
        }

        var psi = new ProcessStartInfo
        {
            FileName = pythonExe,
            Arguments = $"\"{scriptPath}\" --server-only --port={port}",
            WorkingDirectory = projectRoot,
            CreateNoWindow = true,
            UseShellExecute = false,
            WindowStyle = ProcessWindowStyle.Hidden
        };

        _pythonProcess = Process.Start(psi);
        return _pythonProcess != null;
    }

    private static async Task WaitForServerReadyAsync(int port)
    {
        using var client = new HttpClient { Timeout = TimeSpan.FromMilliseconds(500) };
        for (int i = 0; i < 40; i++)
        {
            try
            {
                var resp = await client.GetAsync($"http://127.0.0.1:{port}/api/status");
                if (resp.IsSuccessStatusCode) return;
            }
            catch
            {
                await Task.Delay(120);
            }
        }
    }

    private void OnFormClosing(object? sender, FormClosingEventArgs e)
    {
        try
        {
            if (_pythonProcess != null && !_pythonProcess.HasExited)
            {
                _pythonProcess.Kill(true);
            }
        }
        catch { }
    }
}
