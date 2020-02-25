#############################################################################
# Usage: wget http://localhost/api/ml/sentiment?sent=your_sentence
#############################################################################

import time
import os
import nltk
from flask import Flask, jsonify, request, Response
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# nltk.download('vader_lexicon')
lexicon_file='../model/vader_lexicon/vader_lexicon.txt'
sia = SentimentIntensityAnalyzer(lexicon_file=lexicon_file)

app = Flask(__name__)

@app.route('/api/ml/sentiment', methods=['GET'])
def sentiment():
    global sia
    text = request.args.get('text')
    scores = sia.polarity_scores(text)
    return str(scores)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)