# Adding JobManager/TaskManager Instances to a Cluster
You can add both JobManager and TaskManager instances to your running cluster with the bin/jobmanager.sh and bin/taskmanager.sh scripts.

**Starting Cluster**
```
bin/start-cluster.sh
```

**Adding a JobManager**
```
bin/jobmanager.sh ((start|start-foreground) [host] [webui-port])|stop|stop-all
```
**Adding a TaskManager**
```
bin/taskmanager.sh start|start-foreground|stop|stop-all
```
Make sure to call these scripts on the hosts on which you want to start/stop the respective instance.

# Docker Flink
## Taskmanager Scale Up
```
docker-compose --scale taskmanager=<N>
```

