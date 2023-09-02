
.PHONY: minikube-start minikube-tunnel minikube-ports

minikube-start:
	minikube start --insecure-registry "10.0.0.0/24"

minikube-tunnel:
	minikube tunnel

minikube-ports:

flask:
	flask --app porta run
