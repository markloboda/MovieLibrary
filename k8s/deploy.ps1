function DeployAndCheck {
    param(
        [string]$file
    )
    kubectl apply -f $file
    $status = kubectl get -f $file
    if ($status -eq "Error") {
        Write-Output "Failed to deploy $file"
        Write-Output "-------------------"
        Write-Output ""
        exit 1
    }
    Write-Output "Deployed $file"
    Write-Output "-------------------"
    Write-Output ""	
}

DeployAndCheck https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
DeployAndCheck https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.9.5/deploy/static/provider/cloud/deploy.yaml
DeployAndCheck "ingress.yaml"
DeployAndCheck "etcd.yaml"
DeployAndCheck "secret.yaml"
DeployAndCheck "browse-library.yaml"
DeployAndCheck "login-register.yaml"
DeployAndCheck "user-interface.yaml"
DeployAndCheck "watchlist.yaml"
DeployAndCheck "openapi.yaml"
