import bz2
import json
import csv
import time

from kafka import KafkaProducer

#################### Configuration ####################
bootstrap_servers = ['42.194.194.145:19092']
kafka_topic = "rcas_reddit_raw"
file_path = "/Users/bytedance/Documents/personal/redditdata/reddit_crypto.csv"
#######################################################

producer = KafkaProducer(bootstrap_servers=bootstrap_servers)
attrs = ["id", "created_utc", "link_id", "subreddit_id",
        "score", "stickied", "body"]

if __name__ == '__main__':
    start = time.time()
    print("Start pushing reddits to kafka cluster")

    with open(file_path) as f:
        csv_reader = csv.DictReader(f, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                #print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                try:
                    record = {}
                    for attr in attrs:
                        item = str(row[attr]).replace('\n', '')
                        record[attr] = item if item is not None else ""
                    producer.send(kafka_topic, json.dumps(record).encode('utf-8'))
                    #print(json.dumps(record).encode('utf-8'))

                except BaseException as e:
                    print("Error on parsing data %s" % str(e))
                line_count += 1

            if line_count % 10000 == 0:
                end = time.time()
                elapsed = end - start
                print("#Rows sent: " + str(line_count) + "  elapsed: " + str(int(elapsed)) + "sec")


