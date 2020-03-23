# choose python image
FROM python:3.7-alpine

# install needed pip packages
WORKDIR /usr/src/app
COPY notify.py ./
COPY requirements.txt ./
RUN pip3 install --upgrade -r requirements.txt

RUN mkdir -p ~/.aws/models/s3/2006-03-01/ 
COPY service-2.sdk-extras.json ~/.aws/models/s3/2006-03-01/service-2.sdk-extras.json

# run script from entry point
ENTRYPOINT [ "python3", "./notify.py" ]
