param(
    [Parameter(Mandatory=$true)][ValidateSet('Export','Render')][string]$Mode,
    [Parameter(Mandatory=$true)][string]$InputPath,
    [Parameter(Mandatory=$true)][string]$OutputPath
)
$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [Text.Encoding]::UTF8
$source = (Resolve-Path -LiteralPath $InputPath).Path
$target = [IO.Path]::GetFullPath($OutputPath)
$pdfPath = [IO.Path]::ChangeExtension($target, '.pdf')
$roundtrip = [IO.Path]::ChangeExtension($target, '.roundtrip.xml')
$targets = if ($Mode -eq 'Export') { @($target) } else { @($target, $pdfPath, $roundtrip) }
if ($Mode -eq 'Render' -and [IO.Path]::GetExtension($target) -ne '.hwp') { throw 'Render output must have .hwp extension.' }
if ($targets -contains $source) { throw 'Input and output must be different files.' }
foreach ($path in $targets) {
    if (Test-Path -LiteralPath $path) { throw "Output already exists; preserve it and choose a staging path: $path" }
}
[IO.Directory]::CreateDirectory([IO.Path]::GetDirectoryName($target)) | Out-Null
$hwp = New-Object -ComObject HWPFrame.HwpObject
try {
    $hwp.XHwpWindows.Item(0).Visible = $true
    $format = if ($Mode -eq 'Export') { 'HWP' } else { 'HWPML2X' }
    if (-not $hwp.Open($source, $format, 'forceopen:true')) { throw 'Hangul could not open the input.' }
    if ($Mode -eq 'Render') {
        if (-not $hwp.SaveAs($target, 'HWP', '')) { throw 'HWP save failed.' }
        if (-not $hwp.SaveAs($pdfPath, 'PDF', '')) { throw 'PDF save failed.' }
    }
    $xml = $hwp.GetTextFile('HWPML2X', '')
    $xml = $xml.Replace('encoding="UTF-16"', 'encoding="UTF-8"')
    $xmlPath = if ($Mode -eq 'Export') { $target } else { $roundtrip }
    [IO.File]::WriteAllText($xmlPath, $xml, (New-Object Text.UTF8Encoding($true)))
    foreach ($path in $targets) {
        $file = Get-Item -LiteralPath $path
        if ($file.Length -eq 0) { throw "Empty output: $path" }
        Write-Output $file.FullName
    }
} finally {
    # This COM instance owns only this staging document. Never close a user's other windows.
    $hwp.Clear(1) | Out-Null
    $hwp.Quit()
}
