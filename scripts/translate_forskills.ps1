param(
    [int]$MaxSourceGroups = 0,
    [int]$ChunkSize = 7000,
    [switch]$Resume,
    [string]$Only = '',
    [switch]$ResumeChunks,
    [switch]$DryRun,
    [string]$InputFile = '',
    [string]$OutputName = '',
    [string]$WorkSubdir = ''
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

function ConvertFrom-JsonToHashtable {
    param($InputObject)
    if ($null -eq $InputObject) { return $null }
    if ($InputObject -is [System.Collections.IDictionary]) {
        $ht = @{}
        foreach ($key in @($InputObject.Keys)) { $ht[$key] = ConvertFrom-JsonToHashtable $InputObject[$key] }
        return $ht
    }
    if ($InputObject -is [System.Collections.IList]) {
        $arr = @()
        foreach ($item in $InputObject) { $arr += ,(ConvertFrom-JsonToHashtable $item) }
        return $arr
    }
    if ($InputObject -is [System.Management.Automation.PSCustomObject]) {
        $ht = @{}
        foreach ($prop in $InputObject.PSObject.Properties) { $ht[$prop.Name] = ConvertFrom-JsonToHashtable $prop.Value }
        return $ht
    }
    return $InputObject
}

function Get-FileHashAsHex([string]$Path) {
    $hash = (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash
    return $hash
}

function Test-ValidKoreanResponse([string]$Content) {
    if ([string]::IsNullOrWhiteSpace($Content)) { return $false }
    $trimmed = $Content.Trim()
    if ($trimmed.Length -eq 0) { return $false }
    if ($trimmed.Contains([char]0xFFFD)) { return $false }
    $hangulCodePoint = 0xAC00
    $hasHangul = $false
    foreach ($char in $trimmed.ToCharArray()) {
        if ([int]$char -ge $hangulCodePoint -and [int]$char -le 0xD7A3) {
            $hasHangul = $true
            break
        }
    }
    return $hasHangul
}

function Get-ExistingResponsePath([string]$GroupKey, [int]$OneBasedIndex, [string]$WorkDir) {
    $currentPath = Join-Path $WorkDir ("{0}-{1:D5}.response.txt" -f $GroupKey, $OneBasedIndex)
    if (Test-Path -LiteralPath $currentPath -PathType Leaf) {
        return $currentPath
    }

    if ($GroupKey -eq '374516625') {
        $zeroBasedIndex = $OneBasedIndex - 1
        $legacyPath = Join-Path $WorkDir ("{0}-{1:D5}.response.txt1" -f $GroupKey, $zeroBasedIndex)
        if (Test-Path -LiteralPath $legacyPath -PathType Leaf) {
            return $legacyPath
        }
    }

    return $null
}

function New-TranslationManifest([string]$ManifestPath, [string]$SourceDir, [string]$OutputDir) {
    $manifest = @{
        version = 1
        sources = @{}
    }

    $targetSourceIds = @('388965245', '468956986', '374516625')

    foreach ($sourceId in $targetSourceIds) {
        $sourceFiles = Get-ChildItem -File (Join-Path $SourceDir "$sourceId*") -ErrorAction SilentlyContinue
        if (-not $sourceFiles) { continue }

        $mainSource = $null
        foreach ($ext in @('.txt', '.docx', '.pdf')) {
            $candidate = $sourceFiles | Where-Object { $_.Extension -eq $ext } | Select-Object -First 1
            if ($candidate) { $mainSource = $candidate; break }
        }
        if (-not $mainSource) { continue }

        $sourceHash = Get-FileHashAsHex $mainSource.FullName
        $outputFileName = "$($mainSource.BaseName).ko.txt"
        $mode = if ($sourceId -eq '374516625') { 'selected-extract' } else { 'full' }

        $manifest.sources[$sourceId] = @{
            id = $sourceId
            source_file = $mainSource.Name
            source_sha256 = $sourceHash
            mode = $mode
            chunk_size = 7000
            output_path = "docs/forskills/ko/$outputFileName"
            chunk_status = @{}
        }
    }

    $manifestJson = ($manifest | ConvertTo-Json -Depth 4)
    [System.IO.File]::WriteAllText(
        $ManifestPath,
        $manifestJson,
        [System.Text.UTF8Encoding]::new($false)
    )

    return $manifest
}

$manifestPath = Join-Path $outputDir 'story-psychology-translation-manifest.json'

$manifest = $null
if (Test-Path $manifestPath) {
    $json = Get-Content -Raw -Encoding utf8 $manifestPath | ConvertFrom-Json
    $manifest = ConvertFrom-JsonToHashtable $json
} else {
    $manifest = New-TranslationManifest -ManifestPath $manifestPath -SourceDir $sourceDir -OutputDir $outputDir
}

$status = @{ version = 1; completed = @{}; blocked = @{}; updated_at = $null }
if (Test-Path $statusPath) {
    $json = Get-Content -Raw -Encoding utf8 $statusPath | ConvertFrom-Json
    $saved = ConvertFrom-JsonToHashtable $json
    if ($saved) { $status = $saved }
}

# Extract mode: process single input file
$extractMode = $false
if ($InputFile) {
    $extractMode = $true
    $InputFile = (Resolve-Path $InputFile -ErrorAction Stop).Path
    $inputFileObj = Get-Item -LiteralPath $InputFile -ErrorAction Stop
    $groupKey = $inputFileObj.BaseName
    $targetName = if ($OutputName) { $OutputName } else { "$($inputFileObj.BaseName).ko.txt" }
    $targetPath = Join-Path $outputDir $targetName

    # Create isolated work subdirectory for this extract
    $workSubdirName = if ($WorkSubdir) { $workSubdir } else { $groupKey }
    $workDir = Join-Path $workDir $workSubdirName
    New-Item -ItemType Directory -Force -Path $workDir | Out-Null

    # Create synthetic group object matching Group-Object structure
    $groups = @(
        @{
            Name  = $groupKey
            Group = @($inputFileObj)
        }
    )
    Write-Host "EXTRACT MODE: processing '$($inputFileObj.Name)' as group '$groupKey' with work dir: $workDir"
} else {
    # Original directory-scan mode
    $groups = Get-ChildItem -File $sourceDir |
    Where-Object { $_.DirectoryName -eq $sourceDir } |
    Group-Object -Property { Get-GroupKey $_ } |
    Sort-Object Name
}

if ($Only) {
    $filtered = $groups | Where-Object { $_.Name -like "$($Only)*" }
    if (-not $filtered) {
        throw "No source group matches -Only '$Only'."
    }
    $groups = @($filtered)
    Write-Host "ONLY groups matching '$Only': $($groups.Name -join ', ')"
}

$processed = 0
foreach ($group in $groups) {
    if (($MaxSourceGroups -gt 0) -and ($processed -ge $MaxSourceGroups)) { break }

    # In extract mode, source and target are already set
    if ($extractMode) {
        $source = $inputFileObj
        # targetName and targetPath are already set in extract mode block
    } else {
        $files = $group.Group
        $source = @($files | Where-Object Extension -eq '.txt' | Sort-Object Length -Descending | Select-Object -First 1)
        if (-not $source) { $source = @($files | Where-Object Extension -eq '.docx' | Select-Object -First 1) }
        if (-not $source) { $source = @($files | Where-Object Extension -eq '.pdf' | Select-Object -First 1) }
        if (-not $source) { continue }
        $source = $source[0]
        $targetName = "$($source.BaseName).ko.txt"
        $targetPath = Join-Path $outputDir $targetName
    }

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

    if ($DryRun) {
        Write-Host "DRY-RUN ANALYSIS: $($source.Name): $($chunks.Count) chunks"
    } else {
        Write-Host "TRANSLATE $($source.Name): $($chunks.Count) chunks"
    }

    $chunkStats = @{
        reused = 0
        missing = 0
        invalid = 0
        pending = 0
    }

    for ($index = 0; $index -lt $chunks.Count; $index++) {
        $oneBasedIndex = $index + 1
        $currentResponsePath = Join-Path $workDir ("{0}-{1:D5}.response.txt" -f $group.Name, $oneBasedIndex)
        $reuseResponse = $null

        if ($ResumeChunks) {
            $existingPath = Get-ExistingResponsePath -GroupKey $group.Name -OneBasedIndex $oneBasedIndex -WorkDir $workDir
            if ($existingPath) {
                $content = [System.IO.File]::ReadAllText($existingPath, [System.Text.UTF8Encoding]::new($false))
                if (Test-ValidKoreanResponse -Content $content) {
                    $reuseResponse = $content
                    $chunkStats.reused++
                    Write-Host "  chunk $oneBasedIndex/$($chunks.Count) [REUSED]"
                } else {
                    $chunkStats.invalid++
                    Write-Host "  chunk $oneBasedIndex/$($chunks.Count) [INVALID - will re-translate]"
                }
            } else {
                $chunkStats.missing++
                Write-Host "  chunk $oneBasedIndex/$($chunks.Count) [MISSING]"
            }
        } else {
            $chunkStats.pending++
        }

        if ($DryRun) { continue }

        $translation = $null
        if ($reuseResponse) {
            $translation = $reuseResponse
        } else {
            Remove-Item -LiteralPath $currentResponsePath -Force -ErrorAction SilentlyContinue
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

            Write-Host "  chunk $oneBasedIndex/$($chunks.Count)"
            $promptFile = Join-Path $workDir ("{0}-{1:D5}.prompt.txt" -f $group.Name, $oneBasedIndex)
            [System.IO.File]::WriteAllText($promptFile, $prompt, [System.Text.UTF8Encoding]::new($false))
            $cmdLine = 'codex exec --ephemeral --ignore-rules --color never -s read-only -m gpt-5.6-terra -o "{0}" < "{1}"' -f $currentResponsePath, $promptFile
            cmd.exe /c $cmdLine
            if ($LASTEXITCODE -ne 0 -or -not (Test-Path $currentResponsePath)) {
                throw "Codex translation failed for $($source.Name), chunk $oneBasedIndex."
            }
            $translation = [System.IO.File]::ReadAllText($currentResponsePath).Trim()
            if ([string]::IsNullOrWhiteSpace($translation)) {
                throw "Codex returned empty output for $($source.Name), chunk $oneBasedIndex."
            }
        }

        if ($index -eq 0) {
            [System.IO.File]::WriteAllText($tempTarget, $translation + "`r`n", [System.Text.UTF8Encoding]::new($false))
        } else {
            [System.IO.File]::AppendAllText($tempTarget, "`r`n`r`n" + $translation + "`r`n", [System.Text.UTF8Encoding]::new($false))
        }
    }

    if ($DryRun) {
        Write-Host "DRY-RUN REPORT for $($source.Name):"
        Write-Host "  Reused: $($chunkStats.reused)"
        Write-Host "  Missing: $($chunkStats.missing)"
        Write-Host "  Invalid: $($chunkStats.invalid)"
        Write-Host "  Pending: $($chunkStats.pending)"
        continue
    }

    Move-Item -LiteralPath $tempTarget -Destination $targetPath -Force

    if ($manifest.sources -and $manifest.sources.ContainsKey($group.Name)) {
        $chunkStatusArray = @()
        for ($i = 0; $i -lt $chunks.Count; $i++) {
            $oneBased = $i + 1
            $responsePath = Get-ExistingResponsePath -GroupKey $group.Name -OneBasedIndex $oneBased -WorkDir $workDir
            if ($responsePath) {
                $content = [System.IO.File]::ReadAllText($responsePath)
                if (Test-ValidKoreanResponse -Content $content) {
                    $chunkStatusArray += 'reused'
                } else {
                    $chunkStatusArray += 'invalid'
                }
            } else {
                $chunkStatusArray += 'missing'
            }
        }
        $manifest.sources[$group.Name].chunk_status = $chunkStatusArray

        $manifestJson = ($manifest | ConvertTo-Json -Depth 4)
        [System.IO.File]::WriteAllText(
            $manifestPath,
            $manifestJson,
            [System.Text.UTF8Encoding]::new($false)
        )
    }

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
