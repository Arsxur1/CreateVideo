# Simple verification of extraction quality
# PowerShell 5.1 compatible

$extractFile = "C:\ysj\OpenMontage\docs\forskills\story-source-selections\374516625-social-psychology-story-sections.txt"
$extractLines = Get-Content -Path $extractFile -Encoding UTF8

Write-Host "=== EXTRACTION VERIFICATION SUMMARY ===" -ForegroundColor Cyan
Write-Host ""

# Check 1: Verify all 16 chapter markers are present
Write-Host "1. Checking all 16 chapter markers are present..." -ForegroundColor Yellow
$chapterMarkers = @()
for ($i = 0; $i -lt $extractLines.Count; $i++) {
    if ($extractLines[$i] -match "^CHAPTER (\d+)") {
        $chapterMarkers += [int]$matches[1]
    }
}

$expectedChapters = @(8, 9, 12, 13, 14, 15, 16, 18, 23, 24, 25, 26, 27, 31, 36, 37)
$missingChapters = $expectedChapters | Where-Object { $_ -notin $chapterMarkers }
$extraChapters = $chapterMarkers | Where-Object { $_ -notin $expectedChapters }

if ($missingChapters.Count -eq 0 -and $extraChapters.Count -eq 0) {
    Write-Host "  PASS: All 16 expected chapters present" -ForegroundColor Green
} else {
    if ($missingChapters.Count -gt 0) {
        Write-Host "  FAIL: Missing chapters: $($missingChapters -join ', ')" -ForegroundColor Red
    }
    if ($extraChapters.Count -gt 0) {
        Write-Host "  FAIL: Extra chapters: $($extraChapters -join ', ')" -ForegroundColor Red
    }
}
Write-Host ""

# Check 2: Verify no TOC signature lines
Write-Host "2. Checking for TOC signature leaks..." -ForegroundColor Yellow
$tocLeakCount = 0
$separatorChar = [char]0x23D0
for ($i = 0; $i -lt $extractLines.Count; $i++) {
    $line = $extractLines[$i]
    $hasSeparator = $line.IndexOf($separatorChar) -ge 0
    $hasTrailingPageNumber = $line -match '\d{2,4}\s*$'
    if ($hasSeparator -and $hasTrailingPageNumber) {
        $tocLeakCount++
    }
}

if ($tocLeakCount -eq 0) {
    Write-Host "  PASS: No TOC signature lines found" -ForegroundColor Green
} else {
    Write-Host "  FAIL: Found $tocLeakCount TOC signature lines" -ForegroundColor Red
}
Write-Host ""

# Check 3: Calculate total size
Write-Host "3. Total extraction statistics..." -ForegroundColor Yellow
$totalChars = ($extractLines -join "`n").Length
Write-Host "  Total characters: $totalChars" -ForegroundColor Green
Write-Host "  Total lines: $($extractLines.Count)" -ForegroundColor Green
Write-Host ""

# Final result
Write-Host "=== FINAL RESULT ===" -ForegroundColor Cyan
$allPassed = ($missingChapters.Count -eq 0 -and $extraChapters.Count -eq 0 -and $tocLeakCount -eq 0)
if ($allPassed) {
    Write-Host "VERIFICATION PASSED" -ForegroundColor Green
} else {
    Write-Host "VERIFICATION FAILED" -ForegroundColor Red
}
Write-Host ""

# Return exit code
exit $(if ($allPassed) { 0 } else { 1 })
