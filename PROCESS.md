

## Initialize CDKTF

```
cdktf init --template=typescript \
             --project-name=sedaro-nano \
             --project-description="Deploy Sedaro's simulation approximation to minikube via CDKTF" \
             --providers="kubernetes@~>2.14" \
             --local
```
