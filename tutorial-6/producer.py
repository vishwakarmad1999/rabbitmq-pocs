import pika, sys

EXCHANGE_NAME = "header_logs"

connection = pika.BlockingConnection(parameters=pika.ConnectionParameters("localhost"))
channel = connection.channel()

channel.exchange_declare(
    exchange=EXCHANGE_NAME,
    exchange_type="headers",
)

confirm = True if len(sys.argv) > 1 and sys.argv[1] == "t" else False
message = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else "Order #0090 Confirmed"

channel.basic_publish(
    exchange=EXCHANGE_NAME,
    routing_key="",
    body=message,
    properties=pika.BasicProperties(
        headers={
            "action": "book",
            "confirm": confirm,
        }
    ),
)

print(f" [x] '{message}' sent!")

channel.close()
connection.close()
