from common.config import Config
import boto3
import logging
from botocore.exceptions import ClientError


class Storage:
    def __init__(self):
        self.s3_config = Config().s3_config
        self.general_config = Config().general_config
        self.s3_bucket_name = self.s3_config['bucket_name']
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=self.s3_config['aws_access_key_id'],
            aws_secret_access_key=self.s3_config['aws_secret_access_key'],
            aws_session_token=self.s3_config['aws_session_token'],
            region_name=self.s3_config['region']
        )

    def upload_file(self, file_name, object_name):
        try:
            response = self.s3_client.upload_file(file_name, self.s3_bucket_name, object_name)
        except ClientError as err:
            logging.error('Error uploading to S3: %s', err)
