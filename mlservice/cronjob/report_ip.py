# import time
# import uuid
# import requests
#
# import redis
#
# from mlservice.conf import config
#
# id = str(uuid.uuid1())
# while True:
#     ts = str(time.time())
#     ip = requests.get("http://icanhazip.com").content.decode('utf-8').strip()
#     print(id + ip + ts)
#     time.sleep(3)