from kafka import KafkaAdminClient


admin = KafkaAdminClient(bootstrap_servers=['localhost:32775'])
admin.create_topics('kelvin_topic')