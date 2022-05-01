from debian:latest


RUN apt-get update -y && \
  apt-get install -y python-3.8.2 python3-pip  gcc musl-dev libcrypto++-dev libgmp-dev 

WORKDIR /app

COPY . /app



#RUN cd heartbeat/ && python3 setup.py install
RUN . /app/venv/bin/activate && pip3 --no-cache-dir install -r requirements.txt && cd heartbeat/ && python3 setup.py install

EXPOSE 5566
CMD . /app/venv/bin/activate && exec python3 views.py
#ENTRYPOINT ["python3"]
#CMD ["views.py"]	
