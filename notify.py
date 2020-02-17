'''
@Author Shon Paz
@Date   16/02/2020
'''

import boto3
import json
import botocore
import humanfriendly
import argparse
import urllib.parse

'''This class configures bucket notifications for both kafka and rabbitmq endpoints for real-time message queuing'''


class Notifier:

    def __init__(self):

        # creates all needed arguments for the program to run
        parser = argparse.ArgumentParser()
        parser.add_argument('-e', '--endpoint-url', help="endpoint url for s3 object storage", required=True)
        parser.add_argument('-a', '--access-key', help='access key for s3 object storage', required=True)
        parser.add_argument('-s', '--secret-key', help='secret key for s3 object storage', required=True)
        parser.add_argument('-b', '--bucket-name', help='s3 bucket name', required=True)
        parser.add_argument('-k', '--kafka-endpoint', help='kafka endpoint in which rgw will send notifications to', required=False)
        parser.add_argument('-r', '--rabbitmq-endpoint', help='rabbitmq topic in which rgw will send notifications to', required=False)
        parser.add_argument('-t', '--topic', help='kafka topic in which rgw will send notifications to', required=True)


        # parsing all arguments
        args = parser.parse_args()

        # building instance vars
        self.endpoint_url = args.endpoint_url
        self.access_key = args.access_key
        self.secret_key = args.secret_key
        self.bucket_name = args.bucket_name
        self.kafka_endpoint = args.kafka_endpoint
        self.rabbitmq_endpoint = args.rabbitmq_endpoint
        self.topic = args.topic
        self.sns = boto3.client('sns', 
                               endpoint_url=self.endpoint_url, 
                               aws_access_key_id=self.access_key,
                               region_name='default', 
                               aws_secret_access_key=self.secret_key,
                               config=botocore.client.Config(signature_version = 's3'))

        self.s3 = boto3.client('s3',
                              endpoint_url = self.endpoint_url,
                              aws_access_key_id = self.access_key,
                              aws_secret_access_key = self.secret_key,
                              region_name = 'default',
                              config=botocore.client.Config(signature_version = 's3'))


    ''' This function creates and sns-like topic with configured MQ endpoint'''
    def create_sns_topic(self):
        
        # in case wanted MQ endpoint is kafka 
        if(self.kafka_endpoint):
            endpoint_args = 'push-endpoint=kafka://' + self.kafka_endpoint + '&kafka-ack-level=broker'
        
        # in case wanted MQ endpoint is rabbitmq
        elif(self.rabbitmq_endpoint): 
            endpoint_args = 'push-endpoint=amqp://' + rabbitmq_endpoint + '&amqp-exchange=' + exchange_name + '&amqp-ack-level=broker'
       
        # in case wanted MQ endpoint is not provided by the user 
        else:
            raise Exception("please configure MQ endpoint!")

        # parsing given args to attributes 
        attributes = {nvp[0]: nvp[1] for nvp in urllib.parse.parse_qsl(endpoint_args, keep_blank_values=True)}
        
        # creates the wanted sns-like topic on RGW
        self.sns.create_topic(Name=self.topic, Attributes=attributes)

    ''' This finction confiogures bucket notification for object creation and removal '''
    def configure_bucket_notification(self): 
        
        # creates a bucket if not exists
        self.s3.create_bucket(Bucket = self.bucket_name)

        # generates the topic ARN based on the provided topic
        topic_arn = "arn:aws:sns:default::" + self.topic 

        # initial dictionary 
        bucket_notifications_configuration = {
            'TopicConfigurations': [
                {
                    'Id': 'test-configuration',
                    'TopicArn': '',
                    'Events': ['s3:ObjectCreated:*', 's3:ObjectRemoved:*']
                }
            ]
        }

        # updated the topic name provided as variable 
        bucket_notifications_configuration['TopicConfigurations'][0]['TopicArn'] = topic_arn

        # pushed the notification configuration to the bucket 
        self.s3.put_bucket_notification_configuration(Bucket = self.bucket_name,
                                                        NotificationConfiguration=bucket_notifications_configuration)

if __name__ == '__main__':

    # creates an notifier instance from class
    notifier = Notifier()

    # create sns-like topic sent to MQ endpoint 
    notifier.create_sns_topic()

    # configures object creation and removal based notification for the bucket
    notifier.configure_bucket_notification()

