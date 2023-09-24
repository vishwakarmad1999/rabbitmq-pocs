import pika

def main():
    connection = pika.BlockingConnection(parameters=pika.ConnectionParameters("localhost"))
    channel = connection.channel()

    r1 = channel.queue_declare(queue="", exclusive=True)
    r2 = channel.queue_declare(queue="", exclusive=True)
    
    q1 = r1.method.queue
    q2 = r2.method.queue

    exchange_name = "direct_logs"

    channel.exchange_declare(
        exchange=exchange_name,
        exchange_type="direct",
    )

    channel.queue_bind(
        exchange=exchange_name,
        queue=q1,
        routing_key="error"
    )

    channel.queue_bind(
        queue=q2,
        exchange=exchange_name,
        routing_key="other"
    )
    
    def c1(*args):
        with open("error.txt", "a") as f:
            f.write(f"{ args[-1].decode() }\n")

    def c2(*args):
        print(f" [x] Info/Warning Logs: {args[-1].decode()}")

    channel.basic_consume(
        queue=q1,
        on_message_callback=c1,
        auto_ack=True,
    )

    channel.basic_consume(
        queue=q2,
        on_message_callback=c2,
        auto_ack=True
    )

    print(" [*] Waiting for the messages. Press CTRL+C to exit!\n")
    channel.start_consuming()

try:
    main()
except KeyboardInterrupt:
    try:
        import sys; sys.exit(0)
    except:
        import os; os._exit(0)

