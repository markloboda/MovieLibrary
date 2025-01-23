# Movie Library
An application for managing and searching for movies to watch.

## Documentation

### Folder structure
- assets - All the images and files used in the project.
- certs - Certificates for the application.
- k8s - Kubernetes manifests (YAML files) for deployment and orcestration.
- scripts - Usefull scripts for deploying and building the application.
- src - Source code with each service in its own directory.
- tests - Tests for the application.

### Deployment
1. Install:
- kubectl
- doctl
- Docker
- node.js (npm)

2. Make sure you have all the necesary tools installed.
3. Get Digital Ocean cluster **Config File**.
4. Connect to a Kubernetes cluster with "doctl".
5. Go to root directory of the project.
6. Run:
   - ./scripts/docker-build-push.ps1
   - ./scripts/k8s-deploy.ps1
