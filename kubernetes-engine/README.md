## GKE
### Basic Process
- 영역 및 클러스터 이름에 대한 환경 변수 설정
```
export my_zone=us-central1-a
export my_cluster=standard-cluster-1
```

- kubectl 자동 완성을 활성화(Tab)
```
source <(kubectl completion bash)
```

- kubectl 명령줄 도구에 대한 클러스터 액세스를 구성
```
gcloud container clusters get-credentials $my_cluster --zone $my_zone
```

- 작업 실행
```
kubectl apply -f example-job.yaml
```

- 작업 상태 확인
```
kubectl describe job example-job
```

- 모든 Pod 리소스 보기
```
kubectl get pods
```

- 클러스터의 작업 목록 가져오기
```
kubectl get jobs
```

- Pod의 로그 보기
```
kubectl logs [pod_name]
```

- 작업 삭제 명령
```
kubectl delete job example-job
```

- Crontab을 활용하여 자동화 프로세스 Basic
```
apiVersion: batch/v1
kind: CronJob
metadata:
  name: hello
spec:
  schedule: "*/1 * * * *"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: hello
            image: busybox
            args:
            - /bin/sh
            - -c
            - date; echo "Hello, World!"
          restartPolicy: OnFailure
```

### 배포
```
kubectl apply -f ./nginx-deployment.yaml
kubectl get deployments
kubectl scale --replicas=3 deployment nginx-deployment
kubectl set image deployment.v1.apps/nginx-deployment nginx=nginx:1.9.1 --record
kubectl rollout status deployment.v1.apps/nginx-deployment
kubectl get deployments
kubectl rollout history deployment nginx-deployment
kubectl rollout undo deployments nginx-deployment
kubectl rollout history deployment nginx-deployment
kubectl rollout history deployment/nginx-deployment --revision=3
```

- LoadBalancer Basic
```
apiVersion: v1
kind: Service
metadata:
  name: nginx
spec:
  type: LoadBalancer
  selector:
    app: nginx
  ports:
  - protocol: TCP
    port: 60000
    targetPort: 80
```
```
kubectl apply -f ./service-nginx.yaml
```
