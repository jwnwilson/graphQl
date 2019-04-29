FROM python:3.6-slim
RUN useradd -m -d /home/scp scp
WORKDIR /home/scp

RUN apt-get update && apt-get install -y make
RUN pip install --no-cache-dir --trusted-host pypi.python.org pipenv

ADD . .
RUN pipenv install --system --deploy

RUN chown -R scp:scp ./

USER scp
CMD make run