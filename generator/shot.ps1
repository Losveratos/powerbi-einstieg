# Nimmt den Bildschirm in voller physischer Auflösung auf.
#   powershell -ExecutionPolicy Bypass -File shot.ps1 -Name modul-01
# Wird aufgerufen, während Power BI im gewünschten Zustand im Vordergrund
# steht. Die roten Markierungen setzt danach annotate.py.
#
# Ohne den DPI-Aware-Aufruf liefert Windows nur die skalierte Auflösung
# (z. B. 1280x800 statt 1920x1200) - die Screenshots wären unscharf.
param(
    [Parameter(Mandatory = $true)][string]$Name,
    [string]$Ordner = "C:\Users\MichaelTenner\Desktop\powerbi-einstieg\site\img\raw"
)

Add-Type -AssemblyName System.Windows.Forms, System.Drawing
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class Dpi {
    [DllImport("user32.dll")] public static extern bool SetProcessDPIAware();
}
"@
[Dpi]::SetProcessDPIAware() | Out-Null

$bounds = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
$bmp = New-Object System.Drawing.Bitmap $bounds.Width, $bounds.Height
$gfx = [System.Drawing.Graphics]::FromImage($bmp)
$gfx.CopyFromScreen($bounds.Location, [System.Drawing.Point]::Empty, $bounds.Size)

if (-not (Test-Path $Ordner)) { New-Item -ItemType Directory -Force -Path $Ordner | Out-Null }
$ziel = Join-Path $Ordner "$Name.png"
$bmp.Save($ziel, [System.Drawing.Imaging.ImageFormat]::Png)

$gfx.Dispose()
$bmp.Dispose()
"$ziel  ($($bounds.Width)x$($bounds.Height))"
