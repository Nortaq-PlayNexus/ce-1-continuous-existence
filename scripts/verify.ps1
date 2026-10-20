# verify.ps1 - run every CE-1 check in one command.
#
#   powershell -NoProfile -File scripts\verify.ps1
#
# Exits non-zero if any check fails. Deterministic: no network, no LLM calls,
# no model downloads. Runs in well under a second on a warm checkout.

$ErrorActionPreference = 'Continue'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

$failed = @()

function Invoke-Check {
    param(
        [string]$Name,
        [string]$Exe,
        [string[]]$ArgList
    )
    Write-Host ""
    Write-Host "=== $Name ===" -ForegroundColor Cyan
    # NOTE: the parameter must NOT be named $Args. PowerShell's $Args is an
    # automatic variable; binding to it silently misroutes arguments, which
    # previously caused the interpreter to be invoked with no arguments at all
    # and fall into the interactive REPL.
    & $Exe @ArgList
    $code = $LASTEXITCODE
    if ($code -eq 0) {
        Write-Host "[ok] $Name (exit 0)" -ForegroundColor Green
    } else {
        Write-Host "[FAIL] $Name (exit $code)" -ForegroundColor Red
        $script:failed += $Name
    }
}

Write-Host "CE-1 verification suite" -ForegroundColor White
Write-Host "root: $root"

# Pick the project-local venv if present, else fall back to system python.
$py = if (Test-Path ".venv\Scripts\python.exe") { ".venv\Scripts\python.exe" } else { "python" }
Write-Host "python: $py"

Invoke-Check "source manifest schema" $py @("scripts\validate_sources.py")
Invoke-Check "research artifacts"     $py @("scripts\validate_research_artifacts.py")
Invoke-Check "unit tests"             $py @("-m", "pytest", "tests", "-q")
Invoke-Check "mutation harness"       $py @("scripts\mutation_check.py")
Invoke-Check "experiment manifest"    $py @("scripts\make_research_manifest.py")
Invoke-Check "H8 adversarial audit"   $py @("experiments\continuity_v1\adversarial_verify_h8.py")

Write-Host ""
Write-Host ("=" * 60)
if ($failed.Count -eq 0) {
    Write-Host "ALL CHECKS PASSED" -ForegroundColor Green
    exit 0
} else {
    Write-Host "FAILED: $($failed -join ', ')" -ForegroundColor Red
    exit 1
}