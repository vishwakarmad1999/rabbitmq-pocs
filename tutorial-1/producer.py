import pika

connection = pika.BlockingConnection(parameters=pika.ConnectionParameters("localhost"))
channel = connection.channel()

queue_name = "tut1"
channel.queue_declare(queue=queue_name)

message = "Hello World"

channel.basic_publish(
    exchange="",
    routing_key=queue_name,
    body=message
)

print(f" [x] '{message}' sent 👉")

connection.close()