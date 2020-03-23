# choose python image
FROM python:3.7-alpine

# create a user to have minimal access 
RUN adduser -D notifier 
USER notifier 

# install needed pip packages
WORKDIR /usr/src/app
COPY --chown=notifier:notifier notify.py ./
COPY --chown=notifier:notifier requirements.txt ./
RUN pip3 install --user --upgrade -r requirements.txt

RUN mkdir -p ~/.aws/models/s3/2006-03-01/ 
COPY --chown=notifier:notifier service-2.sdk-extras.json ~/.aws/models/s3/2006-03-01/

# run script from entry point
ENTRYPOINT [ "python3", "./notify.py" ]
