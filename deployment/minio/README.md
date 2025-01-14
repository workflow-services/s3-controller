1. Secret YAML


```yaml
apiVersion: v1
kind: Secret
metadata:
  name: minio-secret
type: Opaque
data:
  # Replace 'minioadmin' and 'minioadminpassword' with base64 encoded values
  MINIO_ROOT_USER: bWluaW9hZG1pbg==
  MINIO_ROOT_PASSWORD: bWluaW9hZG1pbnBhc3N3b3Jk
```


Use `echo -n 'your_value' | base64` to generate the Base64 values for your username and password.

2. StatefulSet

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: minio
spec:
  serviceName: "minio-service"
  replicas: 1
  selector:
    matchLabels:
      app: minio
  template:
    metadata:
      labels:
        app: minio
    spec:
      containers:
      - name: minio
        image: minio/minio:latest
        args:
        - server
        - /data
        env:
        - name: MINIO_ROOT_USER
          valueFrom:
            secretKeyRef:
              name: minio-secret
              key: MINIO_ROOT_USER
        - name: MINIO_ROOT_PASSWORD
          valueFrom:
            secretKeyRef:
              name: minio-secret
              key: MINIO_ROOT_PASSWORD
        ports:
        - containerPort: 9000
          name: http
        volumeMounts:
        - name: data
          mountPath: /data
      volumes:
        - name: data
          persistentVolumeClaim:
            claimName: minio-pvc
```


3. Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: minio-service
spec:
  ports:
  - port: 9000
    targetPort: 9000
  selector:
    app: minio
  type: ClusterIP
```

4. PVC

```
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: minio-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
```




