FROM ubuntu:18.04
COPY . /super_mario_bros

# install dependencies
RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python

RUN pip3 install --upgrade pip \
  && cd /super_mario_bros/ \
  && pip install -r requirements.txt

# run unit test
RUN python -m unittest discover .

CMD [ "python", "/super_mario_bros/demo.py"]