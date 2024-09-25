FROM python:3.10-alpine

MAINTAINER Nils Ost

ENV HOME /app

WORKDIR $HOME

ADD requirements.txt $HOME/
RUN pip3 install -r $HOME/requirements.txt

ADD main.py $HOME/

ENTRYPOINT ["python3"]
CMD ["main.py"]
