FROM ubuntu:20.04
RUN apt update && apt install -y python3 pip

USER root
RUN adduser --disabled-login muser

RUN pip install streamlit kafka-python uuid
ADD ./ui/app.py /home/muser
USER muser
WORKDIR /home/muser
ENTRYPOINT ["streamlit","run","app.py"]