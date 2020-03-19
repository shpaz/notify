Deploying Notify tool on Kubernetes 

## Introducation 
Notify is a tool used with Ceph's Bucket Notifications feature (released in Ceph's new major version, RHCS4.0). To use Bucket 
Notifications feature we have to configure two things: 
* Topic 
* Bucket notification configuration 

Notify, will use boto3 aws python library to create the sns topic against the endpoint url given (in our case, Ceph's RGW). It 
gets the topic name as argument and performs a REST request to create the wanted topic. Notify supports both RabbitMQ and Kafka
configuration, HTTP based configuration will be supported in the future. 

Notify is supported as standalone container and in K8S/Openshift orchestration environments: 

```bash 
docker run shonpaz123/notify:latest -h
usage: notify.py [-h] -e ENDPOINT_URL -a ACCESS_KEY -s SECRET_KEY -b
                 BUCKET_NAME [-k KAFKA_ENDPOINT] [-r RABBITMQ_ENDPOINT] -t
                 TOPIC

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
  -k KAFKA_ENDPOINT, --kafka-endpoint KAFKA_ENDPOINT
                        kafka endpoint in which rgw will send notifications to
  -r RABBITMQ_ENDPOINT, --rabbitmq-endpoint RABBITMQ_ENDPOINT
                        rabbitmq topic in which rgw will send notifications to
  -t TOPIC, --topic TOPIC
                        kafka topic in which rgw will send notifications to
```

For now, when using Notify we need to provide the needed credentials (access and secret keys), the bucket name, the MQ target (whether it's Kafka or RabbitMQ), 
the topic name end the RGW's endpoint url. 

Example of how Notify job is configured on Kubernetes: 

```bash 
apiVersion: batch/v1
kind: Job
metadata:
  name: notify
spec:
  parallelism: 1
  template:
    metadata: 
      name: notify
    spec: 
      containers:
        - image: shonpaz123/notify
          name: notify
          args:
               ["--endpoint-url", "http://rook-ceph-rgw-my-store.rook-ceph.svc.cluster.local",
                "--access-key", "************", 
                "--secret-key", "********************",
                "--bucket", "notifications",
                "--kafka-endpoint", "bootstrap.kafka.svc.cluster.local", 
                "--topic", "notifications"]
      restartPolicy: Never
```
As you see, this is an example of using rook-ceph as S3 service and strimzi as Kafka cluster. 
