minikube docker-env | Invoke-Expression
kubectl delete service login-register-service
kubectl delete deployment login-register-service
kubectl get pods --no-headers -o custom-columns=":metadata.name" | kubectl delete pods