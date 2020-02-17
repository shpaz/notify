# choose python image
FROM python:3

# install needed pip packages
WORKDIR /usr/src/app
COPY notify.py ./
COPY requirements.txt ./
RUN pip3 install -r requirements.txt

# run script from entry point
ENTRYPOINT [ "python3", "./notify.py" ]
