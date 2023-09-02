
# CDKTF Requirements and Implementation plan

Document process of analysis, time constrained development process, and final solution. 

Implement Kubernetes deployment of sedaro-nano supporting services utilizing CDKTF(Typescript).

Utilize Dask distributed processing to parallelize propagation calculation. Ideally share and forward necessary state(QRangeStore data + previous timesteps) to propagation calculations, then reduce calculated state to inform downstream calculation.

HTTP request to Frontend checks Redis for previously calculated `data.js`, keyed by the number of propagation iterations. If the data does not exist, submit work to Dask, and when complete write to redis. Once written to Redis, webpage will automatically render.

Document the lack of security controls, horizontal scalability, and situation.

# Complications

* CDKTF[Typescript] dependency on NPM(from previously existing environment) threw a number of errors until fully rebuilding dev environment.
  * Fell into CDKTF Constructs hole, appears to be low value-per-complexity for a simple project.
* Stable Dask versions(2023.01.0) is on Python 3.8, but `sim.ipynb` utilizes Python 3.9+ methods requiring Dask 2023.8.+. Python3 ecosystem has is less stable than anticipated.
* Dask Array, DataFrames, or Bag for QRange `store`? The DiffEqu Propagation algorithm makes sense, but I need to understand Dask's data structures, and capabilities better to fully take advantage of it's parallelism.
  * Used `client.upload_file(..)` to supply propagation code to workers from flask app. Unsure of true best practices.
* There was an unfortunate amount of learn by doing, not testing, so lacking in base of unit tests for future stability. Time, and context switching constrained with a day job.
* 


# Kubernetes resources

## Namespace

* sedaro(all downstream resources installed in the namespace)

## Services

* Frontend
* dask-notebook(jupyter)
* dask-scheduler

## Deployments

Ideally all envs run identical Python environments. [Efficiency made by using published ]

* dask-scheduler (1)
* dask-workers (3 to start)
* jupyter-notebook (1, with dask plugin installed)

* frontend: Flask
  * Responds to http requests
  * Consults backend if data is already present
  * Launches dask workers if data not cached
    * Optimally only one request to Dask for work to be done will be made but first keeping the solution simple.
* Backend to cache data.js: Redis
  * Data path: `redis:/propagation/<int: step count>`

## TODO:

* [x] Create minikube cluster
* [x] define TF K8s resources vi CDKTF
* [ ] ~CDKTF conversion of TF declarations~ not needed, use Typescript for all simple declarations.
  * [x] Deploy to minikube
  * [x] Expose port to host machine via Service[LoadBalancer || NodePort]
* [x] `minikube` setup
  * [x] `minikube tunnel`
  * [ ] `minikube` forward local docker registry 
* [x] Dask invoked from Flask service frontend: `porta`
  * [x] EnvVars to configure: `DASK_SCHEDULER=localhost:8786 REDIS_ADDR=localhost flask --app porta run`

**Bookark**
* [ ] (started) Dockerfile to build flask app image
* [ ] `minikube start --insecure-registry...` to upload flask app image for execution.
  * [ ] CDKTF Deployment for `porta`
  * [x] CDKTF Service(with exposed NodePort) for `porta`


