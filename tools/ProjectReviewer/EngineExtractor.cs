using System;
using System.Diagnostics;
using System.IO;
using System.Reflection;
using System.Security.Cryptography;
using System.Threading;

namespace ProjectReviewer;

/// <summary>
/// Extracts the embedded Core Engine (ADR-0022) to a content-addressed folder:
///   %TEMP%\ProjectHealthCheck\engine\&lt;sha256-prefix&gt;\reviewer-engine.exe
/// An existing file is reused only after its SHA-256 matches the embedded resource, so a rebuilt engine
/// (even with the same length), a corrupted file or a planted file is never executed silently, and a
/// running older engine (locked file) never blocks starting a newer one: each build has its own folder.
/// A named mutex per build serializes check, delete and publish across instances. (ADR-0025)
/// </summary>
internal static class EngineExtractor
{
    public const string ResourceName = "reviewer-engine.exe";
    private const string ExeName = "reviewer-engine.exe";
    private static readonly TimeSpan LockTimeout = TimeSpan.FromSeconds(20);

    public static string BaseDir =>
        Path.Combine(Path.GetTempPath(), "ProjectHealthCheck", "engine");

    /// <summary>Returns the path of a verified engine, or null when no engine is embedded or extraction failed.</summary>
    public static string? Extract(Assembly assembly, string? baseDir = null) =>
        Extract(() => assembly.GetManifestResourceStream(ResourceName), baseDir);

    /// <summary>Same, for any seekable source (used by tools/EngineExtractorCheck).</summary>
    public static string? Extract(Func<Stream?> openResource, string? baseDir = null)
    {
        try
        {
            baseDir ??= BaseDir;
            using var resource = openResource();
            if (resource == null) return null;

            string expected = Convert.ToHexString(SHA256.HashData(resource));
            string prefix = expected[..16];
            string folder = Path.Combine(baseDir, prefix);
            Directory.CreateDirectory(folder);
            string target = Path.Combine(folder, ExeName);

            // Fast path without the lock: a verified file is immutable (nobody replaces it while valid).
            if (HashMatches(target, expected)) return target;

            using var mutex = new Mutex(false, "Local\\ProjectHealthCheck.engine." + prefix);
            bool held = false;
            try
            {
                try { held = mutex.WaitOne(LockTimeout); }
                catch (AbandonedMutexException) { held = true; }

                return held
                    ? PublishLocked(resource, expected, baseDir, folder, target)
                    : PrivateCopy(resource, folder); // could not get the lock in time: never block startup
            }
            finally
            {
                if (held) mutex.ReleaseMutex();
            }
        }
        catch (Exception ex)
        {
            Debug.WriteLine($"[ERROR] Could not extract the embedded engine: {ex.Message}");
            return null;
        }
    }

    private static string? PublishLocked(Stream resource, string expected, string baseDir, string folder, string target)
    {
        if (HashMatches(target, expected)) return target; // another instance published it while we waited

        // Wrong content (corrupted or planted): remove it if possible; a locked file is handled below.
        if (File.Exists(target)) TryDelete(target);

        resource.Position = 0;
        string temp = Path.Combine(folder, ExeName + "." + Environment.ProcessId + "." + Guid.NewGuid().ToString("N") + ".tmp");
        using (var fs = new FileStream(temp, FileMode.CreateNew, FileAccess.Write, FileShare.None))
        {
            resource.CopyTo(fs);
        }

        try
        {
            File.Move(temp, target, overwrite: false);
        }
        catch (Exception ex) when (ex is IOException || ex is UnauthorizedAccessException)
        {
            TryDelete(temp);
            // Still wrong content that cannot be replaced (locked): use a private verified copy for this process.
            return HashMatches(target, expected) ? target : PrivateCopy(resource, folder);
        }

        if (!HashMatches(target, expected)) return PrivateCopy(resource, folder);

        PruneOtherBuilds(baseDir, Path.GetFileName(folder));
        return target;
    }

    private static string PrivateCopy(Stream resource, string folder)
    {
        string own = Path.Combine(folder, "own-" + Environment.ProcessId, ExeName);
        Directory.CreateDirectory(Path.GetDirectoryName(own)!);
        resource.Position = 0;
        using var fs = new FileStream(own, FileMode.Create, FileAccess.Write, FileShare.None);
        resource.CopyTo(fs);
        return own;
    }

    private static bool HashMatches(string path, string expectedHex)
    {
        try
        {
            if (!File.Exists(path)) return false;
            using var fs = new FileStream(path, FileMode.Open, FileAccess.Read, FileShare.ReadWrite | FileShare.Delete);
            return string.Equals(Convert.ToHexString(SHA256.HashData(fs)), expectedHex, StringComparison.OrdinalIgnoreCase);
        }
        catch (IOException) { return false; }
        catch (UnauthorizedAccessException) { return false; }
    }

    /// <summary>Best effort: remove folders of other builds and the pre-ADR-0025 flat file. A running engine locks its file, so its folder survives.</summary>
    private static void PruneOtherBuilds(string baseDir, string keepFolderName)
    {
        try
        {
            TryDelete(Path.Combine(baseDir, ExeName)); // legacy location
            foreach (var dir in Directory.GetDirectories(baseDir))
            {
                if (string.Equals(Path.GetFileName(dir), keepFolderName, StringComparison.OrdinalIgnoreCase)) continue;
                try { Directory.Delete(dir, recursive: true); } catch { /* in use: keep */ }
            }
        }
        catch { /* never block startup */ }
    }

    private static void TryDelete(string path)
    {
        try { if (File.Exists(path)) File.Delete(path); } catch { /* ignore */ }
    }
}
