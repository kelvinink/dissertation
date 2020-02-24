import os

while True:
    res = os.popen("curl http://localhost:80/api/ml/sentiment?sent=your_sentence 2>/dev/null")
    print(res.read())
    res.close()