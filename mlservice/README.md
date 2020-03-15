# Build Docker Container
```shell
docker build -t mlservice:0.0.1 .
```

# Run Container
```shell
docker run -it --rm --name mlservice -p 8080:80 mlservice:0.0.1
```

# Interface
```shell
curl http://localhost:{{port}}/api/ml/sentiment?text={{your_sentence}}
```

# Docker Scaling
```
docker-compose up --scale mlservice=3
```