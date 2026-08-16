Add-Type -AssemblyName System.Drawing

$dir = "C:\Users\yutti\sato-yuichi-homepage\assets\img"
$W = 1200; $H = 630

$bmp = New-Object System.Drawing.Bitmap($W, $H)
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
$g.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit

# background
$g.Clear([System.Drawing.Color]::FromArgb(255,0xfa,0xfa,0xf8))

# soft accent blobs (brand colors)
$accentBlob = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(55, 0x2f,0x6f,0x4e))
$g.FillEllipse($accentBlob, -180, -200, 560, 560)
$amazonBlob = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(45, 0xc4,0x7a,0x1f))
$g.FillEllipse($amazonBlob, 980, 400, 420, 420)

# text colors
$textBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(255,0x23,0x24,0x1f))
$accentBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(255,0x23,0x4f,0x38))
$mutedBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(255,0x6b,0x6b,0x62))

$fam = "Yu Gothic"
$subFont = New-Object System.Drawing.Font($fam, 22, [System.Drawing.FontStyle]::Bold)
$titleFont = New-Object System.Drawing.Font($fam, 64, [System.Drawing.FontStyle]::Bold)
$leadFont = New-Object System.Drawing.Font($fam, 21, [System.Drawing.FontStyle]::Regular)

$g.DrawString("実業家 ・ アプリ開発者 ・ ビジネスコンサルタント", $subFont, $accentBrush, 70, 96)
$g.DrawString("佐藤雄一", $titleFont, $textBrush, 66, 132)
$g.DrawString("日常の不便を解消するアプリと、", $leadFont, $mutedBrush, 70, 262)
$g.DrawString("実用書（Kindle）を発信しています。", $leadFont, $mutedBrush, 70, 296)

# accent bar
$barBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(255,0x2f,0x6f,0x4e))
$g.FillRectangle($barBrush, 70, 60, 6, 30)

function Draw-ShadowRect($g, $x, $y, $w, $h, $angle) {
  $state = $g.Save()
  $cx = $x + $w/2; $cy = $y + $h/2
  $g.TranslateTransform($cx, $cy)
  $g.RotateTransform($angle)
  $shadowBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(60,0,0,0))
  $g.FillRectangle($shadowBrush, -$w/2 + 6, -$h/2 + 10, $w, $h)
  $g.Restore($state)
}

function Draw-RotatedImage($g, $img, $x, $y, $w, $h, $angle) {
  $state = $g.Save()
  $cx = $x + $w/2; $cy = $y + $h/2
  $g.TranslateTransform($cx, $cy)
  $g.RotateTransform($angle)
  $g.DrawImage($img, -$w/2, -$h/2, $w, $h)
  $pen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(255,0xe5,0xe3,0xda), 2)
  $g.DrawRectangle($pen, -$w/2, -$h/2, $w, $h)
  $g.Restore($state)
}

# book cover (behind icon), slight rotation
$book = [System.Drawing.Image]::FromFile((Join-Path $dir "book-mydivelog-front.png"))
$bw = 175; $bh = 270
Draw-ShadowRect $g 955 300 $bw $bh 6
Draw-RotatedImage $g $book 955 300 $bw $bh 6
$book.Dispose()

# app icon, on top
$icon = [System.Drawing.Image]::FromFile((Join-Path $dir "mediatoolbox-icon.png"))
$iw = 200; $ih = 200
Draw-ShadowRect $g 838 128 $iw $ih -6
Draw-RotatedImage $g $icon 838 128 $iw $ih -6
$icon.Dispose()

$bmp.Save((Join-Path $dir "og-image.png"), [System.Drawing.Imaging.ImageFormat]::Png)
$g.Dispose(); $bmp.Dispose()
Write-Output "done"

