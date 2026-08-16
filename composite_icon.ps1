Add-Type -AssemblyName System.Drawing

$bgColor = [System.Drawing.Color]::FromArgb(255, 0x25, 0x39, 0x43)
$fg = [System.Drawing.Image]::FromFile("C:\Users\yutti\Media Toolbox\app\src\main\res\mipmap-xxxhdpi\ic_launcher_foreground.png")

$size = 512
$bmp = New-Object System.Drawing.Bitmap($size, $size)
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
$g.Clear($bgColor)
$g.DrawImage($fg, 0, 0, $size, $size)
$g.Dispose()

$bmp.Save("C:\Users\yutti\sato-yuichi-homepage\assets\img\mediatoolbox-icon.png", [System.Drawing.Imaging.ImageFormat]::Png)
$bmp.Dispose()
$fg.Dispose()
Write-Output "done"
