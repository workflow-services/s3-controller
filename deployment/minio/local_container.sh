docker run -d \
  -p 9000:9000 \
  -e "MINIO_ACCESS_KEY=admin" \
  -e "MINIO_SECRET_KEY=password" \
  --name minio \
  minio/minio server /data
