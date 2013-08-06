import pika
import sys
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

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

channel = connection.channel()
channel.queue_declare(queue='hello')


channel.basic_publish(exchange='',routing_key='hello',body=command)

print " [x] Sent '%s'" % (command,)
connection.close()
