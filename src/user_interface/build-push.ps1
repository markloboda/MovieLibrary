npm run build
if ($LASTEXITCODE -ne 0) {
  Write-Error "Build failed. Stopping script."
  exit 1
}
docker build -t markloboda/user-interface:latest .
docker push markloboda/user-interface:latest