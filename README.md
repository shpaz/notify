## Notify tool 

# Introduction 

This repository contains the source code of `notify` tool, which is a python3 based tool wrapped by a container used to configure Ceph Bucket Notifications easily. This tool gets few parameters such as endpoint_url, access_key, secret_key, topic etc and use them to configure the bucket notifications. 
Notify tool, will create a topic that will eventually get the notifications for the object's creation/removal and move them into the MQ endpoint. As Ceph Bucket Notifications feature, Notify also supports push-endpoints for AMQP/Kafka/HTTP targets.
Notify tool is supported for Kubernetes and Openshift environments, examples can be found in the relevant directories in this repository. 

# Installation 

To run notify, please pull the docker image: 
```bash 
docker pull shonpaz123/notify:latest
```

A help manual will be printed by using ```docker run shonpaz123/notify -h``` command: 
```bash 
usage: notify.py [-h] -e ENDPOINT_URL -a ACCESS_KEY -s SECRET_KEY -b
                 BUCKET_NAME [-ke KAFKA_ENDPOINT] [-ae AMQP_ENDPOINT]
                 [-he HTTP_ENDPOINT] -t TOPIC [-f FILTER]

optional arguments:
  -h, --help            show this help message and exit
  -e ENDPOINT_URL, --endpoint-url ENDPOINT_URL
                        endpoint url for s3 object storage
  -a ACCESS_KEY, --access-key ACCESS_KEY
                        access key for s3 object storage
  -s SECRET_KEY, --secret-key SECRET_KEY
                        secret key for s3 object storage
  -b BUCKET_NAME, --bucket-name BUCKET_NAME
                        s3 bucket name
  -ke KAFKA_ENDPOINT, --kafka-endpoint KAFKA_ENDPOINT
                        kafka endpoint in which rgw will send notifications to
  -ae AMQP_ENDPOINT, --amqp-endpoint AMQP_ENDPOINT
                        amqp endpoint in which rgw will send notifications to
  -he HTTP_ENDPOINT, --http-endpoint HTTP_ENDPOINT
                        http endpoint in which rgw will send notifications to
  -t TOPIC, --topic TOPIC
                        topic name in which rgw will send notifications to
  -f FILTER, --filter FILTER
                        A filter such as prefix, suffix, metadata or tags
```
Here you can see all the needed parameters where you have to specify the endpoint url, access key, secret key, bucket name and the topic name. You have the ability to choose whether you want to use Kafka/AMQP/HTTP endpoints, just specify the url and notify will automatically use it to create the push endpoint. 

# Filters 
In Octopus (future RHCS5.X version), there is also filter support, which means you can decide which object will be notified according to a given filter pattern. supported filters are prefix/suffix/regex/metadata/tags. When using the proper Ceph version, you could specify a filter and notify will configure the bucket notification for you. 
