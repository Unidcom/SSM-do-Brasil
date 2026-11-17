param([string]$InputPdf,[string]$OutputDir,[int]$Width=550,[int]$Page=-1)
Add-Type -AssemblyName System.Runtime.WindowsRuntime
$ErrorActionPreference='Stop'
$null = [Windows.Storage.StorageFile,Windows.Storage,ContentType=WindowsRuntime]
$null = [Windows.Data.Pdf.PdfDocument,Windows.Data.Pdf,ContentType=WindowsRuntime]
$null = [Windows.Storage.Streams.InMemoryRandomAccessStream,Windows.Storage.Streams,ContentType=WindowsRuntime]
$null = [Windows.Data.Pdf.PdfPageRenderOptions,Windows.Data.Pdf,ContentType=WindowsRuntime]
$asTask = ([System.WindowsRuntimeSystemExtensions].GetMethods() | Where-Object { $_.Name -eq 'AsTask' -and $_.IsGenericMethod -and $_.GetParameters().Count -eq 1 -and $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1' } | Select-Object -First 1)
function AwaitResult($operation,$type) {
  $task = $asTask.MakeGenericMethod($type).Invoke($null,@($operation))
  $task.Wait()
  $task.Result
}
$file = AwaitResult ([Windows.Storage.StorageFile]::GetFileFromPathAsync((Resolve-Path -LiteralPath $InputPdf).Path)) ([Windows.Storage.StorageFile])
$pdf = AwaitResult ([Windows.Data.Pdf.PdfDocument]::LoadFromFileAsync($file)) ([Windows.Data.Pdf.PdfDocument])
New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null
Write-Output "Pages: $($pdf.PageCount)"
$pages = if($Page -ge 0){@($Page)}else{0..($pdf.PageCount-1)}
foreach($i in $pages){
  $p=$pdf.GetPage($i)
  $s=[Windows.Storage.Streams.InMemoryRandomAccessStream]::new()
  $opts=[Windows.Data.Pdf.PdfPageRenderOptions]::new()
  $opts.DestinationWidth=$Width
  $action=$p.RenderToStreamAsync($s,$opts)
  $actionTask=([System.WindowsRuntimeSystemExtensions].GetMethods() | Where-Object { $_.Name -eq 'AsTask' -and -not $_.IsGenericMethod -and $_.GetParameters().Count -eq 1 -and $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncAction' } | Select-Object -First 1).Invoke($null,@($action))
  $actionTask.Wait()
  $s.Seek(0)
  $input=[System.IO.WindowsRuntimeStreamExtensions]::AsStreamForRead($s)
  $path=Join-Path (Resolve-Path $OutputDir).Path ('page-{0:D2}.png' -f ($i+1))
  $out=[System.IO.File]::Create($path)
  $input.CopyTo($out)
  $out.Dispose();$input.Dispose();$s.Dispose();$p.Dispose()
}
[Environment]::Exit(0)
