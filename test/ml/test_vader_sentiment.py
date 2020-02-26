import requests
from multiprocessing import Process

def test_sentiment(x):
    seq = 0
    while True:
        response = requests.get("http://106.13.90.40:8080/api/ml/sentiment?text=your_sentence")
        seq += 1
        print(response.text + "  " + str(seq))

if __name__ == '__main__':
    for x in range(8):
        Process(target=test_sentiment, args=(x,)).start()