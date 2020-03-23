# docker build -t ubuntu1604py36
FROM python:3.8-slim-buster

# install needed pip packages
WORKDIR /usr/src/app
COPY notify.py ./
COPY requirements.txt ./
RUN pip3 install --upgrade -r requirements.txt

# copy the S3 API extension to the relevant directory
COPY service-2.sdk-extras.json /usr/local/lib/python3.8/site-packages/botocore/data/s3/2006-03-01

# run script from entry point
ENTRYPOINT [ "python3", "./notify.py" ]
