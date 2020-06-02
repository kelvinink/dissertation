# Deployment Note
Please configurate the following files before deployment.

# Data Source
data_source/twitter_archive/archive_source.py

# Data Processing
data_processing/config.py

# Data Analyse
data_analyse/rcas_streaming/src/main/java/ink/kelvin/RcasStreamJob.java

# Flink
flink/jobmanager/conf/flink-conf.yaml
flink/jobmanager/etc/hosts
flink/taskmanager/conf/flink-conf.yaml
flink/taskmanager/etc/hosts

# Kafka
kafka/.env

**Set Partitions for Topics**
```shell
docker exec -it kafka1 bash
kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 8 --topic rcas_twitter_raw
kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 8 --topic rcas_twitter_after_sentiment

kafka-topics.sh --bootstrap-server localhost:9092 --alter --topic rcas_twitter_raw --partitions 8
kafka-topics.sh --bootstrap-server localhost:9092 --alter --topic rcas_twitter_after_sentiment --partitions 8

kafka-topics.sh --describe --bootstrap-server localhost:9092
```

# Fix Crypto Virus
```shell
https://github.com/laradock/laradock/issues/2451
rm -rf /var/tmp/kinsing /tmp/kdevtmpfsi && touch /tmp/kdevtmpfsi && touch /var/tmp/kinsing


https://blog.csdn.net/Cupster/article/details/104498884
vim /tmp/kill_kdevtmpfsi.sh

ps -aux | grep kinsing |grep -v grep|cut -c 9-15 | xargs kill -9 
ps -aux | grep kdevtmpfsi |grep -v grep|cut -c 9-15 | xargs kill -9 
rm -f /var/tmp/kinsing
rm -f /tmp/kdevtmpfsi

* * * * * /tmp/kill_kdevtmpfsi.sh
```