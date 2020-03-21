FROM python:3

COPY . /usr/src/app/mlservice

WORKDIR /usr/src/app/mlservice

EXPOSE 80

RUN pip install -r requirements.txt
RUN export PYTHONPATH=${PYTHONPATH}:/usr/src/app

ENTRYPOINT ["./entrypoint.sh"]