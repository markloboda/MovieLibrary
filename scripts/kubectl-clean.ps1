Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

kubectl delete deployment login-register-deployment
kubectl delete deployment browse-library-deployment
kubectl delete deployment watchlist-watched-deployment
kubectl delete service login-register
kubectl delete service browse-library
kubectl delete service watchlist-watched