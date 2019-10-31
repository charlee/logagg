import boto3
from ..base import Target


class CloudWatch(Target):
    def __init__(self, namespace, metric_name, instance_id, aws_profile=None, aws_config=None):
        super().__init__()

        if aws_config is not None:
            self.client = boto3.client('cloudwatch',
                                       region_name=aws_config.region_name,
                                       aws_access_key_id=aws_config.aws_access_key_id,
                                       aws_secret_access_key=aws_config.aws_secret_access_key,
                                      )
        elif aws_profile is not None:
            session = boto3.session.Session(profile_name=aws_profile)
            self.client = session.client('cloudwatch')
        else:
            self.client = boto3.client('cloudwatch')

        self.namespace = namespace
        self.metric_name = metric_name
        self.instance_id = instance_id


    def notify(self, event):
        if event.event_type == 'http_request_rate':
            response = self.client.put_metric_data(
                Namespace=self.namespace,
                MetricData=[
                    {
                        'MetricName': self.metric_name,
                        'Dimensions': [
                            { 'Name': 'InstanceId', 'Value': self.instance_id },
                        ],
                        'Timestamp': event.payload['datetime'],
                        'Value': event.payload['count'],
                    }
                ]
            )

