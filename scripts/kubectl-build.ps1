minikube docker-env | Invoke-Expression
docker build -t login-register-service:latest .\src\login_register_service\
kubectl apply -f .\src\login_register_service\deployment.yaml