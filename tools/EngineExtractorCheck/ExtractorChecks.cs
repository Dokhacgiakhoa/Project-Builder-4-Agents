using System.Security.Cryptography;
using ProjectReviewer;

// Scenarios for EngineExtractor (ADR-0025). Exit code 0 = all passed.
int failures = 0;
void Check(string name, bool ok, string detail = "")
{
    Console.WriteLine($"{(ok ? "PASS" : "FAIL")}  {name}{(detail.Length > 0 ? "  [" + detail + "]" : "")}");
    if (!ok) failures++;
}

static byte[] Payload(byte seed, int length = 200_000)
{
    var b = new byte[length];
    new Random(seed).NextBytes(b);
    return b;
}
static string Hash(string path) => Convert.ToHexString(SHA256.HashData(File.ReadAllBytes(path)));
static string HashBytes(byte[] b) => Convert.ToHexString(SHA256.HashData(b));
static Func<Stream?> Source(byte[] b) => () => new MemoryStream(b);

string root = Path.Combine(Path.GetTempPath(), "EngineExtractorCheck-" + Guid.NewGuid().ToString("N"));
Directory.CreateDirectory(root);
try
{
    var a = Payload(1);
    var b = Payload(2); // same length as a, different content
    Check("payloads have equal length and different content", a.Length == b.Length && HashBytes(a) != HashBytes(b));

    // 1. fresh extraction
    string? p1 = EngineExtractor.Extract(Source(a), root);
    Check("1 fresh extract returns a file with the right SHA-256", p1 != null && File.Exists(p1) && Hash(p1) == HashBytes(a));

    // 2. reuse without rewriting
    var t1 = File.GetLastWriteTimeUtc(p1!);
    Thread.Sleep(50);
    string? p2 = EngineExtractor.Extract(Source(a), root);
    Check("2 second call reuses the same verified file", p2 == p1 && File.GetLastWriteTimeUtc(p2!) == t1);

    // 3. tampered file with the same length is replaced (old behaviour: reused by size)
    var tampered = (byte[])a.Clone();
    tampered[0] ^= 0xFF;
    File.WriteAllBytes(p1!, tampered);
    string? p3 = EngineExtractor.Extract(Source(a), root);
    Check("3 same-size tampered file is replaced by the verified engine", p3 != null && Hash(p3) == HashBytes(a));

    // 4. tampered AND locked: must not return the tampered file
    File.WriteAllBytes(p1!, tampered);
    using (var lockHandle = new FileStream(p1!, FileMode.Open, FileAccess.Read, FileShare.Read))
    {
        string? p4 = EngineExtractor.Extract(Source(a), root);
        Check("4 locked tampered file is never returned; a private verified copy is used",
            p4 != null && p4 != p1 && Hash(p4) == HashBytes(a), p4 ?? "null");
    }
    File.WriteAllBytes(p1!, a); // restore for the next scenarios

    // 5. a rebuilt engine with the same length gets its own folder (old behaviour: stale engine kept)
    string? pb = EngineExtractor.Extract(Source(b), root);
    Check("5 same-length new build is extracted separately and verified",
        pb != null && pb != p1 && Hash(pb) == HashBytes(b));

    // 6. older build folder is pruned when it is not in use
    Check("6 old build folder was pruned after publishing the new build", !File.Exists(p1!));

    // 7. an older build that is still running does not block the newer one
    string? pa2 = EngineExtractor.Extract(Source(a), root); // recreate A, which prunes B
    using (var running = new FileStream(pa2!, FileMode.Open, FileAccess.Read, FileShare.Read))
    {
        string? pb2 = EngineExtractor.Extract(Source(b), root);
        Check("7 newer build starts while the older engine file is locked",
            pb2 != null && Hash(pb2) == HashBytes(b) && File.Exists(pa2!), pb2 ?? "null");
    }

    // 8. concurrent extraction of the same build
    string root2 = Path.Combine(root, "concurrent");
    var results = new string?[16];
    var errors = new List<string>();
    Parallel.For(0, results.Length, i =>
    {
        try { results[i] = EngineExtractor.Extract(Source(a), root2); }
        catch (Exception ex) { lock (errors) errors.Add(ex.Message); }
    });
    Check("8 16 concurrent extractions all return a verified file",
        errors.Count == 0 && results.All(r => r != null && Hash(r) == HashBytes(a)), string.Join("; ", errors));

    // 9. no resource embedded -> null, no exception
    Check("9 missing resource returns null", EngineExtractor.Extract(() => null, Path.Combine(root, "none")) == null);
}
catch (Exception ex)
{
    Console.WriteLine("FAIL  unexpected exception: " + ex);
    failures++;
}
finally
{
    try { Directory.Delete(root, true); } catch { /* ignore */ }
}

Console.WriteLine(failures == 0 ? "ALL PASSED" : $"{failures} FAILED");
return failures == 0 ? 0 : 1;
