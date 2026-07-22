# Extract Story Psychology Sections from Handbook of Social Psychology
# Extracts 16 specific chapters for later Korean translation
# PowerShell 5.1 compatible

$ErrorActionPreference = "Stop"

# File paths
$sourceFile = "C:\ysj\OpenMontage\docs\forskills\374516625-Handbook-of-Social-Psychology.txt"
$outputDir = "C:\ysj\OpenMontage\docs\forskills\story-source-selections"
$outputFile = Join-Path $outputDir "374516625-social-psychology-story-sections.txt"

# Ensure output directory exists
if (-not (Test-Path $outputDir)) {
    New-Item -ItemType Directory -Path $outputDir -Force | Out-Null
}

# Chapters to extract: (ChapterNumber, StartLine, EndLine, Title)
$chapters = @(
    @(8, 16206, 19287, "Motivation"),
    @(9, 19288, 21505, "Emotion"),
    @(12, 26134, 28289, "Perceiving People"),
    @(13, 28290, 30318, "Nonverbal Behavior"),
    @(14, 30319, 33203, "Mind Perception"),
    @(15, 33204, 36083, "Judgment and Decision Making"),
    @(16, 36084, 38643, "Self and Identity"),
    @(18, 40903, 42643, "Personality in Social Psychology"),
    @(23, 50974, 53033, "Aggression"),
    @(24, 53034, 55088, "Affiliation, Acceptance, and Belonging"),
    @(25, 55089, 57714, "Close Relationships"),
    @(26, 57715, 60474, "Status, Power, and Subordination"),
    @(27, 60475, 63118, "Social Conflict"),
    @(31, 71677, 74216, "Influence and Leadership"),
    @(36, 85047, 87195, "Language and Conversations"),
    @(37, 87196, 97389, "Cultural Psychology")
)

# Calculate source file hash for provenance
Write-Host "Calculating source file hash..."
$fileHash = Get-FileHash -Path $sourceFile -Algorithm SHA256
$hashString = $fileHash.Hash.ToString()

# Get extraction date
$extractionDate = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

Write-Host "Reading source file..."
$lines = Get-Content -Path $sourceFile -Encoding UTF8

Write-Host "Extracting $($chapters.Count) chapters..."

# Build output content
$outputContent = New-Object System.Text.StringBuilder

# Add provenance header
$outputContent.AppendLine("====================================================================") | Out-Null
$outputContent.AppendLine("SOCIAL PSYCHOLOGY STORY SECTIONS - EXTRACTED CHAPTERS") | Out-Null
$outputContent.AppendLine("====================================================================") | Out-Null
$outputContent.AppendLine("Source File: $sourceFile") | Out-Null
$outputContent.AppendLine("Source SHA-256: $hashString") | Out-Null
$outputContent.AppendLine("Extraction Date: $extractionDate") | Out-Null
$outputContent.AppendLine("Selected Chapters:") | Out-Null
foreach ($chapter in $chapters) {
    $chapterNum = $chapter[0]
    $startLine = $chapter[1]
    $endLine = $chapter[2]
    $title = $chapter[3]
    $outputContent.AppendLine("  Chapter $chapterNum ($title): Lines $startLine-$endLine") | Out-Null
}
$outputContent.AppendLine("====================================================================") | Out-Null
$outputContent.AppendLine("") | Out-Null

# Extract each chapter
foreach ($chapter in $chapters) {
    $chapterNum = $chapter[0]
    $startLine = $chapter[1]
    $endLine = $chapter[2]
    $title = $chapter[3]

    Write-Host "  Extracting Chapter ${chapterNum}: ${title} (lines ${startLine} to ${endLine})"

    # Add chapter separator
    $outputContent.AppendLine("") | Out-Null
    $outputContent.AppendLine("====================================================================") | Out-Null
    $outputContent.AppendLine("CHAPTER $chapterNum - $title") | Out-Null
    $outputContent.AppendLine("====================================================================") | Out-Null
    $outputContent.AppendLine("") | Out-Null

    # Extract chapter content (0-indexed array, so subtract 1 from line numbers)
    $chapterLines = $lines[($startLine - 1)..($endLine - 1)]

    # Filter out TOC signature lines (containing ⏐ separator with trailing page number)
    $filteredLines = @()
    foreach ($line in $chapterLines) {
        # Skip lines that look like TOC entries: contain special separator and trailing page number pattern
        # Use character code check for the separator (U+23D0)
        $hasSeparator = $line.IndexOf([char]0x23D0) -ge 0
        $hasTrailingPageNumber = $line -match '\d{2,4}\s*$'
        if ($hasSeparator -and $hasTrailingPageNumber) {
            # This looks like a TOC line, skip it
            continue
        }
        $filteredLines += $line
    }

    # Add filtered chapter content
    foreach ($line in $filteredLines) {
        $outputContent.AppendLine($line) | Out-Null
    }
}

Write-Host "Writing output file..."

# Write output file as UTF-8 without BOM
$utf8NoBom = New-Object System.Text.UTF8Encoding $false
[System.IO.File]::WriteAllText($outputFile, $outputContent.ToString(), $utf8NoBom)

Write-Host "Extraction complete!"
Write-Host "Output written to: $outputFile"

# Calculate statistics
$totalChars = $outputContent.ToString().Length
Write-Host "Total characters extracted: $totalChars"
