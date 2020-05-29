import bz2
import json
import subprocess

from kafka import KafkaProducer

#################### Configuration ####################
bootstrap_servers = ['106.52.240.156:19092']
kafka_topic = "rcas_twitter_raw"
data_root = "/Users/bytedance/Documents/personal/twitter_data/2019"
#######################################################

producer = KafkaProducer(bootstrap_servers=bootstrap_servers)
attrs = ["id_str", "created_at", "quote_count", "reply_count", "retweet_count", "favorite_count",
            "geo", "coordinates",  "timestamp_ms", "lang", "text"]

def generator(file_path):
    with bz2.open(file_path, "r") as f:
        for record in f:
            try:
                json_tweet = json.loads(record)
                record = {}
                for attr in attrs:
                    item = str(json_tweet[attr]).replace('\n', '')
                    record[attr] = item if item is not None else ""

                if record["lang"] != "en":
                    continue

                producer.send(kafka_topic, json.dumps(record).encode('utf-8'))
                print(json.dumps(record).encode('utf-8'))

            except BaseException as e:
                print("Error on parsing data %s" % str(e))


if __name__ == '__main__':
    months = subprocess.run(['ls', data_root], stdout=subprocess.PIPE).stdout.decode('utf-8').split("\n")
    for m in months:
        if len(m) > 0:
            month_dir = data_root + "/" + m
            file_partitions = subprocess.run(['ls', month_dir], stdout=subprocess.PIPE).stdout.decode('utf-8').split("\n")
            for p in file_partitions:
                if len(p) > 0:
                    partition_dir = month_dir + "/" + p
                    files = subprocess.run(['ls', partition_dir], stdout=subprocess.PIPE).stdout.decode('utf-8').split("\n")
                    for f in files:
                        if len(f) > 0:
                            file_path = partition_dir + "/" + f
                            generator(file_path)

