import pika
from sys import argv

EXCHANGE_NAME = "topic_logs"

log_type, message = argv[1:]

connection = pika.BlockingConnection(parameters=pika.ConnectionParameters(host="localhost"))
channel = connection.channel()

channel.exchange_declare(
    exchange=EXCHANGE_NAME,
    exchange_type="topic",
    auto_delete=True,
)

channel.basic_publish(
    exchange=EXCHANGE_NAME,
    routing_key=log_type,
    body=message,
)

print(f"Message '{message}' sent 🚛")

connection.close()
