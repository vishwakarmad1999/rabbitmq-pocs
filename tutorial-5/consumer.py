import pika

def error_cb(*args):
    print(f"Processed error.*: {args[-1].decode()} ✅\n")

def logs_cb(*args):
    print(f"Processed #.logs: {args[-1].decode()} ✅\n")

ROUTING_CB_MAP = {
    '#.logs' : logs_cb,
    'error.*' : error_cb,
}
EXCHANGE_NAME = "topic_logs"

def main():
    connection = pika.BlockingConnection(parameters=pika.ConnectionParameters(host="localhost"))    
    channel = connection.channel()

    channel.exchange_declare(
        exchange=EXCHANGE_NAME,
        exchange_type="topic",
        auto_delete=True,
    )

    for routing_key, cb in ROUTING_CB_MAP.items():
        res = channel.queue_declare(
            queue="",
            exclusive=True,
        )
        queue_name = res.method.queue

        channel.queue_bind(
            queue=queue_name,
            exchange=EXCHANGE_NAME,
            routing_key=routing_key,
        )

        channel.basic_consume(
            queue=queue_name,
            on_message_callback=cb,
            auto_ack=True,
        )

    print("Listening for messages. Press CTRL+C to exit!\n")
    channel.start_consuming()

try:
    main()
except KeyboardInterrupt:
    try:
        from sys import exit; exit(0)
    except:
        from os import _exit; _exit(0)
