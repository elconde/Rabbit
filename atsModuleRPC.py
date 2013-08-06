"""ATS server for consuming requests from RabbitMQ"""
import pika
import acm
import FLogger
logger = FLogger.FLogger(__name__,level=2)

def ATSCallback(command):
    return eval(command)
    
    
def on_request(ch, method, props, command):
    logger.LOG('Received %s',command)
    exec('response = %s' % (command,))
    logger.DLOG('response %s',response)

    ch.basic_publish(
        exchange='',
        routing_key=props.reply_to,
        properties=pika.BasicProperties(
            correlation_id = props.correlation_id
        ),
        body=str(response)
    )
    ch.basic_ack(delivery_tag = method.delivery_tag)

def start():
    logger.DLOG('DEBUG LOGGING ENABLED')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host='localhost'
        )
    )

    channel = connection.channel()

    channel.queue_declare(queue='rpc_queue')

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(on_request, queue='rpc_queue')
    logger.LOG('Awaiting RPC requests')
    channel.start_consuming()