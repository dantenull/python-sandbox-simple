
## introduce

简易python运行环境。
在语言侧面保证安全性。

## usage

### docker image

```shell
docker build -f dockerfile.base -t python-sandbox-simple-base .
docker build -f dockerfile -t python-sandbox-simple .
```

### docker container

```shell
docker run -d --name python-sandbox-simple -p 8009:8009 python-sandbox-simple
```

### k8s

```shell
minikube image load python-sandbox-simple:latest
kubectl apply -f sandbox.yaml
```

```shell
kubectl port-forward -n sandbox pod/pod-name 8009:8009
```
