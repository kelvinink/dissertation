FROM python:3

COPY . /usr/src/app/data_processing

WORKDIR /usr/src/app/data_processing

RUN pip install -r requirements.txt
RUN export PYTHONPATH=${PYTHONPATH}:/usr/src/app
RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]