oh-my-posh init pwsh --config 'https://raw.githubusercontent.com/JanDeDobbeleer/oh-my-posh/main/themes/multiverse-neon.omp.json' | Invoke-Expression
if (-not (Test-Path $profile)) {
  New-Item -ItemType File -Path (Split-Path $profile) -Force -Name (Split-Path $profile -Leaf)
}
$profileEntry = 'Remove-Item Alias:ni -Force -ErrorAction Ignore'
$profileContent = Get-Content $profile
if ($profileContent -notcontains $profileEntry) {
  ("`n" + $profileEntry) | Out-File $profile -Append -Force -Encoding UTF8
}
Remove-Item Alias:ni -Force -ErrorAction Ignore
function ls_git { & 'C:\Program Files\Git\usr\bin\ls' --color=auto -hF $args }
Set-Alias -Name ls -Value ls_git -Option AllScope
