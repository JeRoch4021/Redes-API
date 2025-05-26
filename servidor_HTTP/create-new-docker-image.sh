docker build -t jeshuarocha/fastapi-server:latest .
docker push jeshuarocha/fastapi-server:latest
kubectl apply -f servidor_fastapi.yaml
