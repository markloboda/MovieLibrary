kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.9.5/deploy/static/provider/cloud/deploy.yaml
kubectl apply -f ingress.yaml
kubectl apply -f etcd.yaml

kubectl apply -f browse-library.yaml
kubectl apply -f login-register.yaml
kubectl apply -f secret.yaml
kubectl apply -f user-interface.yaml