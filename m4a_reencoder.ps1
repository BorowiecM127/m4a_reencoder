$initFilenames = @()
$initFilenames += (Get-ChildItem .\* -Include *.m4a).Name

$tempFilenames = @()
$tempFilenames += $initFilenames | ForEach-Object {$_.Replace(".m4a", "_temp.m4a")}

$filenames = @()

for ($i = 0; $i -lt $initFilenames.Count; $i++) {
    $filenames += [System.Tuple]::Create($initFilenames[$i], $tempFilenames[$i])
}

(Get-ChildItem .\* -Include *.m4a) | Rename-Item -NewName {$_.BaseName + "_temp" + $_.Extension}

$ffmpegArguments = @()

$filenames | ForEach-Object {
    $ffmpegArguments = '-i "{0}" -codec: copy "{1}"' -f $_.Item2, $_.Item1
    Start-Process -FilePath ./ffmpeg.exe -ArgumentList $ffmpegArguments -Wait -NoNewWindow;
}

$tempFilenames | ForEach-Object { Remove-Item $_ }