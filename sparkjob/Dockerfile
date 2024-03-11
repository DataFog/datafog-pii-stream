FROM python:3.11-alpine
USER root
RUN adduser -D muser
RUN apk update && apk add bash && apk add openjdk11 && apk add build-base
RUN pip install pyspark
RUN wget https://dlcdn.apache.org/spark/spark-3.5.1/spark-3.5.1-bin-hadoop3.tgz -P /home/muser
RUN cd /home/muser && tar -xzvf /home/muser/spark-3.5.1-bin-hadoop3.tgz
RUN chmod a+x /home/muser/spark-3.5.1-bin-hadoop3/bin/spark-submit
# TODO: Pin this
RUN pip install https://huggingface.co/beki/en_spacy_pii_fast/resolve/main/en_spacy_pii_fast-any-py3-none-any.whl
RUN pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_lg-3.4.1/en_core_web_lg-3.4.1-py3-none-any.whl
RUN pip install datafog

ADD ./sparkjob/pii_stream.py /home/muser
USER muser
WORKDIR /home/muser
ENTRYPOINT ["/home/muser/spark-3.5.1-bin-hadoop3/bin/spark-submit","--packages","org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1","/home/muser/pii_stream.py"]