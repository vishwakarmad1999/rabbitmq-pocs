# RabbitMQ Tutorials

## Pre-Requisites

To get started with this repository, make sure you have RabbitMQ installed in your system. If not then the easiest way to get the message broker into your system would be through **Docker**. 

```bash
# Pull the RabbitMQ image
docker pull rabbitmq

# Run the container as a daemon
docker run -dp 5672:5672 --hostname myrmq --name rmq rabbitmq
```

After you have the RabbitMQ container running in your system, create a virtual environment for the Python modules, mainly **pika**. The python library, pika, provides us the APIs to interact with RabbitMQ.

```bash
# Create a virtual environment
python -m venv venv

# Activate it. 
# Once you have activated the virtual environment, its name would start to appear in your terminal like (venv) 
source venv/bin/activate

# Install pika thereafter
pip install pika
```

Now that you have completed the pre-requisites, navigate to the tutorial directories (like _tutorial-1_) and follow the **README.md** file there!

Happy **Learning**!