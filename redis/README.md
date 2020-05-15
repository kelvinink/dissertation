# Connect to Redis from CLI
Please ensure that your redis client and redis server reside on the same network
```shell
# Option 1
docker exec -it redis bash
redis-cli

# Option 2
docker run -it --rm --name redis-cli -network rcas  redis:6.0-rc2 redis-cli -h redis -p 6379
 ```