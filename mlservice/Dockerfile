FROM python:3

WORKDIR /usr/src/app

COPY . ./mlservice

RUN pip install -r ./mlservice/requirements.txt
RUN export PYTHONPATH=${PYTHONPATH}:.

EXPOSE 80

CMD [ "python", "./mlservice/sentiment/vader_sentiment.py" ]