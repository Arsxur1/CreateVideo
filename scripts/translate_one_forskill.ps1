param(
    [Parameter(Mandatory = $true)]
    [string]$SourcePath,
    [Parameter(Mandatory = $true)]
    [string]$TargetPath
)

$ErrorActionPreference = 'Stop'
$env:PYTHONIOENCODING = 'utf-8'
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)

$workspacePython = 'C:\Users\dbtmd\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
$extension = [System.IO.Path]::GetExtension($SourcePath).ToLowerInvariant()

if ($extension -eq '.txt') {
    $sourceText = [System.IO.File]::ReadAllText((Resolve-Path $SourcePath))
} elseif ($extension -eq '.docx') {
    $extractor = @'
from docx import Document
from pathlib import Path
import sys
document = Document(Path(sys.argv[1]))
print("\n\n".join(paragraph.text for paragraph in document.paragraphs))
'@
    $sourceText = ((& $workspacePython -c $extractor (Resolve-Path $SourcePath)) -join "`n")
} elseif ($extension -eq '.pdf') {
    $extractor = @'
from pathlib import Path
from pypdf import PdfReader
import sys
reader = PdfReader(Path(sys.argv[1]))
print("\n\n".join((page.extract_text() or "") for page in reader.pages))
'@
    $sourceText = ((& $workspacePython -c $extractor (Resolve-Path $SourcePath)) -join "`n")
} else {
    throw "Unsupported source type: $extension"
}

if ([string]::IsNullOrWhiteSpace($sourceText)) {
    throw 'No usable source text was extracted.'
}

$prompt = @"
Translate the following source text fully into Korean. Preserve headings, paragraphs, lists, quotations, references, and the original order. Do not summarize, omit, explain, or add commentary. Output only the Korean translation.

SOURCE TEXT START
$sourceText
SOURCE TEXT END
"@

$target = (Resolve-Path (Split-Path -Parent $TargetPath)).Path + '\' + (Split-Path -Leaf $TargetPath)
$temporary = "$target.partial"
Remove-Item -LiteralPath $temporary -Force -ErrorAction SilentlyContinue

$prompt | & 'C:\nvm4w\nodejs\codex.cmd' -a never --color never exec --ephemeral --ignore-rules -s read-only -o $temporary -
if ($LASTEXITCODE -ne 0) {
    throw "Codex failed with exit code $LASTEXITCODE."
}
if (-not (Test-Path $temporary) -or (Get-Item $temporary).Length -lt 100) {
    throw 'Codex returned no usable translation.'
}
Move-Item -LiteralPath $temporary -Destination $target -Force
Write-Output "WROTE $target"
