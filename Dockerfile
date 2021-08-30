FROM python:3.9

ENV PYTHONUNBUFFERED 1

WORKDIR /code

RUN apt-get update && \
    apt-get install -y jq && \
    apt-get install -y procmail && \
    apt-get install cron && \
    apt-get clean

COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /code/
COPY . /code/

##custom entry point — needed by cron
RUN chmod +x /code/entrypoint.sh
RUN chmod 0644 /code/cron


# RUN groupadd -r django && useradd -r -g django django
# RUN chown -R django /code
# RUN chmod u+s /usr/sbin/cron

