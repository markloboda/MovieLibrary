Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

kubectl apply -f ..\k8s\login-register-deployment.yaml
kubectl apply -f ..\k8s\browse-library-deployment.yaml
kubectl apply -f ..\k8s\watchlist-watched-deployment.yaml
kubectl get pods