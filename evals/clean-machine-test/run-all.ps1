# Runs both variants one after the other and prints a short summary.
#   app-fd : default shell exe (framework-dependent: needs the .NET 10 Desktop Runtime)
#   app-sc : self-contained shell exe (bundles the runtime)
$here = $PSScriptRoot
foreach ($v in 'fd', 'sc') {
    Write-Host ("=== testing app-{0} (about 40 seconds, a window will open) ===" -f $v)
    & (Join-Path $here 'run-test.ps1') -AppDir (Join-Path $here "app-$v") -Out (Join-Path $here "results\$v")
}
Write-Host ""
foreach ($v in 'fd', 'sc') {
    Write-Host ("----- results\{0}\result.txt -----" -f $v)
    Get-Content (Join-Path $here "results\$v\result.txt")
    Write-Host ""
}
Write-Host "Done. Send back the whole 'results' folder (result.txt and screen.png of each variant)."
