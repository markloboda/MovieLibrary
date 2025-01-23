
function BuildAndCheck {
  param (
    [string]$servicePath
  )
  cd $servicePath
  if (./build-push.ps1) {
    Write-Output "Service $servicePath built and pushed successfully"
  } else {
    Write-Output "Service $servicePath failed to build and push"
  }
  cd $originalPath
}

$originalPath = Get-Location
BuildAndCheck "src/browse_library_service"
BuildAndCheck "src/login_register_service"
BuildAndCheck "src/user_interface"
BuildAndCheck "src/watchlist_service"
