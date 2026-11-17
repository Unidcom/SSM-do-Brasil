Add-Type -AssemblyName System.Drawing
$dest = Join-Path $PSScriptRoot 'imagens'
New-Item -ItemType Directory -Force -Path $dest | Out-Null
$accent = [System.Drawing.ColorTranslator]::FromHtml('#0A6DBF')
$ink = [System.Drawing.ColorTranslator]::FromHtml('#142C40')
$blue = [System.Drawing.SolidBrush]::new($accent)
$dark = [System.Drawing.SolidBrush]::new($ink)
$light = [System.Drawing.SolidBrush]::new([System.Drawing.ColorTranslator]::FromHtml('#E9F2F9'))
$white = [System.Drawing.Brushes]::White
$font = [System.Drawing.Font]::new('Arial',22)
$small = [System.Drawing.Font]::new('Arial',17)
$title = [System.Drawing.Font]::new('Arial',36,[System.Drawing.FontStyle]::Bold)
$pen = [System.Drawing.Pen]::new($accent,3)
$base = Join-Path $PSScriptRoot '../../SSM-do-Brasil-main/.agents/skills/seo-geo-blog-writer/assets/logo-allblack-b64.txt'
$logoText = (Get-Content -Raw $base).Trim() -replace '^data:image/[^;]+;base64,',''
$stream = [System.IO.MemoryStream]::new([Convert]::FromBase64String($logoText))
$logo = [System.Drawing.Image]::FromStream($stream)
foreach ($kind in @('layout','processo')) {
  $bmp = [System.Drawing.Bitmap]::new(1200,675)
  $g = [System.Drawing.Graphics]::FromImage($bmp)
  $g.SmoothingMode = 'AntiAlias'
  $g.TextRenderingHint = 'AntiAliasGridFit'
  $g.Clear([System.Drawing.Color]::White)
  $g.FillRectangle($blue,0,0,1200,12)
  $g.DrawString('CARPORT SOLAR | GUIA DE CONFIGURAÇÃO',$small,$blue,50,40)
  if ($kind -eq 'layout') {
    $g.DrawString('O layout orienta a escolha',$title,$dark,50,90)
    $g.FillRectangle($light,50,180,760,365)
    for ($i=0; $i -lt 5; $i++) {
      $x = 75 + $i*140
      $g.DrawRectangle($pen,$x,205,125,110)
      $g.DrawRectangle($pen,$x,405,125,110)
    }
    $g.DrawString('FAIXA DE CIRCULAÇÃO',$font,$dark,180,345)
    $g.DrawLine($pen,90,375,755,375)
    $g.DrawLine($pen,755,375,740,365)
    $g.DrawLine($pen,755,375,740,385)
    $g.DrawString('Verificar na planta:',$font,$dark,850,205)
    $g.DrawString('Vagas e divisas',$small,$dark,850,265)
    $g.DrawString('Acessos e manobras',$small,$dark,850,315)
    $g.DrawString('Posição dos apoios',$small,$dark,850,365)
    $g.DrawString('Rotas de pedestres',$small,$dark,850,415)
    $g.DrawString('Planta gráfica ilustrativa, sem escala. Não representa produto ou projeto executivo.',$small,$dark,50,565)
  } else {
    $g.DrawString('Do estacionamento ao projeto',$title,$dark,50,90)
    $labels = @('LEVANTAR','COMPATIBILIZAR','DEFINIR')
    $lines = @(@('Planta e medidas','Vagas e acessos','Dados dos módulos'),@('Cobertura e vagas','Circulação e apoios','Interferências do local'),@('Solução estrutural','Fundações e fixações','Interfaces do projeto'))
    for ($i=0; $i -lt 3; $i++) {
      $x = 50 + $i*375
      $g.FillRectangle($light,$x,220,350,280)
      $g.FillRectangle($blue,$x,220,350,65)
      $g.DrawString($labels[$i],$font,$white,($x+22),237)
      for ($j=0; $j -lt 3; $j++) {$g.DrawString($lines[$i][$j],$small,$dark,($x+22),(315+$j*48))}
    }
    $g.DrawString('Fluxo ilustrativo. As definições técnicas dependem da engenharia do projeto.',$small,$dark,50,550)
  }
  $lw = 125; $lh = [int]($logo.Height * $lw / $logo.Width)
  $g.DrawImage($logo,1025,(640-$lh),$lw,$lh)
  $g.DrawString('Conteúdo preparado para a SSM do Brasil',$small,$dark,50,625)
  $bmp.Save((Join-Path $dest "$kind-carport-editorial.png"),[System.Drawing.Imaging.ImageFormat]::Png)
  $g.Dispose(); $bmp.Dispose()
}
$logo.Dispose(); $stream.Dispose()
