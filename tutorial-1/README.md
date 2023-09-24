# Tutorial 1 - The Basics

RabbitMQ is a middleman that takes care of receiving messages from a producer, stores them into queues, and then post them to a consumer. It is widely used across the industry to tackle resource heavy processes in an asynchronous manner.

```bash
# To test the workings of the POC, open two tabs in your terminal

# Terminal 1
# This file would listen for the messgaes until you press CTRL+C
python consumer.py

# Terminal 2
# Run this file to send messages multiple times
python producer.py
```

---

The file, `producer.py`, first establishes a connection and then extracts a channel out of that connection. 

```py
connection = pika.BlockingConnection(parameters=pika.ConnectionParameters("localhost"))
channel = connection.channel()
```

A channel is used to perform numerous tasks like:
    - declaring a queue
    - publishing a message
    - listening for messages

And many more such operations are performed using a channel.

Once you have a created a channel, we declare a queue named as **tut1**. A queue is where RabbitMQ pushes the messages.

```py
queue_name = "tut1"
channel.queue_declare(queue=queue_name)
```

Now that we have a queue ready, we'll push a message to this queue using the `basic_publish` method of channel.

```py
message = "Hello World"

channel.basic_publish(
    exchange="", # We'll discuss this parameter later
    routing_key=queue_name, # The queue name is provided in the routing_key parameter
    body=message, # The message which you want to push
)

print(f" [x] '{message}' sent 👉")
```

After you have published the message, don't forget to close the connection to make sure the network buffers were flushed and the message was sent to RabbitMQ

```py
connection.close()
```

---

Now let's look at `consumer.py`

It also first establishes the connection as done by the producer. You'll notice we have declared the queue again in the consumer. If the queue does not exist in RabbitMQ, the consumer will take care of declaring it, otherwise if it was already exist, then it will remain untouched.

To listen to messages on a specific queue, we create a callback, that has 4 parameters, and the last one is the **message**. Just like you used `basic_publish` in the producer, we'll use `basic_consume` in the consumer. This statement would bind a queue with a callback.

Manual message acknowledgements are turned on by default. We have explicitly turned it off using `auto_ack=True`. More on this [Tutorial 2](/tutorial-2/README.md)

```py
def callback(ch, method, properties, message):
    print(f" [x] Recieved '{message}' ✅")

channel.basic_consume(
    queue=queue_name,
    on_message_callback=callback,
    auto_ack=True, 
)
```

After we have executed the above two statements, we'll start listening for messages.

```py
print(" [*] Waiting for the messages. Press CTRL+C to exit!")

channel.start_consuming()
```