## Deploying Notify tool on Openshift 

Notify is a tool used with Ceph's Bucket Notifications feature (released in Ceph's new major version, RHCS4.0). To use Bucket 
Notifications feature we have to configure two things: 
* Topic 
* Bucket notification configuration 

Notify, will use boto3 aws python library to create the sns topic against the endpoint url given (in our case, Ceph's RGW). It 
gets the topic name as argument and performs a REST request to create the wanted topic. Notify supports AMQP, Kafka
and HTTP configuration.

Notify is supported as standalone container and in K8S/Openshift orchestration environments: 

```bash 
docker run shonpaz123/notify:latest -h
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

For now, when using Notify we need to provide the needed credentials (access and secret keys), the bucket name, the MQ target (whether it's Kafka or RabbitMQ), 
the topic name end the RGW's endpoint url. 

When using notify, all you need to do is fill up and environment file, which has all the needed information:

```bash 
ACCESS_KEY=
SECRET_KEY=
ENDPOINT_URL=
BUCKET_NAME=
KAFKA_ENDPOINT=      
FILTER=              # example: '{"Key": {"FilterRules": [{"Name": "prefix", "Value": "hosts"}]}}'
FILTER_TYPE=         # can contain prefix/suffix/regex/metadata/tags
TOPIC=
```
In the background, notify will take al the needed information and turn it into a K8S job.
After you have notify env file configured, just run the following command: 

```bash 
oc create -f notify.yaml --param-file notify.env | oc create -f -
``` 
Now Verify the job has completed successfuly: 

```bash 
NAME                                                           READY   STATUS      RESTARTS   AGE
notify-5z6xq                                                  0/1     Completed   0          2m
``` 
