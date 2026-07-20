param(
    [int]$MaxSourceGroups = 0,
    [int]$ChunkSize = 7000,
    [switch]$Resume
)

$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'

$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$sourceDir = Join-Path $root 'docs\forskills'
$outputDir = Join-Path $sourceDir 'ko'
$workDir = Join-Path $root 'tmp\forskills-translation'
$statusPath = Join-Path $outputDir 'translation-status.json'
$python = 'C:\Users\dbtmd\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'

New-Item -ItemType Directory -Force -Path $outputDir, $workDir | Out-Null
$env:PYTHONIOENCODING = 'utf-8'

function Get-GroupKey([System.IO.FileInfo]$File) {
    if ($File.BaseName -match '^(\d+)') { return $Matches[1] }
    return $File.BaseName
}

function Get-DocumentText([System.IO.FileInfo]$File) {
    if ($File.Extension -eq '.txt') {
        return [System.IO.File]::ReadAllText($File.FullName)
    }

    $extractor = @'
import sys
from pathlib import Path

path = Path(sys.argv[1])
if path.suffix.lower() == ".docx":
    from docx import Document
    document = Document(path)
    blocks = [p.text for p in document.paragraphs]
    for table in document.tables:
        for row in table.rows:
            blocks.append("\t".join(cell.text for cell in row.cells))
    print("\n\n".join(blocks))
elif path.suffix.lower() == ".pdf":
    from pypdf import PdfReader
    reader = PdfReader(path)
    print("\n\n".join((page.extract_text() or "") for page in reader.pages))
else:
    raise SystemExit(f"Unsupported source type: {path.suffix}")
'@
    return ((& $python -c $extractor $File.FullName) -join "`n")
}

function Split-ForTranslation([string]$Text, [int]$Limit) {
    $text = $Text -replace "`r`n", "`n"
    $paragraphs = [regex]::Split($text, "\n{2,}")
    $chunks = [System.Collections.Generic.List[string]]::new()
    $current = [System.Text.StringBuilder]::new()

    function Add-Chunk([string]$Value) {
        if (-not [string]::IsNullOrWhiteSpace($Value)) {
            $chunks.Add($Value.Trim())
        }
    }

    foreach ($paragraph in $paragraphs) {
        $part = $paragraph.Trim()
        if (-not $part) { continue }

        if ($part.Length -gt $Limit) {
            Add-Chunk $current.ToString()
            $current.Clear() | Out-Null
            $offset = 0
            while ($offset -lt $part.Length) {
                $length = [Math]::Min($Limit, $part.Length - $offset)
                if ($offset + $length -lt $part.Length) {
                    $breakAt = $part.LastIndexOfAny([char[]]" .?!;:`n", $offset + $length - 1, $length)
                    if ($breakAt -gt $offset + [Math]::Floor($Limit * 0.55)) {
                        $length = $breakAt - $offset + 1
                    }
                }
                Add-Chunk $part.Substring($offset, $length)
                $offset += $length
            }
            continue
        }

        if (($current.Length -gt 0) -and ($current.Length + 2 + $part.Length -gt $Limit)) {
            Add-Chunk $current.ToString()
            $current.Clear() | Out-Null
        }
        if ($current.Length -gt 0) { $null = $current.Append("`n`n") }
        $null = $current.Append($part)
    }
    Add-Chunk $current.ToString()
    return $chunks
}

function Save-Status([hashtable]$Status) {
    $Status.updated_at = (Get-Date).ToUniversalTime().ToString('o')
    [System.IO.File]::WriteAllText(
        $statusPath,
        ($Status | ConvertTo-Json -Depth 8),
        [System.Text.UTF8Encoding]::new($false)
    )
}

$status = @{ version = 1; completed = @{}; blocked = @{}; updated_at = $null }
if (Test-Path $statusPath) {
    $saved = Get-Content -Raw -Encoding utf8 $statusPath | ConvertFrom-Json -AsHashtable
    if ($saved) { $status = $saved }
}

$groups = Get-ChildItem -File $sourceDir |
    Where-Object { $_.DirectoryName -eq $sourceDir } |
    Group-Object -Property { Get-GroupKey $_ } |
    Sort-Object Name

$processed = 0
foreach ($group in $groups) {
    if (($MaxSourceGroups -gt 0) -and ($processed -ge $MaxSourceGroups)) { break }
    $files = $group.Group
    $source = @($files | Where-Object Extension -eq '.txt' | Sort-Object Length -Descending | Select-Object -First 1)
    if (-not $source) { $source = @($files | Where-Object Extension -eq '.docx' | Select-Object -First 1) }
    if (-not $source) { $source = @($files | Where-Object Extension -eq '.pdf' | Select-Object -First 1) }
    if (-not $source) { continue }
    $source = $source[0]
    $targetName = "$($source.BaseName).ko.txt"
    $targetPath = Join-Path $outputDir $targetName

    if ((Test-Path $targetPath) -and -not $Resume) {
        Write-Host "SKIP complete output: $targetName"
        $status.completed[$group.Name] = @{ source = $source.Name; output = $targetName; existing = $true }
        Save-Status $status
        continue
    }

    Write-Host "EXTRACT $($source.Name)"
    $text = Get-DocumentText $source
    if ([string]::IsNullOrWhiteSpace($text) -or $text.Length -lt 200) {
        $status.blocked[$group.Name] = @{ source = $source.Name; reason = 'No usable extractable text; OCR or visual page review is required.' }
        Save-Status $status
        Write-Warning "BLOCKED (no usable text): $($source.Name)"
        continue
    }

    $chunks = Split-ForTranslation $text $ChunkSize
    if ($chunks.Count -eq 0) {
        $status.blocked[$group.Name] = @{ source = $source.Name; reason = 'No translatable chunks after extraction.' }
        Save-Status $status
        continue
    }

    $tempTarget = "$targetPath.partial"
    if (Test-Path $tempTarget) { Remove-Item -LiteralPath $tempTarget -Force }
    Write-Host "TRANSLATE $($source.Name): $($chunks.Count) chunks"

    for ($index = 0; $index -lt $chunks.Count; $index++) {
        $responsePath = Join-Path $workDir ("{0}-{1:D5}.response.txt" -f $group.Name, $index + 1)
        Remove-Item -LiteralPath $responsePath -Force -ErrorAction SilentlyContinue
        $prompt = @"
Translate the source text below from its original language into natural Korean.

Strict requirements:
- Translate every line and every paragraph completely. Do not summarize, omit, explain, or add commentary.
- Preserve headings, lists, quotations, references, page markers, and paragraph breaks where possible.
- Keep proper names, book and film titles, formulas, identifiers, and technical terms in English when a Korean rendering would reduce clarity.
- Output only the Korean translation, with no preface, Markdown fence, or note.

SOURCE TEXT START
$($chunks[$index])
SOURCE TEXT END
"@

        Write-Host "  chunk $($index + 1)/$($chunks.Count)"
        & codex -a never --color never exec --ephemeral --ignore-rules -s read-only -o $responsePath $prompt
        if ($LASTEXITCODE -ne 0 -or -not (Test-Path $responsePath)) {
            throw "Codex translation failed for $($source.Name), chunk $($index + 1)."
        }
        $translation = [System.IO.File]::ReadAllText($responsePath).Trim()
        if ([string]::IsNullOrWhiteSpace($translation)) {
            throw "Codex returned empty output for $($source.Name), chunk $($index + 1)."
        }
        if ($index -eq 0) {
            [System.IO.File]::WriteAllText($tempTarget, $translation + "`r`n", [System.Text.UTF8Encoding]::new($false))
        } else {
            [System.IO.File]::AppendAllText($tempTarget, "`r`n`r`n" + $translation + "`r`n", [System.Text.UTF8Encoding]::new($false))
        }
    }

    Move-Item -LiteralPath $tempTarget -Destination $targetPath -Force
    $status.completed[$group.Name] = @{
        source = $source.Name
        output = $targetName
        source_characters = $text.Length
        chunks = $chunks.Count
        completed_at = (Get-Date).ToUniversalTime().ToString('o')
    }
    $status.blocked.Remove($group.Name)
    Save-Status $status
    $processed++
    Write-Host "DONE $targetName"
}

Save-Status $status
