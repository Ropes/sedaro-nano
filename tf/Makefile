
.PHONY: start synth deploy minikube-services

start:
	minikube start

minikube-services:
	minikube service --all --namespace sedaro

synth:
	cdktf synth

deploy: synth
	cdktf deploy --skip-synth --auto-approve sedaro
