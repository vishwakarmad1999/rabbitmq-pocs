import pika


def main():
    con = pika.BlockingConnection(parameters=pika.ConnectionParameters("localhost"))
    channel = con.channel()
    
    queue_name = "tut1"
    channel.queue_declare(queue=queue_name)

    def callback(ch, method, properties, message):
        print(f" [x] Recieved '{message}' ✅")

    channel.basic_consume(
        queue=queue_name,
        on_message_callback=callback,
        auto_ack=True,
    )

    print(" [*] Waiting for the messages. Press CTRL+C to exit!")

    channel.start_consuming()


try:
    main()
except KeyboardInterrupt:
    try:
        import sys; sys.exit(0)
    except:
        import os; os._exit(0)