
.PHONY: main.ts synth deploy dask-notebook-url dask-scheduler-url

start:
	minikube start

synth:
	cdktf synth

deploy: synth
	cdktf deploy --skip-synth --auto-approve sedaro

dask-notebook-url:
	minikube service dask-notebook -n sedaro --url

dask-scheduler-url:
	minikube service dask-scheduler -n sedaro --url
