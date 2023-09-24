import pika
import sys

connection = pika.BlockingConnection(parameters=pika.ConnectionParameters("localhost"))
channel = connection.channel()

queue_name = "tut2"
channel.queue_declare(queue=queue_name, durable=True)

message = sys.argv[1]
channel.basic_publish(
    exchange="",
    routing_key=queue_name,
    body=message,
    properties=pika.BasicProperties(
        delivery_mode=pika.DeliveryMode.Persistent
    )
)

print(f" [x] Message '{message}' sent 👉")

connection.close()
