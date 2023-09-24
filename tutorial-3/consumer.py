import pika

def main():
    connection = pika.BlockingConnection(parameters=pika.ConnectionParameters("localhost"))
    channel = connection.channel()

    res = channel.queue_declare(queue="", exclusive=True)
    queue_name = res.method.queue

    channel.queue_bind(
        queue=queue_name,
        exchange='logs',
    )

    def callback(*args):
        print(f" [x] Message '{args[-1].decode()}' processed ✅\n")
        
    channel.basic_consume(
        queue=queue_name,
        on_message_callback=callback,
        auto_ack=True,
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
