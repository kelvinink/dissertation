FROM python:3

COPY . /usr/src/app/data_processing

WORKDIR /usr/src/app/data_processing

EXPOSE 80

RUN pip install -r requirements.txt
RUN export PYTHONPATH=${PYTHONPATH}:/usr/src/app

ENTRYPOINT ["./entrypoint.sh"]