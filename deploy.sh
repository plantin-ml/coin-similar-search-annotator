kubectl apply -f ./k8s/api-deployment.yaml
kubectl apply -f ./k8s/client-deployment.yaml

kubectl apply -f ./k8s/api-service.yaml
kubectl apply -f ./k8s/client-service.yaml

kubectl apply -f ./k8s/api-ingress.yaml
kubectl apply -f ./k8s/client-ingress.yaml
