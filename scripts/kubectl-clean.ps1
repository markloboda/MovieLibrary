minikube docker-env | Invoke-Expression
kubectl delete service browse-library
kubectl delete deployment browse-library-deployment
kubectl get pods --no-headers -o custom-columns=":metadata.name" | kubectl delete pods