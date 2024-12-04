minikube start
minikube docker-env | Invoke-Expression
docker build -t login-register-service:latest .
kubectl apply -f deployment.yaml
minikube service login-register-service --url

$uri = "http://127.0.0.1:50816/register"
$headers = @{
    "Content-Type" = "application/json"
}
$body = @{
    "username" = "testuser"
    "password" = "testpassword"
}

Invoke-RestMethod -Uri $uri -Method Post -Headers $headers -Body ($body | ConvertTo-Json)