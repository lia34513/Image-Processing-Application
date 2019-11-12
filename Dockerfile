FROM nikolaik/python-nodejs:python2.7-nodejs13
ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt

WORKDIR /app

ENTRYPOINT [ "./start.sh" ]
