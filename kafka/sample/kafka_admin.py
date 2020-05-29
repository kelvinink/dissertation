from kafka import KafkaAdminClient
from kafka import KafkaConsumer

bootstrap_servers=['129.204.135.185:32770']

admin = KafkaAdminClient(bootstrap_servers=bootstrap_servers)

def create_topic(topic):
    admin.create_topics(topic)

def delete_topic(topic):
    admin.delete_topics(topic)

def list_topics(topic):
    consumer = KafkaConsumer(topic,
                             bootstrap_servers=bootstrap_servers,
                             auto_offset_reset='earliest')
    print("List of Topics: ")
    print(consumer.topics())


if __name__ == '__main__':
    t = 't1'
    create_topic(t)
    list_topics(t)
    delete_topic(t)
    list_topics(t)
