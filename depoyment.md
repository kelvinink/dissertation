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