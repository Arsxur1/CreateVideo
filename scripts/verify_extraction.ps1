# Verification script for extracted chapters
# PowerShell 5.1 compatible

$ErrorActionPreference = "Stop"

# File paths
$sourceFile = "C:\ysj\OpenMontage\docs\forskills\374516625-Handbook-of-Social-Psychology.txt"
$extractFile = "C:\ysj\OpenMontage\docs\forskills\story-source-selections\374516625-social-psychology-story-sections.txt"

# Expected chapters with their titles
$expectedChapters = @{
    "Motivation" = 8
    "Emotion" = 9
    "Perceiving People" = 12
    "Nonverbal Behavior" = 13
    "Mind Perception" = 14
    "Judgment and Decision Making" = 15
    "Self and Identity" = 16
    "Personality in Social Psychology" = 18
    "Aggression" = 23
    "Affiliation, Acceptance, and Belonging" = 24
    "Close Relationships" = 25
    "Status, Power, and Subordination" = 26
    "Social Conflict" = 27
    "Influence and Leadership" = 31
    "Language and Conversations" = 36
    "Cultural Psychology" = 37
}

# Source line ranges for each chapter
$chapterRanges = @{
    8 = @(16206, 19287)
    9 = @(19288, 21505)
    12 = @(26134, 28289)
    13 = @(28290, 30318)
    14 = @(30319, 33203)
    15 = @(33204, 36083)
    16 = @(36084, 38643)
    18 = @(40903, 42643)
    23 = @(50974, 53033)
    24 = @(53034, 55088)
    25 = @(55089, 57714)
    26 = @(57715, 60474)
    27 = @(60475, 63118)
    31 = @(71677, 74216)
    36 = @(85047, 87195)
    37 = @(87196, 97389)
}

Write-Host "=== VERIFICATION REPORT ===" -ForegroundColor Cyan
Write-Host ""

# Read files
$sourceLines = Get-Content -Path $sourceFile -Encoding UTF8
$extractLines = Get-Content -Path $extractFile -Encoding UTF8

Write-Host "Source file: $($sourceLines.Count) lines"
Write-Host "Extract file: $($extractLines.Count) lines"
Write-Host ""

# Verification 1: Check chapter headings occur exactly once
Write-Host "1. Checking chapter headings occur exactly once..." -ForegroundColor Yellow
$headingErrors = 0
foreach ($title in $expectedChapters.Keys) {
    $count = 0
    for ($i = 0; $i -lt $extractLines.Count; $i++) {
        if ($extractLines[$i] -match "^$title$") {
            $count++
        }
    }
    if ($count -eq 1) {
        Write-Host "  OK '$title' appears exactly once" -ForegroundColor Green
    } else {
        Write-Host "  FAIL '$title' appears $count times (expected 1)" -ForegroundColor Red
        $headingErrors++
    }
}
Write-Host "  Result: $(if ($headingErrors -eq 0) { 'PASS' } else { 'FAIL' })" -ForegroundColor $(if ($headingErrors -eq 0) { 'Green' } else { 'Red' })
Write-Host ""

# Verification 2: Check first/last 200 characters match for each chapter
Write-Host "2. Checking first/last 200 characters match original..." -ForegroundColor Yellow
$charErrors = 0
foreach ($chapterNum in $chapterRanges.Keys) {
    $range = $chapterRanges[$chapterNum]
    $startLine = $range[0]
    $endLine = $range[1]

    # Get the original content (skip TOC lines)
    $originalLines = $sourceLines[($startLine - 1)..($endLine - 1)]
    $originalContent = $originalLines -join "`n"

    # Get the first 200 and last 200 chars from original
    $first200Original = $originalContent.Substring(0, [Math]::Min(200, $originalContent.Length))
    $last200Original = $originalContent.Substring([Math]::Max(0, $originalContent.Length - 200))

    # Find corresponding content in extract (after the chapter marker)
    $extractContent = $extractLines -join "`n"
    $chapterMarker = "CHAPTER $chapterNum"
    $markerPos = $extractContent.IndexOf($chapterMarker)
    if ($markerPos -ge 0) {
        # Get content after the marker (skip the header section)
        $afterMarker = $extractContent.Substring($markerPos + $chapterMarker.Length)
        # Find the actual chapter content (skip to next blank line after the header)
        $contentStartPos = $afterMarker.IndexOf("          Chapter") # find the actual chapter line
        if ($contentStartPos -ge 0) {
            $actualContent = $afterMarker.Substring($contentStartPos)
            # Get content up to next chapter marker or end
            $nextChapterPos = $actualContent.IndexOf("====================================================================
CHAPTER")
            if ($nextChapterPos -gt 0) {
                $actualContent = $actualContent.Substring(0, $nextChapterPos)
            }

            $first200Extract = $actualContent.Substring(0, [Math]::Min(200, $actualContent.Length))
            $last200Extract = $actualContent.Substring([Math]::Max(0, $actualContent.Length - 200))

            if ($first200Original -eq $first200Extract) {
                Write-Host "  OK Chapter $chapterNum first 200 chars match" -ForegroundColor Green
            } else {
                Write-Host "  FAIL Chapter $chapterNum first 200 chars DON'T match" -ForegroundColor Red
                $charErrors++
            }

            if ($last200Original -eq $last200Extract) {
                Write-Host "  OK Chapter $chapterNum last 200 chars match" -ForegroundColor Green
            } else {
                Write-Host "  FAIL Chapter $chapterNum last 200 chars DON'T match" -ForegroundColor Red
                $charErrors++
            }
        } else {
            Write-Host "  FAIL Chapter $chapterNum content start not found in extract" -ForegroundColor Red
            $charErrors += 2
        }
    } else {
        Write-Host "  FAIL Chapter $chapterNum marker not found in extract" -ForegroundColor Red
        $charErrors += 2
    }
}
Write-Host "  Result: $(if ($charErrors -eq 0) { 'PASS' } else { 'FAIL' })" -ForegroundColor $(if ($charErrors -eq 0) { 'Green' } else { 'Red' })
Write-Host ""

# Verification 3: Check for TOC leaks (lines with ⏐ separator and trailing page number)
Write-Host "3. Checking for TOC signature lines..." -ForegroundColor Yellow
$tocLeakCount = 0
$separatorChar = [char]0x23D0
for ($i = 0; $i -lt $extractLines.Count; $i++) {
    $line = $extractLines[$i]
    $hasSeparator = $line.IndexOf($separatorChar) -ge 0
    $hasTrailingPageNumber = $line -match '\d{2,4}\s*$'
    if ($hasSeparator -and $hasTrailingPageNumber) {
        $tocLeakCount++
        if ($tocLeakCount -le 5) {
            Write-Host "  FAIL TOC leak at line $($i+1): $line" -ForegroundColor Red
        }
    }
}
if ($tocLeakCount -eq 0) {
    Write-Host "  OK No TOC signature lines found in extract" -ForegroundColor Green
} else {
    Write-Host "  FAIL Found $tocLeakCount TOC signature lines in extract" -ForegroundColor Red
}
Write-Host "  Result: $(if ($tocLeakCount -eq 0) { 'PASS' } else { 'FAIL' })" -ForegroundColor $(if ($tocLeakCount -eq 0) { 'Green' } else { 'Red' })
Write-Host ""

# Verification 4: Check chapter sizes
Write-Host "4. Analyzing chapter sizes..." -ForegroundColor Yellow
$extractContent = $extractLines -join "`n"
$totalSize = 0
foreach ($chapterNum in $chapterRanges.Keys) {
    $chapterMarker = "CHAPTER $chapterNum"
    $markerPos = $extractContent.IndexOf($chapterMarker)
    if ($markerPos -ge 0) {
        # Find next chapter marker or end
        $searchStart = $markerPos + $chapterMarker.Length
        $nextChapterPos = $extractContent.IndexOf("====================================================================
CHAPTER", $searchStart)
        if ($nextChapterPos -gt 0) {
            $chapterContent = $extractContent.Substring($searchStart, $nextChapterPos - $searchStart)
        } else {
            $chapterContent = $extractContent.Substring($searchStart)
        }
        $size = $chapterContent.Length
        $totalSize += $size
        $status = if ($size -gt 1000) { "OK" } else { "TOO SMALL" }
        Write-Host "  $status Chapter ${chapterNum}: $size characters" -ForegroundColor $(if ($size -gt 1000) { 'Green' } else { 'Red' })
    }
}
Write-Host "  Total extracted content size: $totalSize characters"
Write-Host ""

# Final summary
Write-Host "=== SUMMARY ===" -ForegroundColor Cyan
$totalTests = 3
$passedTests = 0
if ($headingErrors -eq 0) { $passedTests++ }
if ($charErrors -eq 0) { $passedTests++ }
if ($tocLeakCount -eq 0) { $passedTests++ }

Write-Host "Tests Passed: $passedTests/$totalTests" -ForegroundColor $(if ($passedTests -eq $totalTests) { 'Green' } else { 'Red' })
Write-Host "Overall Result: $(if ($passedTests -eq $totalTests) { 'VERIFICATION PASSED' } else { 'VERIFICATION FAILED' })" -ForegroundColor $(if ($passedTests -eq $totalTests) { 'Green' } else { 'Red' })
Write-Host ""

# Return exit code
exit $(if ($passedTests -eq $totalTests) { 0 } else { 1 })
