$originalPath = Get-Location

cd k8s
./deploy.ps1
Write-Output "K8s deployed"
cd $originalPath