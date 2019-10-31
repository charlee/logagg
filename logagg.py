import argparse
import requests
from dataflowbox.sources import Tail, Timer
from dataflowbox.pipes import HttpElfParser, HttpRequestRate
from dataflowbox.targets import Print, CloudWatch
from dataflowbox import DataFlowBox


def log_aggregate(filename, aws_profile='default'):

    instance_id = get_instance_id()

    tail = Tail(filename)
    timer = Timer(tzname='US/Eastern', accuracy='minute')

    elf = HttpElfParser()
    request_rate = HttpRequestRate()

    output1 = Print()
    output2 = CloudWatch('ECE1779/A2', 'HttpRequestRate', instance_id, aws_profile=aws_profile)

    tail.subscribe(elf)

    elf.subscribe(request_rate)
    timer.subscribe(request_rate)

    request_rate.subscribe(output1)
    request_rate.subscribe(output2)

    logaggr = DataFlowBox()
    logaggr.add_source(tail)
    logaggr.add_source(timer)

    logaggr.start()


def get_instance_id():
    try:
        res = requests.get('http://169.254.169.254/latest/meta-data/instance-id', timeout=1)
        if res.status_code == 200:
            instance_id = res.text
            return instance_id
        else:
            return 'test-host'
    except requests.exceptions.ConnectTimeout:
        return 'test-host'


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', type=str, nargs=1)
    parser.add_argument('--profile', type=str, nargs='?', help='AWS profile')
    args = parser.parse_args()

    if args.profile:
        log_aggregate(args.filename[0], args.profile[0])
    else:
        log_aggregate(args.filename[0])
