import pika
import time

def main():
    connection = pika.BlockingConnection(parameters=pika.ConnectionParameters("localhost"))
    channel = connection.channel()

    queue_name = "tut2"
    channel.queue_declare(queue=queue_name, durable=True)

    def callback(ch, method, properties, message):
        print(f" [x] Message {message} received")
        time.sleep(int(message.decode()))        
        print(f" [x] Message processed ✅\n")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(
        queue=queue_name,
        on_message_callback=callback,
    )

    channel.basic_qos(prefetch_count=1)

    print(" [*] Waiting for the messages. Press CTRL+C to exit!\n")
    channel.start_consuming()

try:
    main()
except KeyboardInterrupt:
    try:
        import sys; sys.exit(0)
    except:
        import os; os._exit(0)