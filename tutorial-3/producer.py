import pika
import sys

connection = pika.BlockingConnection(parameters=pika.ConnectionParameters("localhost"))
channel = connection.channel()

channel.exchange_declare(
    exchange="logs",
    exchange_type="fanout",
)

message = sys.argv[1]

channel.basic_publish(
    exchange="logs",
    routing_key="",
    body=message
)

print(f" [x] Message '{message}' sent 👉")
