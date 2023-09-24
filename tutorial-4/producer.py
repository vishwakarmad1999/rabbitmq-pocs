import pika
import sys

log_level, message = sys.argv[1:]

connection = pika.BlockingConnection(parameters=pika.ConnectionParameters("localhost"))
channel = connection.channel()

exchange_name = "direct_logs"

channel.exchange_declare(
    exchange=exchange_name,
    exchange_type="direct",
)

channel.basic_publish(
    exchange=exchange_name,
    routing_key=log_level,
    body=message
)

connection.close()
