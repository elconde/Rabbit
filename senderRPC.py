"""Testing out RabbitMQ Remote Procedure Calls to the ATS"""
import pika
import uuid
import argparse

parser = argparse.ArgumentParser(description='Send commands to RabbitMQ')
parser.add_argument(
    'command',
    metavar='CMD',
    type=str,
    help='The command to send to the ATS',
    nargs='+'
)
args = parser.parse_args()
command = ' '.join(args.command)


class ATSRPCClient(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost')
        )
        self.channel=self.connection.channel()
        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(
            self.on_response,
            no_ack=True,
            queue=self.callback_queue
        )
    def on_response(self,ch,method,props,body):
        if self.corr_id == props.correlation_id:
            self.response=body
            
    def call(self, cmd):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key = 'rpc_queue',
            properties = pika.BasicProperties(
                reply_to = self.callback_queue,
                correlation_id = self.corr_id
            ),
            body = cmd
        )
        
        while self.response is None:
            self.connection.process_data_events()
        return self.response
        
        
myATSRPCClient = ATSRPCClient()
response = myATSRPCClient.call(command)
print response
