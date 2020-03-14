# Connect to Redis from CLI
Please ensure that your redis client and redis server reside on the same network
```shell
 docker run -it --rm --name redis-cli  redis redis-cli -h redis -p 6379
 ```