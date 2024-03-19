import pika

EXCHANGE_NAME = "header_logs"

connection = pika.BlockingConnection(parameters=pika.ConnectionParameters("localhost"))
channel = connection.channel()

channel.exchange_declare(
    exchange=EXCHANGE_NAME,
    exchange_type="headers",
)

res = channel.queue_declare(
    queue="",
    auto_delete=True,
)
queue = res.method.queue

channel.queue_bind(
    queue=queue,
    exchange=EXCHANGE_NAME,
    routing_key="",
    arguments={
        "x-match": "any",
        "confirm": True,
        "action": "cancel"
    },
)

def callback(*args):
    print(f" [x] Received '{args[-1].decode()}'")

channel.basic_consume(
    queue=queue,
    on_message_callback=callback,
    auto_ack=True,
)

def main():
    print(" [*] Listening for messages")
    channel.start_consuming()

try:
    main()
except KeyboardInterrupt:
    try:
        from sys import exit
        exit(0)
    except:
        from os import _exit
        _exit(0)
