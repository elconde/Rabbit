"""Demo Rabbit MQ functionality."""
import pika
import FLogger

logger = FLogger.FLogger(__name__,level=2)

def start():
    logger.DLOG('DEBUG LOGGING ENABLED')
    global connection
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost')
    )
    channel = connection.channel()
    channel.queue_declare(queue='hello')
    channel.basic_consume(callback,queue='hello',no_ack=True)
    logger.LOG('Waiting for messages...')
    channel.start_consuming()

    
def stop():
    print 'stop'*20
    return
    
def status():
    print 'status'*20
    return
    
def work():
    return

def callback(ch,method,properties,body):
    logger.DLOG('Received %r',body)
