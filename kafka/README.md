# Create Network
```shell
docker network create rcas --driver bridge
```

# Compose Service
```shell
docker-compose up -d
```

# Run Kafka Client
```shell
docker run -it --rm \
    --network rcas \
    -e KAFKA_CFG_ZOOKEEPER_CONNECT=zookeeper:2181 \
    bitnami/kafka:2.4.0-ol-7-r55 \
    kafka-topics.sh --list  --zookeeper zookeeper:2181
```

# Investigating Containers
```shell
docker run -it --rm \
    --network rcas \
    -e KAFKA_CFG_ZOOKEEPER_CONNECT=zookeeper:2181 \
    bitnami/kafka:2.4.0-ol-7-r55 \
    bash

docker exec -it kafka_kafka1_1 bash
```

# Create a New Topic
```shell
docker exec -it kafka1 bash
kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic kelvin_topic
```

# List Topics
```shell
kafka-topics.sh --list --bootstrap-server localhost:9092
```

# Push Messages
```shell
docker exec -it kafka1 bash
kafka-console-producer.sh --broker-list localhost:9092 --topic kelvin_topic
```

# Receive Messages
```shell
docker exec -it kafka1 bash
kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic kelvin_topic --from-beginning
```

# Check your Consumer Group
```shell
kafka-consumer-groups.sh --bootstrap-server localhost:9092 --list
```

# Check which Group your Topic Belongs
```shell
kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group kelvin_group --describe
```

# Consumer from External of Kafka network(rcas)
```shell
docker run -it --rm \
    --network rcas \
    -e KAFKA_CFG_ZOOKEEPER_CONNECT=zookeeper:2181 \
    bitnami/kafka:2.4.0-ol-7-r55 \
    kafka-console-consumer.sh --bootstrap-server localhost:32826 --topic kelvin_topic --from-beginning
```

# Info
Path to Kafka bin:
/opt/bitnami/kafka/bin/


