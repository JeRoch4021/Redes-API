for pod in $(kubectl get pods -l app=fastapi-server -o name); do
  echo "==== Logs for $pod ===="
  kubectl logs $pod
done
